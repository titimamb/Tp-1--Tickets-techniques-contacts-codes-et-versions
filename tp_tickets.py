
import re
import pandas as pd
import spacy
from nltk.stem.snowball import SnowballStemmer

# Initialisation des outils français
nlp = spacy.load("fr_core_news_sm")
stemmer = SnowballStemmer("french")

# Les 12 tickets
tickets = [
    {"id": "B01", "text_raw": "Erreur E404 sur Python 3.11."},
    {"id": "B02", "text_raw": "Contact : lina@example.test ; tel : 0612345678 ; erreur E404."},
    {"id": "B03", "text_raw": "Le paiement de 150 DH ne passe pas."},
    {"id": "B04", "text_raw": "Les connexions échouent depuis la mise à jour."},
    {"id": "B05", "text_raw": "Le service ne fonctionne plus."},
    {"id": "B06", "text_raw": "Message E403 ; version 2.1."},
    {"id": "B07", "text_raw": "Documentation https://exemple.test/aide"},
    {"id": "B08", "text_raw": " ERREUR E404 SUR PYTHON 3.11. "},
    {"id": "B09", "text_raw": ""},
    {"id": "B10", "text_raw": "Les fichiers sont supprimés après fermeture."},
    {"id": "B11", "text_raw": "Tel : 0712345678 ; contact : sami@example.test."},
    {"id": "B12", "text_raw": "Échec sur l’application à 08:30."}
]

# 1. Clé de doublon créée AVANT le masquage
def creer_cle(texte):
    texte = texte.lower().strip()
    texte = re.sub(r"[^\w\s]", " ", texte)
    texte = re.sub(r"\s+", " ", texte)
    return texte.strip()

# 2. Masquage des contacts
def masquer(texte):
    # Emails
    texte = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "EMAILTOKEN", texte
    )

    # URLs
    texte = re.sub(
        r"https?://\S+|www\.\S+",
        "URLTOKEN", texte
    )

    # Téléphone : 10 chiffres uniquement après "tel :"
    texte = re.sub(
        r"(?i)(\btel\s*:\s*)\d{10}\b",
        r"\1PHONETOKEN", texte
    )

    return texte

# 3. Motif du tokenizer métier
motif = (
    r"EMAILTOKEN|PHONETOKEN|URLTOKEN|"
    r"E\d+|\d+\.\d+|\d{1,2}:\d{2}|\d+|"
    r"[a-zA-ZÀ-ÿ]+"
)

# 4. Vérifier si un token doit être protégé
def est_protege(token):
    return (
        token.upper() in [
            "EMAILTOKEN", "PHONETOKEN", "URLTOKEN", "DH"
        ]
        or re.fullmatch(r"E\d+", token, re.IGNORECASE)
        or re.fullmatch(r"\d+\.\d+", token)
        or re.fullmatch(r"\d{1,2}:\d{2}", token)
        or re.fullmatch(r"\d+", token)
    )

# 5. Prétraitement des tickets
resultats = []

for ticket in tickets:
    brut = ticket["text_raw"]

    # Clé avant masquage
    cle = creer_cle(brut)

    # Masquage
    texte_masque = masquer(brut)

    # Tokenisation
    tokens = re.findall(motif, texte_masque, re.IGNORECASE)

    formes = []
    stems = []
    lemmes = []

    for token in tokens:
        if est_protege(token):
            # Protéger les marqueurs et valeurs techniques
            formes.append(token)
            stems.append(token)
            lemmes.append(token)
        else:
            mot = token.lower()
            formes.append(mot)

            # Stemming
            stems.append(stemmer.stem(mot))

            # Lemmatisation
            doc = nlp(mot)
            lemmes.append(doc[0].lemma_)

    resultats.append({
        "id": ticket["id"],
        "brut": brut,
        "texte_masque": texte_masque,
        "tokens": " | ".join(tokens),
        "formes": " | ".join(formes),
        "stems": " | ".join(stems),
        "lemmes": " | ".join(lemmes),
        "cle_avant_masquage": cle
    })

# 6. Détection des doublons
groupes = {}

for resultat in resultats:
    cle = resultat["cle_avant_masquage"]

    if cle != "":
        if cle not in groupes:
            groupes[cle] = []
        groupes[cle].append(resultat["id"])

for resultat in resultats:
    ids = groupes.get(resultat["cle_avant_masquage"], [])

    if len(ids) > 1:
        resultat["groupe_doublon"] = ", ".join(ids)
    else:
        resultat["groupe_doublon"] = "Aucun"

# 7. Compter les mots et les tokens
mots_avant = sum(
    len(ticket["text_raw"].split())
    for ticket in tickets
)

tokens_apres = sum(
    len(r["tokens"].split(" | ")) if r["tokens"] else 0
    for r in resultats
)

# Un seul ticket conservé par groupe de doublons
cles_vues = set()
doublons = []

for resultat in resultats:
    cle = resultat["cle_avant_masquage"]

    if cle != "":
        if cle in cles_vues:
            doublons.append(resultat["id"])
        else:
            cles_vues.add(cle)

tokens_sans_doublons = sum(
    len(r["tokens"].split(" | ")) if r["tokens"] else 0
    for r in resultats
    if r["id"] not in doublons
)

# 8. Exporter le tableau CSV
df = pd.DataFrame(resultats)
df.to_csv("resultats_tickets.csv", index=False, encoding="utf-8-sig")

# 9. Afficher le bilan
print("\n===== RÉSULTATS =====")
print(df.to_string(index=False))

print("\n===== BILAN FINAL =====")
print("Nombre de mots avant traitement :", mots_avant)
print("Nombre de tokens après traitement :", tokens_apres)
print("Nombre de doublons à retirer :", len(doublons))
print("Tickets doublons :", doublons)
print("Tokens après suppression des doublons :", tokens_sans_doublons)

vides = [
    t["id"] for t in tickets
    if t["text_raw"].strip() == ""
]
print("Tickets vides :", vides)

print("\nFichier créé : resultats_tickets.csv")
