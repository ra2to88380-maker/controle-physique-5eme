import streamlit as st
from fpdf import FPDF
from difflib import SequenceMatcher
import random
import unicodedata

# --- 1. CONFIGURATION & DESIGN ---
st.set_page_config(page_title="Contrôle 6ème : Masse et Volume", page_icon="🧪", layout="centered")

# CSS pour le design
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        color: #4B0082;
        text-align: center;
        font-family: 'Helvetica', sans-serif;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FONCTIONS UTILITAIRES ---
def remove_accents(input_str):
    if not input_str: return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def check_spelling_ratio(answer_user, answer_key):
    if not answer_user: return 0.0
    clean_user = remove_accents(str(answer_user).lower().strip())
    clean_key = remove_accents(str(answer_key).lower().strip())
    return SequenceMatcher(None, clean_user, clean_key).ratio()

# --- GENERATION PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(75, 0, 130) # Violet
        self.cell(0, 10, 'Correction : La Masse et le Volume', 0, 1, 'C')
        self.ln(5)

def create_detailed_pdf(nom, prenom, classe, score, total, report):
    pdf = PDF()
    pdf.add_page()
    
    # Cadre Info Élève
    pdf.set_font("Arial", '', 12)
    pdf.set_fill_color(240, 240, 255) # Bleu très pâle
    pdf.set_draw_color(200, 200, 200)
    pdf.rect(10, 25, 190, 15, 'DF')
    pdf.set_xy(15, 28)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=f"Eleve : {nom} {prenom}   |   Classe : {classe}", ln=1)
    
    # Note
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    if score >= 10:
        pdf.set_text_color(34, 139, 34) # Vert Forêt
    else:
        pdf.set_text_color(220, 20, 60) # Rouge
    pdf.cell(0, 10, txt=f"NOTE FINALE : {score} / {total}", ln=1, align='C')
    pdf.ln(5)
    
    # Détails
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt="Correction detaillee par exercice :", ln=1)
    
    for item in report:
        q = item['question'].encode('latin-1', 'replace').decode('latin-1')
        u = str(item['user_answer']).encode('latin-1', 'replace').decode('latin-1')
        c = str(item['correct_answer']).encode('latin-1', 'replace').decode('latin-1')
        status = item['status'] 
        
        pdf.ln(3)
        # Question (Fond gris)
        pdf.set_font("Arial", 'B', 10)
        pdf.set_fill_color(245, 245, 245)
        pdf.multi_cell(0, 7, txt=f"Q: {q}", fill=True)
        
        # Réponse
        pdf.set_font("Arial", '', 10)
        if status == 'perfect':
            pdf.set_text_color(0, 128, 0) # Vert
            pdf.cell(0, 6, txt=f"   -> {u} (Parfait)", ln=1)
        elif status == 'fuzzy':
            pdf.set_text_color(255, 140, 0) # Orange foncé
            pdf.cell(0, 6, txt=f"   -> {u} (Accepte avec faute)", ln=1)
            pdf.set_font("Arial", 'I', 9)
            pdf.cell(0, 6, txt=f"      Orthographe correcte : {c}", ln=1)
        else:
            pdf.set_text_color(178, 34, 34) # Rouge
            pdf.cell(0, 6, txt=f"   -> {u} (Faux)", ln=1)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", 'B', 9)
            pdf.cell(0, 6, txt=f"      Reponse attendue : {c}", ln=1)
        
        pdf.set_text_color(0, 0, 0)

    return pdf.output(dest='S').encode('latin-1')

# --- LOGIQUE STATE (Mémoire) ---
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if 'shuffled_protocol' not in st.session_state:
    etapes_sans_num = ["Allumer la balance", "Poser le gobelet vide", "Appuyer sur TARE", "Verser le sable jusqu'à 50g", "Lire la valeur affichée"]
    melange = etapes_sans_num.copy()
    while melange == etapes_sans_num:
        random.shuffle(melange)
    st.session_state.shuffled_protocol = melange
    st.session_state.correct_protocol_values = etapes_sans_num

# --- INTERFACE UTILISATEUR ---
disable = st.session_state.submitted

# Sidebar
with st.sidebar:
    st.header("Identité de l'élève")
    nom = st.text_input("NOM de famille", disabled=disable).upper()
    prenom = st.text_input("Prénom", disabled=disable).capitalize()
    
    # --- MODIFICATION ICI : CLASSES 6EME ---
    classe = st.selectbox("Classe", ["6ème C", "6ème D", "Autre"], disabled=disable)
    
    if st.session_state.submitted:
        st.success("✅ Copie rendue.")

st.title("⚖️ Contrôle 6ème : Masse et Volume")
st.markdown("---")

with st.form("quiz_form"):
    
    # --- EXERCICE 1 ---
    with st.container(border=True):
        st.subheader("Exercice 1 : Vocabulaire (4 pts)")
        q1 = st.radio("1. Définition du VOLUME :", 
                      ["La quantité de matière", "L'espace occupé par un objet", "Le poids de l'objet"], 
                      horizontal=True, disabled=disable)
        q2 = st.radio("2. Définition de la MASSE :", 
                      ["La quantité de matière", "L'espace occupé par un objet", "La taille de l'objet"],
                      horizontal=True, disabled=disable)
        
        st.markdown("**3. Instruments et Unités :**")
        c1, c2 = st.columns(2)
        q3_vol = c1.selectbox("Outil pour le VOLUME :", ["Une balance", "Une éprouvette graduée", "Une règle"], disabled=disable)
        q3_mas = c2.selectbox("Outil pour la MASSE :", ["Une balance", "Une éprouvette graduée", "Un thermomètre"], disabled=disable)

    # --- EXERCICE 2 ---
    with st.container(border=True):
        st.subheader("Exercice 2 : Conversions (3 pts)")
        st.info("Rappel : 1 L = 1 dm³ et 1 mL = 1 cm³")
        cc1, cc2, cc3 = st.columns(3)
        q4 = cc1.text_input("1,5 L = ... dm³", disabled=disable)
        q5 = cc2.text_input("350 mL = ... cm³", disabled=disable)
        q6 = cc3.text_input("2 kg = ... g", disabled=disable)

    # --- EXERCICE 3 ---
    with st.container(border=True):
        st.subheader("Exercice 3 : La Pratique (6 pts)")
        
        st.markdown("#### A. Mesure de liquide")
        c_liq1, c_liq2 = st.columns(2)
        q7 = c_liq1.text_input("Nom de la courbe du liquide ?", disabled=disable).strip()
        q8 = c_liq2.radio("Où placer son œil ?", ["Au dessus", "En face du bas du ménisque", "En dessous"], disabled=disable)
        
        st.divider()
        st.markdown("#### B. Solide (Déplacement d'eau)")
        col_txt, col_dum = st.columns([3,1])
        with col_txt:
            st.info("💧 V1 (eau) = **30 mL** |  🪨 V2 (eau + pierre) = **48 mL**")
            q9 = st.number_input("Quel est le volume de la pierre (mL) ?", min_value=0, step=1, disabled=disable)

    # --- EXERCICE 4 ---
    with st.container(border=True):
        st.subheader("Exercice 4 : Le Protocole (4 pts)")
        st.write("Remets les étapes pour peser **50g de sable** dans l'ordre.")
        
        opts = ["-- Choisir --"] + st.session_state.shuffled_protocol
        
        # Affichage plus compact
        pe1 = st.selectbox("Étape 1", opts, key="p1", disabled=disable)
        pe2 = st.selectbox("Étape 2", opts, key="p2", disabled=disable)
        pe3 = st.selectbox("Étape 3", opts, key="p3", disabled=disable)
        pe4 = st.selectbox("Étape 4", opts, key="p4", disabled=disable)
        pe5 = st.selectbox("Étape 5", opts, key="p5", disabled=disable)

    # --- EXERCICE 5 ---
    with st.container(border=True):
        st.subheader("Exercice 5 : Réflexion (3 pts)")
        c5a, c5b = st.columns(2)
        q10 = c5a.number_input("Masse d'1 L d'eau (kg) ?", 0.0, step=0.1, disabled=disable)
        q11 = c5b.radio("1 L d'huile est...", ["Plus lourd que l'eau", "Plus léger que l'eau"], disabled=disable)
        q12 = st.text_input("Nom de la grandeur (Masse...?)", disabled=disable).strip()

    # Bouton de validation
    submit_btn = st.form_submit_button("✅ VALIDER MA COPIE", disabled=disable)

# --- CORRECTION ---
if submit_btn or st.session_state.submitted:
    
    # 1. Vérification Anti-Doublon (Seulement au premier clic)
    if not st.session_state.submitted:
        choix = [pe1, pe2, pe3, pe4, pe5]
        reels = [c for c in choix if c != "-- Choisir --"]
        
        if len(set(reels)) < len(reels):
            st.error("⛔ Erreur : Tu as mis plusieurs fois la même étape !")
            st.stop()
        if "-- Choisir --" in choix:
            st.warning("⚠️ Complète toutes les étapes du protocole.")
            st.stop()
            
        st.session_state.submitted = True
        st.rerun()

    # 2. Notation
    score = 0
    report = []

    def check(q, u, c, pts, type_check="text"):
        status = "wrong"
        points_gagnes = 0
        
        if type_check == "num":
            try:
                if float(str(u).replace(',','.')) == float(c): 
                    status = "perfect"
                    points_gagnes = pts
            except: pass
            
        elif type_check == "fuzzy":
            ratio = check_spelling_ratio(str(u), str(c))
            if str(u).lower().strip() == str(c).lower().strip():
                status = "perfect"
                points_gagnes = pts
            elif ratio >= 0.75: # Tolérance
                status = "fuzzy"
                points_gagnes = pts
                
        else: # Text exact
            if str(u) == str(c):
                status = "perfect"
                points_gagnes = pts
        
        report.append({"question": q, "user_answer": u, "correct_answer": c, "status": status})
        return points_gagnes

    # Calculs Ex 1, 2, 3, 5
    score += check("Def Volume", q1, "L'espace occupé par un objet", 1)
    score += check("Def Masse", q2, "La quantité de matière", 1)
    score += check("Outil Volume", q3_vol, "Une éprouvette graduée", 1)
    score += check("Outil Masse", q3_mas, "Une balance", 1)
    
    score += check("1,5 L -> dm3", q4, "1.5", 1, "num")
    score += check("350 mL -> cm3", q5, "350", 1, "num")
    score += check("2 kg -> g", q6, "2000", 1, "num")
    
    score += check("Courbe liquide", q7, "Ménisque", 1, "fuzzy")
    score += check("Position oeil", q8, "En face du bas du ménisque", 2)
    score += check("Volume Pierre", q9, 18, 3, "num")
    
    score += check("Masse 1L eau", q10, 1, 1, "num")
    score += check("Huile vs Eau", q11, "Plus léger que l'eau", 1)
    score += check("Masse Volumique", q12, "Masse Volumique", 1, "fuzzy")

    # Calcul Spécial Ex 4 (1 erreur = -1 point)
    user_order = [pe1, pe2, pe3, pe4, pe5]
    corr_order = st.session_state.correct_protocol_values
    
    erreurs_proto = 0
    for i in range(5):
        if user_order[i] != corr_order[i]:
            erreurs_proto += 1
            
    # Formule : 4 points - nombre d'erreurs (min 0)
    pts_proto = max(0, 4 - erreurs_proto)
    score += pts_proto
    
    status_proto = "perfect" if pts_proto == 4 else "wrong"
    report.append({
        "question": "Ordre du Protocole", 
        "user_answer": f"{erreurs_proto} erreurs de placement", 
        "correct_answer": "1.Allumer, 2.Gobelet, 3.Tare, 4.Verser, 5.Lire", 
        "status": status_proto
    })

    # Affichage résultat
    if score >= 10:
        st.balloons()
        st.success(f"🎉 Bravo ! Note : **{score} / 20**")
    else:
        st.error(f"Note : **{score} / 20**. Télécharge le corrigé pour réviser.")

    if nom and prenom:
        pdf_bytes = create_detailed_pdf(nom, prenom, classe, score, 20, report)
        st.download_button("📄 TÉLÉCHARGER LE CORRIGÉ PDF", pdf_bytes, f"Controle_{nom}.pdf", "application/pdf")
    else:
        st.warning("⚠️ Remplis ton NOM et PRÉNOM à gauche pour avoir ton PDF !")