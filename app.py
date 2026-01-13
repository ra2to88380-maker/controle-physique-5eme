import streamlit as st
from fpdf import FPDF
import io

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Contrôle : Masse et Volume", page_icon="⚖️")

# --- FONCTION GÉNÉRATION PDF ---
def create_pdf(nom, prenom, classe, score, total, details):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Titre
    pdf.cell(200, 10, txt="Résultats du Contrôle : Masse et Volume", ln=1, align='C')
    pdf.ln(10)
    
    # Info Élève
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Nom : {nom} {prenom} | Classe : {classe}", ln=1, align='L')
    pdf.cell(200, 10, txt=f"Note obtenue : {score} / {total}", ln=1, align='L')
    pdf.line(10, 40, 200, 40)
    pdf.ln(10)
    
    # Détails
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Détail de la correction :", ln=1)
    pdf.set_font("Arial", '', 11)
    
    for item in details:
        # On nettoie un peu le texte pour éviter les erreurs d'encodage simples
        clean_text = item.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=clean_text)
        
    return pdf.output(dest='S').encode('latin-1')

# --- TITRE DE L'APPLICATION ---
st.title("⚖️ Contrôle : La Masse et le Volume")
st.markdown("Remplis ce contrôle sérieusement. Une fois terminé, clique sur **Valider** tout en bas pour voir ta note et télécharger ton PDF.")

# --- FORMULAIRE ---
with st.form("quiz_form"):
    
    # Identité
    col_id1, col_id2, col_id3 = st.columns(3)
    nom = col_id1.text_input("Nom")
    prenom = col_id2.text_input("Prénom")
    classe = col_id3.selectbox("Classe", ["5ème A", "5ème B", "5ème C", "Autre"])
    
    st.markdown("---")

    # --- EXERCICE 1 ---
    st.header("Exercice 1 : Vocabulaire et Unités (4 pts)")
    
    q1 = st.radio("1. Quelle est la définition du VOLUME ?", 
                  ["La quantité de matière dans un objet", "L'espace occupé par un objet", "Le poids de l'objet"])
    
    q2 = st.radio("2. Quelle est la définition de la MASSE ?", 
                  ["La quantité de matière dans un objet", "L'espace occupé par un objet", "La taille de l'objet"])
    
    st.markdown("**3. Complétez le tableau :**")
    c1, c2 = st.columns(2)
    q3_vol_inst = c1.selectbox("Instrument pour le VOLUME", ["Balance", "Éprouvette graduée", "Règle"])
    q3_vol_unit = c1.selectbox("Unité SI du VOLUME", ["Mètre cube (m³)", "Kilogramme (kg)", "Degré Celsius"])
    
    q3_mas_inst = c2.selectbox("Instrument pour la MASSE", ["Balance", "Éprouvette graduée", "Thermomètre"])
    q3_mas_unit = c2.selectbox("Unité SI de la MASSE", ["Mètre cube (m³)", "Kilogramme (kg)", "Newton"])

    st.markdown("---")

    # --- EXERCICE 2 ---
    st.header("Exercice 2 : Conversions (3 pts)")
    st.info("Rappel : 1 L = 1 dm³ et 1 mL = 1 cm³")
    
    c_conv1, c_conv2, c_conv3 = st.columns(3)
    q4 = c_conv1.number_input("1,5 L = ... dm³", min_value=0.0, step=0.1)
    q5 = c_conv2.number_input("350 mL = ... cm³", min_value=0, step=1)
    q6 = c_conv3.number_input("2 kg = ... g", min_value=0, step=10)

    st.markdown("---")

    # --- EXERCICE 3 ---
    st.header("Exercice 3 : Mesures (6 pts)")
    
    st.subheader("A. Le liquide")
    q7 = st.selectbox("1. Quel instrument est le plus précis pour mesurer un liquide ?", ["Le bécher", "Le verre à pied", "L'éprouvette graduée"])
    q8 = st.text_input("2. Comment s'appelle la courbe formée par la surface du liquide ? (Un seul mot)").strip().lower()
    q9 = st.radio("3. Pour lire le volume, il faut regarder :", ["Le haut de la courbe", "Le bas de la courbe"])
    
    st.subheader("B. Le solide (Déplacement d'eau)")
    st.write("Léa met 30 mL d'eau (V1). Elle ajoute une pierre, le niveau monte à 48 mL (V2).")
    q10 = st.number_input("Quel est le volume de la pierre en mL ?", min_value=0, step=1)

    st.markdown("---")

    # --- EXERCICE 4 ---
    st.header("Exercice 4 : Le Protocole (4 pts)")
    st.write("Remets les étapes pour peser 50g de sable dans l'ordre (de 1 à 5).")
    
    etapes_possibles = [
        "Allumer la balance",
        "Poser le gobelet vide",
        "Appuyer sur TARE",
        "Verser le sable jusqu'à 50g",
        "Lire la valeur affichée"
    ]
    
    e1 = st.selectbox("Étape 1", etapes_possibles, key="e1")
    e2 = st.selectbox("Étape 2", etapes_possibles, key="e2")
    e3 = st.selectbox("Étape 3", etapes_possibles, key="e3")
    e4 = st.selectbox("Étape 4", etapes_possibles, key="e4")
    e5 = st.selectbox("Étape 5", etapes_possibles, key="e5")

    st.markdown("---")

    # --- EXERCICE 5 ---
    st.header("Exercice 5 : Comprendre la matière (3 pts)")
    q11 = st.number_input("1. Quelle est la masse d'un Litre d'eau (en kg) ?", min_value=0.0, step=0.1)
    q12 = st.radio("2. Un litre d'huile est-il plus lourd ou plus léger qu'un litre d'eau ?", ["Plus lourd", "Plus léger", "Pareil"])
    q13 = st.text_input("3. Comment s'appelle la grandeur qui lie la masse et le volume ? (2 mots)").strip().lower()

    # --- BOUTON DE VALIDATION ---
    submitted = st.form_submit_button("VALIDER MA COPIE")

# --- TRAITEMENT DES RÉSULTATS ---
if submitted:
    score = 0
    total_points = 20
    correction_details = []

    # Correction Ex 1
    if q1 == "L'espace occupé par un objet": score += 1
    else: correction_details.append("- Ex 1.1 : Faux. Le volume est l'espace occupé.")
    
    if q2 == "La quantité de matière dans un objet": score += 1
    else: correction_details.append("- Ex 1.2 : Faux. La masse est la quantité de matière.")
    
    if q3_vol_inst == "Éprouvette graduée" and q3_vol_unit == "Mètre cube (m³)": score += 1
    else: correction_details.append("- Ex 1.3 (Vol) : Faux. On mesure le volume en m³ avec une éprouvette.")
    
    if q3_mas_inst == "Balance" and q3_mas_unit == "Kilogramme (kg)": score += 1
    else: correction_details.append("- Ex 1.3 (Masse) : Faux. On mesure la masse en kg avec une balance.")

    # Correction Ex 2
    if q4 == 1.5: score += 1
    else: correction_details.append(f"- Ex 2.1 : Faux. 1,5 L = 1,5 dm³.")
    
    if q5 == 350: score += 1
    else: correction_details.append(f"- Ex 2.2 : Faux. 350 mL = 350 cm³.")
    
    if q6 == 2000: score += 1
    else: correction_details.append(f"- Ex 2.3 : Faux. 2 kg = 2000 g.")

    # Correction Ex 3
    if q7 == "L'éprouvette graduée": score += 1
    else: correction_details.append("- Ex 3.1 : L'éprouvette est plus précise que le bécher.")
    
    if "nisque" in q8: score += 1 # Tolérance orthographique pour ménisque
    else: correction_details.append(f"- Ex 3.2 : La courbe s'appelle le ménisque.")
    
    if q9 == "Le bas de la courbe": score += 1
    else: correction_details.append("- Ex 3.3 : Il faut lire le bas du ménisque.")
    
    if q10 == 18: score += 3
    else: correction_details.append(f"- Ex 3 (Calcul) : Faux. 48 - 30 = 18 mL.")

    # Correction Ex 4 (Ordre strict)
    ordre_correct = ["Allumer la balance", "Poser le gobelet vide", "Appuyer sur TARE", "Verser le sable jusqu'à 50g", "Lire la valeur affichée"]
    user_ordre = [e1, e2, e3, e4, e5]
    if user_ordre == ordre_correct:
        score += 4
    elif user_ordre[0] == ordre_correct[0] and user_ordre[2] == ordre_correct[2]: # Si au moins allumage et tare sont bons
        score += 2
        correction_details.append("- Ex 4 : L'ordre n'est pas tout à fait exact (2/4).")
    else:
        correction_details.append("- Ex 4 : L'ordre du protocole est incorrect.")

    # Correction Ex 5
    if q11 == 1.0: score += 1
    else: correction_details.append("- Ex 5.1 : 1 L d'eau pèse exactement 1 kg.")
    
    if q12 == "Plus léger": score += 1
    else: correction_details.append("- Ex 5.2 : L'huile flotte, elle est plus légère.")
    
    if "masse volumique" in q13: score += 1
    else: correction_details.append("- Ex 5.3 : C'est la masse volumique.")

    # --- AFFICHAGE RÉSULTAT ---
    st.balloons()
    st.success(f"Terminé ! Note : {score} / {total_points}")
    
    if score < 10:
        st.warning("Attention, il y a plusieurs erreurs. Regarde le PDF pour comprendre.")
    else:
        st.info("Bon travail !")

    # --- GÉNÉRATION DU PDF ---
    pdf_bytes = create_pdf(nom, prenom, classe, score, total_points, correction_details)
    
    st.download_button(
        label="📄 Télécharger mon Contrôle Corrigé (PDF)",
        data=pdf_bytes,
        file_name=f"Controle_Physique_{nom}_{prenom}.pdf",
        mime="application/pdf"
    )