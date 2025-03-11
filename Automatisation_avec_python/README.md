# Transformateur de Données de Ventes

## Description
Cet algorithme automatise la transformation des fichiers bruts de données de ventes en un format standardisé. Le programme extrait les informations clés (Enseigne, date) à partir du nom du fichier, applique des transformations spécifiques selon l'enseigne concernée, et structure les données dans un format uniforme.

## Fonctionnalités
- Importation de fichiers via interface graphique (PyQt6)
- Extraction automatique des métadonnées (Enseigne, date) depuis le nom de fichier
- Transformation des données selon des règles spécifiques à chaque enseigne
- Vérification de la qualité des données (contrôle des totaux)
- Export dans un format standardisé

## Prérequis
```python
import pandas as pd 
import numpy as np 
from datetime import datetime
import csv
import os
import sys
from PyQt6.QtWidgets import QApplication, QFileDialog, QWidget
import tkinter as tk
from tkinter import filedialog
```

## Structure des données standardisées

| Gencode | Volume | Valeur HT | Valeur TTC | PDV | Date | Enseigne |
|---------|--------|-----------|------------|-----|------|----------|
| XXXXXXX |  100   |  1200.50  |  1440.60   |  10 | YYYY-MM-DD |  ABC123  |


## Utilisation
1. Lancez le programme
2. Sélectionnez les fichiers bruts à traiter via l'interface graphique
3. Le programme traite automatiquement les fichiers selon l'enseigne détectée
4. Les données transformées sont ajoutées au fichier "verification.csv"

## Processus de transformation
1. **Importation** : Lecture du fichier brut 
2. **Extraction des métadonnées** : Identification de l'enseigne et de la date à partir du nom du fichier
3. **Transformation** : Application des règles spécifiques à l'enseigne identifiée
4. **Structuration** : Mise en forme des données selon le schéma standardisé
5. **Vérification** : Contrôle de l'intégrité des données (somme des volumes et chiffres d'affaires)
6. **Export** : Ajout des données transformées au fichier de sortie

## Mécanisme de vérification
Le programme vérifie l'intégrité des données en comparant :
- La somme des volumes dans le fichier original vs. le fichier transformé
- La somme des valeurs (chiffre d'affaires) dans le fichier original vs. le fichier transformé

## Format de sortie
Les données sont exportées au format CSV avec les paramètres suivants :
- Séparateur : point-virgule (;)
- Décimal : virgule (,)
- Valeurs textuelles : entourées de guillemets (QUOTE_NONNUMERIC)
- Mode d'écriture : append (ajout à un fichier existant)