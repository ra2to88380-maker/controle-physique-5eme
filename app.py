import streamlit as st
from fpdf import FPDF
from difflib import SequenceMatcher
import random

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Contrôle 5ème : Masse et Volume", page_icon="🧪", layout="centered")

# Fonction pour vérifier l'orthographe (tolérance de 80%)
def check_spelling(answer_user, answer_key):
    if not answer_user: return False
    # On met tout en minuscule et on compare
    ratio = SequenceMatcher(None, answer_user.lower().strip(), answer_key.lower().strip()).ratio()
    return ratio > 0.8

# Fonction pour générer le PDF détaillé
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Correction : La Masse et le Volume', 0, 1, 'C')
        self.ln(5)

def create_detailed_pdf(nom, prenom, classe, score, total, report):
    pdf = PDF()
    pdf.add_page()
    
    # Infos élève
    pdf.set_font("Arial", '', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, txt=f"Élève : {nom} {prenom} | Classe : {classe}", ln=1, align='L', fill=True)
    
    # Note
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    if score >= 10:
        pdf.set_text_color(0, 100, 0) # Vert foncé
    else:
        pdf.set_text_color(200, 0, 0) # Rouge
    pdf.cell(0, 10, txt=f"NOTE FINALE : {score} / {total}", ln=1, align='C')
    pdf.set_text_color(0, 0, 0) # Reset noir
    pdf.ln(5)
    
    # Détail des réponses
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Détail de ta copie :", ln=1)
    
    pdf.set_font("Arial", '', 11)
    
    for item in report:
        question = item['question'].encode('latin-1', 'replace').decode('latin-1')
        user_ans = str(item['user_answer']).encode('latin-1', 'replace').decode('latin-1')
        correct_ans = str(item['correct_answer']).encode('latin-1', 'replace').decode('latin-1')
        is_correct = item['is_correct']
        
        # Affichage de la question
        pdf.set_font("Arial", 'B', 10)
        pdf.multi_cell(0, 6, txt=f"Q: {question}")
        
        # Affichage de la réponse
        pdf.set_font("Arial", '', 10)
        if is_correct:
            pdf.set_text_color(0, 128, 0) # Vert
            pdf.cell(0, 6, txt=f"  -> Ta réponse : {user_ans} (Correct)", ln=1)
        else:
            pdf.set_text_color(180, 0, 0) # Rouge
            pdf.cell(0, 6, txt=f"  -> Ta réponse : {user_ans} (Faux)", ln=1)
            pdf.set_text_color(0, 0, 0) # Noir
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 6, txt=f"     Correction : {correct_ans}", ln=1)
        
        pdf.ln(2) # Petit espace
        pdf.set_text_color(0, 0, 0) # Reset noir

    return pdf.output(dest='S').encode('latin-1')

# --- 2. INITIALISATION DES VARIABLES (S'assurer que l'ordre aléatoire reste le même pendant le test) ---
if 'shuffled_protocol' not in st.session_state:
    etapes = [
        "Allumer la balance",
        "Poser le gobelet vide",
        "Appuyer sur TARE",
        "Verser le sable jusqu'à 50g",
        "Lire la valeur affichée"
    ]
    # On crée une copie mélangée pour l'affichage
    options_melangees = etapes.copy()
    random.shuffle(options_melangees)
    st.session_state.shuffled_protocol = options_melangees
    st.session_state.correct_protocol = etapes

# --- 3. INTERFACE UTILISATEUR ---

# Sidebar pour les infos
with st.sidebar:
    st.header("👤 Identité")
    nom = st.text_input("Ton Nom")
    prenom = st.text_input("Ton Prénom")
    classe = st.selectbox("Ta Classe", ["5ème A", "5ème B", "5ème C", "Autre"])
    st.info("Remplis bien ces infos pour ton bulletin PDF.")

st.title("🧪 Contrôle : La Masse et le Volume")
st.markdown("---")

with st.form("quiz_form"):

    # EXERCICE 1
    st.subheader("Exercice 1 : Le bon vocabulaire (4 pts)")
    
    q1 = st.radio("1. Définition du VOLUME :", 
                  ["La quantité de matière dans un objet", "L'espace occupé par un objet", "Le poids de l'objet"])
    
    q2 = st.radio("2. Définition de la MASSE :", 
                  ["La quantité de matière dans un objet", "L'espace occupé par un objet", "La taille de l'objet"])
    
    st.markdown("**3. Les instruments et unités :**")
    c1, c2 = st.columns(2)
    q3_vol = c1.selectbox("Pour mesurer un VOLUME on utilise :", ["Une balance", "Une éprouvette graduée", "Une règle"])
    q3_mas = c2.selectbox("Pour mesurer une MASSE on utilise :", ["Une balance", "Une éprouvette graduée", "Un thermomètre"])

    st.markdown("---")

    # EXERCICE 2
    st.subheader("Exercice 2 : Les conversions (3 pts)")
    st.caption("Rappel : 1 L = 1 dm³ et 1 mL = 1 cm³")
    
    cc1, cc2, cc3 = st.columns(3)
    q4 = cc1.text_input("1,5 L = ... dm³")
    q5 = cc2.text_input("350 mL = ... cm³")
    q6 = cc3.text_input("2 kg = ... g")

    st.markdown("---")

    # EXERCICE 3
    st.subheader("Exercice 3 : La pratique (6 pts)")
    
    st.write(" **A. Mesure de liquide**")
    q7 = st.text_input("Comment s'appelle la courbe formée par le liquide ? (Attention à l'orthographe)").strip()
    q8 = st.radio("Où faut-il placer son œil ?", ["Au dessus du liquide", "En face du bas du ménisque", "En dessous du niveau"])
    
    st.write(" **B. Mesure de solide (Déplacement d'eau)**")
    col_img, col_txt = st.columns([1, 2])
    with col_txt:
        st.info("Léa met 30 mL d'eau (V1). Elle ajoute une pierre, le niveau monte à 48 mL (V2).")
        q9 = st.number_input("Quel est le volume de la pierre (en mL) ?", min_value=0, step=1)

    st.markdown("---")

    # EXERCICE 4
    st.subheader("Exercice 4 : Le Protocole (4 pts)")
    st.write("Remets les étapes pour peser 50g de sable dans l'ordre chronologique.")
    
    # On utilise la liste mélangée stockée en mémoire
    opts = ["-- Choisir --"] + st.session_state.shuffled_protocol
    
    pe1 = st.selectbox("Étape 1", opts, key="p1")
    pe2 = st.selectbox("Étape 2", opts, key="p2")
    pe3 = st.selectbox("Étape 3", opts, key="p3")
    pe4 = st.selectbox("Étape 4", opts, key="p4")
    pe5 = st.selectbox("Étape 5", opts, key="p5")

    st.markdown("---")

    # EXERCICE 5
    st.subheader("Exercice 5 : Réflexion (3 pts)")
    q10 = st.number_input("Quelle est la masse d'un Litre d'eau (en kg) ?", min_value=0.0, step=0.1)
    q11 = st.radio("1 Litre d'huile est-il plus lourd ou plus léger qu'un litre d'eau ?", ["Plus lourd", "Plus léger"])
    q12 = st.text_input("Quel est le nom de la grandeur liant masse et volume ?").strip()

    submit = st.form_submit_button("✅ Valider ma copie")

# --- 4. CORRECTION ET GÉNÉRATION ---
if submit:
    score = 0
    total = 20
    report = [] # Liste pour stocker le détail pour le PDF

    # Fonction helper pour ajouter au rapport et compter les points
    def check(question_text, user_val, correct_val, points, is_fuzzy=False, is_number=False):
        is_correct = False
        if is_number:
            try:
                if float(str(user_val).replace(',','.')) == float(correct_val): is_correct = True
            except: pass
        elif is_fuzzy:
            if check_spelling(str(user_val), str(correct_val)): is_correct = True
        else:
            if str(user_val) == str(correct_val): is_correct = True
        
        # Ajout au rapport
        report.append({
            "question": question_text,
            "user_answer": user_val,
            "correct_answer": correct_val,
            "is_correct": is_correct
        })
        return points if is_correct else 0

    # --- CALCUL DES POINTS ---
    
    # Ex 1
    score += check("Définition Volume", q1, "L'espace occupé par un objet", 1)
    score += check("Définition Masse", q2, "La quantité de matière dans un objet", 1)
    score += check("Instrument Volume", q3_vol, "Une éprouvette graduée", 1)
    score += check("Instrument Masse", q3_mas, "Une balance", 1)

    # Ex 2 (Numérique mais traité en texte tolérant pour les virgules/points)
    score += check("1,5 L en dm3", q4, "1.5", 1, is_number=True)
    score += check("350 mL en cm3", q5, "350", 1, is_number=True)
    score += check("2 kg en g", q6, "2000", 1, is_number=True)

    # Ex 3
    score += check("Nom de la courbe (liquide)", q7, "Ménisque", 1, is_fuzzy=True)
    score += check("Position oeil", q8, "En face du bas du ménisque", 2)
    score += check("Calcul Volume Pierre", q9, 18, 3, is_number=True)

    # Ex 4 (Protocole)
    user_order = [pe1, pe2, pe3, pe4, pe5]
    correct_order = st.session_state.correct_protocol
    
    # Logique spéciale pour le protocole dans le PDF
    is_proto_perfect = (user_order == correct_order)
    points_proto = 0
    if is_proto_perfect: points_proto = 4
    elif user_order[0] == correct_order[0] and user_order[2] == correct_order[2]: points_proto = 2
    
    score += points_proto
    report.append({
        "question": "Ordre du protocole",
        "user_answer": " (Voir tes choix)",
        "correct_answer": "1.Allumer, 2.Gobelet, 3.Tare, 4.Verser, 5.Lire",
        "is_correct": (points_proto == 4)
    })

    # Ex 5
    score += check("Masse 1L eau (kg)", q10, 1, 1, is_number=True)
    score += check("Masse huile vs eau", q11, "Plus léger", 1)
    score += check("Nom grandeur Masse/Volume", q12, "Masse Volumique", 1, is_fuzzy=True)

    # --- AFFICHAGE RESULTAT ---
    if score >= 10:
        st.canvas = st.balloons()
        st.success(f"Bravo {prenom} ! Note : {score} / 20")
    else:
        st.error(f"Tu as obtenu {score} / 20. Télécharge le corrigé pour comprendre tes erreurs.")

    # --- PDF ---
    if nom and prenom:
        pdf_data = create_detailed_pdf(nom, prenom, classe, score, total, report)
        st.download_button(label="📄 Télécharger ma copie corrigée et détaillée",
                           data=pdf_data,
                           file_name=f"Controle_PC_{nom}_{prenom}.pdf",
                           mime="application/pdf")
    else:
        st.warning("⚠️ Entre ton nom et prénom dans la barre latérale à gauche pour télécharger ton PDF !")