# Documentation - Traitement automatisé des données data-sharing

## Introduction

Ce projet a pour objectif de standardiser et d'automatiser le traitement de fichiers de ventes issus de différentes enseignes. Il permet de transformer des fichiers Excel hétérogènes en un format structuré et homogène, prêt à être utilisé pour des analyses ou des tableaux de bord (via Power BI).

Le traitement est réalisé à l’aide d’un notebook Jupyter (`Algorithme - Ventes.ipynb`) qui s’appuie sur un module Python (`utils.py`) contenant les fonctions utilitaires, un module python (`transformation.py`) contenant la fonction de transformation des données, un module python (`verification.py`) contenant la fonction de vérification de l'intégrité des données puis un module python (`exportation.py`) contenant la fonction pour exporter les données vers un ou plusieurs fichiers csv.

---

## Structure

``` 
Power Bi/ 
├── src/ 
│ ├── __init__.py 
| ├── utils.py 
| ├── transformation.py
| ├── exportation.py
│ └── verification.py
├──Notebook/
|  ├── Algorithme - Ventes.ipynb 
|  └── Algorithme - Stock.ipynb 
├──data/
|   ├──output/
|   |   ├── data.csv 
│   |   ├── adeo.csv 
│   |   ├── gammvert.csv 
│   |   ├── bricomarche.csv 
│   |   ├── jardin.csv 
│   |   └── carrefour.csv 
|   ├──input/
``` 


## Architecture du traitement

1. **Sélection du fichier source** via une interface graphique.
2. **Extraction automatique** de la date et du nom de l’enseigne à partir du nom du fichier.
3. **Chargement des fichiers de référence** (articles, magasins).
4. **Nettoyage et transformation** des données selon l’enseigne.
5. **Uniformisation** des colonnes dans une structure commune.
6. **Agrégation** des données par Gencode.
7. **Vérification d’intégrité** (volume et chiffre d’affaires).
8. **Exportation** des résultats dans des fichiers CSV.

---

## Contenu du projet
- `Notebook/` : Dossier contenant les notebooks Jupyter.
    - `Algorithme - Ventes.ipynb` : Notebook principal contenant le pipeline de traitement pour les ventes.
    - `Algorithme - Stock.ipynb` : Notebook principal contenant le pipeline de traitement pour les stocks.
- `src/` : Dossier contenant algorithmes pythons.
    - `utils.py` : Module contenant les fonctions utilitaires.
    - `transformation.py` : Module contenant les fonctions utilitaires.
    - `exportation.py` : Module contenant la fonction pour exporter les données.
    - `verification.py` : Module contenant les fonctions utilitaires.
- `data/` : Dossier contenant les fichiers données.
    - `output/` : Dossier contenant les fichiers data de sortie.
        - `adeo.csv` : Fichier de sortie des enseigne : `Leroy Merlin`, `Weldom` & `Castorama`
        - `bricomarche.csv` : Fichier de sortie de l'enseigne `Bricomarché`.
        - `carrefour.csv` : Fichier de sortie de l'enseigne `Carrefour`.
        - `data.csv` : Fichier de sortie agrégé.
        - `gammvert.csv` : Fichier de sortie de l'enseigne `Gammvert`.
        - `jardin.csv` : Fichier de sortie des enseigne : `Botanic`, `Jardiland`, `Truffaut` & `Sevea`.

---

## Détail des fonctions (`utils.py`)

### `importer_fichier()`
Ouvre une boîte de dialogue pour sélectionner un fichier Excel local.

- **Retour** : chemin du fichier sélectionné (`str`)

### `extraire_infos()`
Extrait la date (au format `AAAA/MM`) et le nom de l’enseigne à partir du nom du fichier.

- **Paramètre** : nom du fichier (`str`)
- **Retour** : `date (str)`, `enseigne (str)`

### `uniformisation()`
Crée un DataFrame standardisé avec les colonnes suivantes : `gencode`, `code_article`, `volume`, `valeur_HT`, `valeur_TTC`, `PDV`, `date`, `enseigne`.

- **Paramètres** : colonnes sources, date, enseigne
- **Retour** : `standardized_df` (DataFrame), `standardized_df_aggregated` (DataFrame), 


---

## Détail des fonctions (`transformation.py`)

### `transformation()`
Transforme les données bruts puis crée deux DataFrame. Un avec les données agrégés, un autre avec les données par magasins.

- **Paramètre** : `df_brut`(DataFrame), colonnes sources
- **Retour** : `df_clean`(DataFrame), `df_brut`(DataFrame)

### `case_uniformisation()`
Switch d'uniformisation de la structure des données

- **Paramètre** : `enseigne`(DataFrame), `df_clean`(DataFrame),`date`(str),`annee`(str),`last_month_df`(DataFrame)
- **Retour** : `standardized_df`(DataFrame), `standardized_df_aggregated`(DataFrame)

---

## Détail des fonctions (`exportation.py`)

### `output()`
Fonction qui permet à l'utilisateur de vérifier les informations puis d'accepter, ou non, l'écriture des données.

- **Paramètre** : `df`(DataFrame), `enseigne`(str)

---

## Détail des fonctions (`verification.py`)

### `verifier_integrite_donnees()`
Fonction qui permet de vérifier l'intégrité des données en utilisant l'aggrégation de la colonne Volume ET Valeur.

- **Paramètre** : `df_agregee`(DataFrame), `df_magasin`(DataFrame), `df_brut`(DataFrame), `colonnes sources`, `merged_df`(DataFrame)

---

## Format attendu des fichiers

Le nom du fichier doit suivre le format suivant :


```
AAMM - {Enseigne}.xlsx
```

Exemple : `2405 - Leroy.xlsx` pour un fichier de mai 2024.

---

## Lancement

1. Ouvrir le fichier `Algorithme - Ventes.ipynb` dans Jupyter Notebook ou VSCode avec l'extension Jupyter.
2. Exécuter les cellules dans l’ordre.
3. Une fenêtre s’ouvrira pour sélectionner un fichier Excel à traiter.
4. Le script extraira automatiquement la date et l’enseigne à partir du nom du fichier.
5. À la fin du traitement, valider l’exportation en saisissant `Oui` ou `Test` dans la console.

---

## Résultats attendus

- `data.csv` : fichier agrégé contenant les ventes consolidées.
- `{enseigne}.csv` : fichiers détaillés par enseigne, ajoutés automatiquement selon les règles définies.

---

## Personnalisation et extension

- **Ajouter une nouvelle enseigne** : ajouter un nouveau bloc `case` dans les sections `match Enseigne` du notebook.
- **Modifier les chemins de fichiers** : adapter les chemins vers les fichiers SharePoint dans les cellules concernées.
- **Ajouter des colonnes ou métriques** : modifier la fonction `uniformisation()` dans `utils.py` pour inclure de nouveaux champs.

---

## Exemples d’utilisation

### Exemple 1 : Traitement d’un fichier Leroy Merlin

Nom du fichier : `2405 - leroy.xlsx`

- Le script détecte automatiquement l’enseigne `leroy` et la date `2024/05`.
- Il applique les règles de nettoyage spécifiques à Leroy Merlin.
- Il exporte les résultats dans `data/output/data.csv` et `data/output/adeo.csv`.

### Exemple 2 : Traitement d’un fichier Amazon

Nom du fichier : `2404 - amazon.xlsx`

- Le script détecte l’enseigne `amazon` et la date `2024/04`.
- Il applique les règles de transformation propres à Amazon.
- Les données sont exportées dans `data/output/data.csv` uniquement (pas de fichier magasin).

---

## Remarques

- Le fichier `fonction.py` doit être dans le même dossier que le notebook pour que l'import fonctionne correctement.
- Le script s’arrête automatiquement si des erreurs critiques sont détectées (ex. : données manquantes, incohérences).
- Le traitement est conçu pour être relancé chaque mois avec un nouveau fichier de ventes.

