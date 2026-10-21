# TP — Tickets techniques : contacts, codes et versions

## Description

Ce projet réalise le prétraitement de 12 tickets techniques en Python.

L'objectif est de masquer les informations de contact ciblées sans supprimer les codes techniques, les versions, les montants et les autres valeurs utiles.

## Objectifs du TP

- Inspecter les 12 tickets.
- Identifier les emails, téléphones, URLs, codes, versions et montants.
- Repérer les doublons potentiels et les textes vides.
- Masquer les contacts avec des marqueurs.
- Effectuer une tokenisation métier avec une expression régulière.
- Appliquer le stemming et la lemmatisation aux mots ordinaires.
- Protéger les marqueurs et les valeurs techniques.
- Construire une clé de doublon avant le masquage.
- Exporter les résultats dans un fichier CSV.

## Méthodes utilisées

| Méthode | Description |
|---|---|
| Inspection | Analyse des tickets bruts |
| Normalisation | Création d'une clé de comparaison |
| Masquage | Remplacement des contacts ciblés |
| Tokenisation | Découpage du texte en tokens métier |
| Filtrage | Protection des informations techniques |
| Stemming | Réduction des mots à leur racine |
| Lemmatisation | Recherche de la forme de base des mots |
| Détection de doublons | Regroupement des clés identiques |
| Exportation | Création d'un tableau CSV |

## Marqueurs de masquage

- `EMAILTOKEN` : email
- `PHONETOKEN` : téléphone ciblé
- `URLTOKEN` : adresse URL

Le téléphone est masqué uniquement lorsqu'il est composé de 10 chiffres et suit `tel :`.

Les autres chiffres sont conservés.

## Informations techniques protégées

Le programme conserve notamment :

- Les codes : `E404`, `E403`
- Les versions : `3.11`, `2.1`
- Le montant : `150 DH`
- L'heure : `08:30`

## Détection des doublons

Les tickets B01 et B08 sont des doublons potentiels.

Le ticket B09 contient une chaîne vide et est signalé séparément.

## Installation

Installer les dépendances :

```bash
pip install -r requirements.txt
python -m spacy download fr_core_news_sm
```

## Exécution

```bash
python tp_tickets.py
```

Le programme affiche le tableau des résultats et le bilan final.

Il génère également le fichier :

`resultats_tickets.csv`

## Résultats exportés

Le CSV contient les colonnes suivantes :

- `id`
- `brut`
- `texte_masque`
- `tokens`
- `formes`
- `stems`
- `lemmes`
- `cle_avant_masquage`
- `groupe_doublon`

## Bilan

Le programme calcule automatiquement :

- Le nombre de mots avant traitement
- Le nombre de tokens après traitement
- Le nombre de doublons à retirer
- Le nombre de tokens après dédoublonnage
- Les identifiants des tickets vides

Le nombre de mots bruts et le nombre de tokens ne sont pas directement équivalents, car ils sont calculés avec deux méthodes différentes.

## Technologies

- Python
- Expressions régulières (`re`)
- NLTK
- spaCy
- pandas
