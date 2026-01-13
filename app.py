import streamlit as st
from fpdf import FPDF
from difflib import SequenceMatcher
import random
import unicodedata

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Contrôle 5ème : Masse et Volume", page_icon="🧪", layout="centered")

# --- FONCTIONS UTILITAIRES ---

def remove_accents(input_str):
    if not input_str: return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def check_spelling(answer_user, answer_key):
    if not answer_user: return False
    # 1. On nettoie tout (minuscule + sans accent)
    clean_user = remove_accents(str(answer_user).lower().strip())
    clean_key = remove_accents(str(answer_key).lower().strip())
    
    # 2. Comparaison souple (Ratio de similarité)
    # 0.75 permet d'accepter "menicque" pour "menisque"
    ratio = SequenceMatcher(None, clean_user, clean_key).ratio()
    return ratio >= 0.75

# --- GENERATION PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Correction : La Masse et le Volume', 0, 1, 'C')
        self.ln(5)

def create_detailed_pdf(nom, prenom, classe, score, total, report):
    pdf = PDF()
    pdf.add_page()
    
    # Infos
    pdf.set_font("Arial", '', 12)
    pdf.set_fill_color(230, 230, 250)
    pdf.cell(0, 10, txt=f"Eleve : {nom} {prenom} | Classe : {classe}", ln=1, align='L', fill=True)
    
    # Note
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    color = (0, 100, 0) if score >= 10 else (200, 0, 0)
    pdf.set_text_color(*color)
    pdf.cell(0, 10, txt=f"NOTE FINALE : {score} / {total}", ln=1, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Détails
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Correction detaillee :", ln=1)
    
    for item in report:
        q = item['question'].encode('latin-1', 'replace').decode('latin-1')
        u = str(item['user_answer']).encode('latin-1', 'replace').decode('latin-1')
        c = str(item['correct_answer']).encode('latin-1', 'replace').decode('latin-1')
        
        pdf.ln(4)
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(240, 240, 240)
        pdf.multi_cell(0, 8, txt=f"Question : {q}", fill=True)
        
        pdf.set_font("Arial", '', 11)
        if item['is_correct']:
            pdf.set_text_color(0, 128, 0)
            pdf.cell(0, 6, txt=f"   Votre reponse : {u} (Correct !)", ln=1)
        else:
            pdf.set_text_color(200, 0, 0)
            pdf.cell(0, 6, txt=f"   Votre reponse : {u}", ln=1)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 6, txt=f"   -> La bonne reponse etait : {c}", ln=1)
        pdf.set_text_color(0, 0, 0)

    return pdf.output(dest='S').encode('latin-1')

# --- INITIALISATION STATE (Mémoire) ---
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if 'shuffled_protocol' not in st.session_state:
    etapes_sans_num = ["Allumer la balance", "Poser le gobelet vide", "Appuyer sur TARE", "Verser le sable jusqu'à 50g", "Lire la valeur affichée"]
    melange = etapes_sans_num.copy()
    while melange == etapes_sans_num:
        random.shuffle(melange)
    st.session_state.shuffled_protocol = melange
    st.session_state.correct_protocol_values = etapes_sans_num

# --- INTERFACE ---
# Variable pour verrouiller les inputs si déjà soumis
disable_inputs = st.session_state.submitted

with st.sidebar:
    st.header("👤 Identité")
    nom = st.text_input("Ton Nom", disabled=disable_inputs)
    prenom = st.text_input("Ton Prénom", disabled=disable_inputs)
    classe = st.selectbox("Ta Classe", ["5 Sci C", "5 Sci D", "5 Sci E", "Autre"], disabled=disable_inputs)
    if st.session_state.submitted:
        st.info("⚠️ Le contrôle est terminé. Tu ne peux plus modifier tes réponses.")

st.title("🧪 Contrôle : La Masse et le Volume")
st.markdown("---")

with st.form("quiz_form"):
    
    # EXERCICE 1
    st.subheader("Exercice 1 : Le bon vocabulaire (4 pts)")
    q1 = st.radio("1. Définition du VOLUME :", 
                  ["La quantité de matière dans un objet", "L'espace occupé par un objet", "Le poids de l'objet"], 
                  disabled=disable_inputs)
    q2 = st.radio("2. Définition de la MASSE :", 
                  ["La quantité de matière dans un objet", "L'espace occupé par un objet", "La taille de l'objet"],
                  disabled=disable_inputs)
    
    c1, c2 = st.columns(2)
    q3_vol = c1.selectbox("Pour mesurer un VOLUME on utilise :", ["Une balance", "Une éprouvette graduée", "Une règle"], disabled=disable_inputs)
    q3_mas = c2.selectbox("Pour mesurer une MASSE on utilise :", ["Une balance", "Une éprouvette graduée", "Un thermomètre"], disabled=disable_inputs)
    st.markdown("---")

    # EXERCICE 2
    st.subheader("Exercice 2 : Les conversions (3 pts)")
    st.caption("Rappel : 1 L = 1 dm³ et 1 mL = 1 cm³")
    cc1, cc2, cc3 = st.columns(3)
    q4 = cc1.text_input("1,5 L = ... dm³", disabled=disable_inputs)
    q5 = cc2.text_input("350 mL = ... cm³", disabled=disable_inputs)
    q6 = cc3.text_input("2 kg = ... g", disabled=disable_inputs)
    st.markdown("---")

    # EXERCICE 3
    st.subheader("Exercice 3 : La pratique (6 pts)")
    st.write(" **A. Mesure de liquide**")
    q7 = st.text_input("Comment s'appelle la courbe formée par le liquide ?", disabled=disable_inputs).strip()
    q8 = st.radio("Où faut-il placer son œil ?", ["Au dessus du liquide", "En face du bas du ménisque", "En dessous du niveau"], disabled=disable_inputs)
    
    st.write(" **B. Mesure de solide**")
    col_txt, col_dum = st.columns([2,1])
    with col_txt:
        st.info("Léa met 30 mL d'eau (V1). Elle ajoute une pierre, le niveau monte à 48 mL (V2).")
        q9 = st.number_input("Quel est le volume de la pierre (en mL) ?", min_value=0, step=1, disabled=disable_inputs)
    st.markdown("---")

    # EXERCICE 4
    st.subheader("Exercice 4 : Le Protocole (4 pts)")
    st.write("Remets les étapes pour peser 50g de sable.")
    opts = ["-- Choisir --"] + st.session_state.shuffled_protocol
    
    pe1 = st.selectbox("Étape 1", opts, key="p1", disabled=disable_inputs)
    pe2 = st.selectbox("Étape 2", opts, key="p2", disabled=disable_inputs)
    pe3 = st.selectbox("Étape 3", opts, key="p3", disabled=disable_inputs)
    pe4 = st.selectbox("Étape 4", opts, key="p4", disabled=disable_inputs)
    pe5 = st.selectbox("Étape 5", opts, key="p5", disabled=disable_inputs)
    st.markdown("---")

    # EXERCICE 5
    st.subheader("Exercice 5 : Réflexion (3 pts)")
    q10 = st.number_input("Quelle est la masse d'un Litre d'eau (en kg) ?", min_value=0.0, step=0.1, disabled=disable_inputs)
    q11 = st.radio("1 L d'huile est-il plus lourd ou plus léger qu'1 L d'eau ?", ["Plus lourd", "Plus léger"], disabled=disable_inputs)
    q12 = st.text_input("Grandeur liant masse et volume ?", disabled=disable_inputs).strip()

    # Le bouton disparaît ou se grise après validation
    submit_btn = st.form_submit_button("✅ Valider ma copie", disabled=disable_inputs)

# --- LOGIQUE DE CORRECTION ---
if submit_btn or st.session_state.submitted:
    
    # 1. Vérification Anti-Doublon (Uniquement si c'est la première soumission)
    if not st.session_state.submitted:
        choix_proto = [pe1, pe2, pe3, pe4, pe5]
        choix_reels = [c for c in choix_proto if c != "-- Choisir --"]
        
        if len(set(choix_reels)) < len(choix_reels):
            st.error("⛔ Tu as mis plusieurs fois la même étape ! Corrige avant de valider.")
            st.stop()
        if "-- Choisir --" in choix_proto:
            st.warning("⚠️ Tu n'as pas fini le protocole.")
            st.stop()
            
        # Si tout est bon, on verrouille pour de bon
        st.session_state.submitted = True
        st.rerun() # On recharge la page pour griser les inputs

    # 2. Calcul des points (Maintenant que c'est verrouillé)
    score = 0
    report = []

    def check(q, u, c, pts, fuzzy=False, num=False):
        ok = False
        if num:
            try: 
                if float(str(u).replace(',','.')) == float(c): ok = True
            except: pass
        elif fuzzy:
            if check_spelling(str(u), str(c)): ok = True
        else:
            if str(u) == str(c): ok = True
        
        report.append({"question": q, "user_answer": u, "correct_answer": c, "is_correct": ok})
        return pts if ok else 0

    # Ex 1
    score += check("Def Volume", q1, "L'espace occupé par un objet", 1)
    score += check("Def Masse", q2, "La quantité de matière dans un objet", 1)
    score += check("Instru Volume", q3_vol, "Une éprouvette graduée", 1)
    score += check("Instru Masse", q3_mas, "Une balance", 1)
    # Ex 2
    score += check("1,5 L -> dm3", q4, "1.5", 1, num=True)
    score += check("350 mL -> cm3", q5, "350", 1, num=True)
    score += check("2 kg -> g", q6, "2000", 1, num=True)
    # Ex 3
    score += check("Courbe liquide", q7, "Ménisque", 1, fuzzy=True) # "menicque" passera
    score += check("Position oeil", q8, "En face du bas du ménisque", 2)
    score += check("Volume Pierre", q9, 18, 3, num=True)
    
    # Ex 4 (Protocole)
    user_order = [pe1, pe2, pe3, pe4, pe5]
    corr_order = st.session_state.correct_protocol_values
    pts_p = 0
    if user_order == corr_order: pts_p = 4
    elif user_order[0] == corr_order[0] and user_order[2] == corr_order[2]: pts_p = 2
    
    score += pts_p
    report.append({"question": "Ordre Protocole", "user_answer": "(Voir copie)", "correct_answer": "1.Allumer, 2.Gobelet, 3.Tare, 4.Verser, 5.Lire", "is_correct": pts_p==4})

    # Ex 5
    score += check("Masse 1L eau", q10, 1, 1, num=True)
    score += check("Huile vs Eau", q11, "Plus léger", 1)
    score += check("Masse Volumique", q12, "Masse Volumique", 1, fuzzy=True)

    # Affichage résultat
    st.success(f"Copie rendue ! Note finale : {score} / 20")
    
    if nom and prenom:
        pdf_data = create_detailed_pdf(nom, prenom, classe, score, 20, report)
        st.download_button("📄 TÉLÉCHARGER MA COPIE CORRIGÉE", pdf_data, f"Controle_{nom}.pdf", "application/pdf")
    else:
        st.error("⚠️ Tu as oublié de mettre ton nom ! (Recharge la page pour recommencer si besoin)")