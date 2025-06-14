import pandas as pd
import numpy as np
from PyQt6.QtWidgets import QApplication, QFileDialog, QWidget
import os
import sys
import tkinter as tk
from tkinter import font


def importer_fichier():
    '''
    Description
        Cette fonction permet importer un fichier local

    Args : 
        Aucun
        
    Returns : 
        fichier(str)

    '''
    #Crée l'application Qt s'il n'y en a pas déjà une
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    #Crée une fenêtre parent (même si invisible)
    parent = QWidget()
    parent.setWindowTitle("Sélection de fichier")
    
    #Ouvre la boîte de dialogue avec la fenêtre parent
    fichier, _ = QFileDialog.getOpenFileName(
        parent,
        "Sélectionner un fichier Excel",
        r"C:\Users\alyssa.derensy\OneDrive - Groupe Limagrain Holding\RME\Sorties caisses\DATA sorties caisses\Data extraction enseignes",
        "Excel Files (*.xlsx *.xls);;All Files (*)"
    )
    #Force la fenêtre au premier plan
    parent.activateWindow()
    parent.raise_()
    
    #Nettoie la mémoire
    parent.deleteLater()
    
    return fichier

def extraire_infos(nom_fichier):
    '''
    Cette fonction permet d'extraire les informations, dont le nom de l'enseigne & la date,
    permet de minimiser les erreurs causé par les fautes de frappes par exemple.

    Args : 
        nom_fichier(str)
    
    Returns :
        date(str)
        enseigne(str)
    '''

    # Sépare la partie date et la partie enseigne
    partie_date, partie_enseigne = nom_fichier.split(' - ')
    # Extrait l'année et le mois
    annee = '20' + partie_date[:2]
    mois = partie_date[2:4]
    # Formate la date en AAAA/MM
    date = f"{annee}/{mois}"
    # Enlève l'extension du nom de l'enseigne
    enseigne = os.path.splitext(partie_enseigne)[0].lower()
        
    return date, enseigne
    
def uniformisation(gencode, code_article, volume, valeur_HT, valeur_TTC, PDV, date, enseigne) :
    '''
    Cette fonction permet d'uniformiser la structure d'un dataframe pour tous les fichiers enseignes

    Args : 
        gencode(str)
        code_article(str)
        volume(int)
        valeur_HT(float)
        valeur_TTC(float)
        PDV(str)
        date(date)
        enseigne(str)
    
    Returns :
        standardized_df(dataframe)
        standardized_df_aggregated(dataframe)
    '''
        
    # Création du dataframe
    
    standardized_df = pd.DataFrame({
     'Gencode': gencode.astype(str),
     'Code_article': code_article,
     'Volume': volume.astype(int),
     'Valeur HT': valeur_HT,
     'Valeur TTC': valeur_TTC,
     'PDV': PDV.astype(str),
     'date': date,
     'enseigne': enseigne
    })

    standardized_df['Valeur TTC'] = standardized_df['Valeur TTC'].apply(lambda x: float(x) if pd.notna(x) and x != 'NaN' else np.nan)
    standardized_df['Valeur HT'] = standardized_df['Valeur HT'].apply(lambda x: float(x) if pd.notna(x) and x != 'NaN' else np.nan)

    standardized_df["PDV"] = standardized_df["PDV"].str.replace('.0', '')

    #Suppression des 0 avant transformation
    standardized_df.drop(standardized_df[(standardized_df['Volume'] == 0) | (standardized_df['Volume'] == 0.0) | (standardized_df['Volume'].isnull())].index, inplace=True)
    
    #Permet de calculer le nb de PDV distinct
    m = standardized_df['Volume'] > 0

    #Création du dataframe agréger
    standardized_df_aggregated = standardized_df.groupby('Gencode').agg({
                                  'Code_article':'first',
                                    'Volume':'sum',
                                    'Valeur HT': 'sum',
                                    'Valeur TTC' : 'sum',
                                    'PDV' : lambda x: x[m].nunique(),
                                    'date' : 'first',
                                    'enseigne' : 'first'})
    

    
    return standardized_df, standardized_df_aggregated

def ask_validation(enseigne, date, volume, valeur):
    '''
    Fonction de sécurité permettant de donner les informations que l'utilisateur doit vérifier puis lui demandant de valider l'écriture des nouvelles données.

    Args : 
        enseigne(str)
        date(str)
        volume(int)
        valeur(float)
    
    Returns :
        response(str)
    '''

    reponse = {"valide": None}

    def choisir_oui():
        reponse["valide"] = "Oui"
        fenetre.destroy()

    def choisir_non():
        reponse["valide"] = "Non"
        fenetre.destroy()

    def test_action():
        reponse["valide"] = "Test"
        fenetre.destroy()

    def on_enter(event):
        event.widget.config(bg="#3e8e41")

    def on_leave(event):
        event.widget.config(bg="#4CAF50")

    fenetre = tk.Tk()
    fenetre.title("Validation de l'écriture")
    fenetre.configure(bg="#f0f0f0")

    custom_font = font.Font(family="Helvetica", size=12, weight="bold")
    info_font = font.Font(family="Helvetica", size=11)

    label_infos = tk.Label(fenetre, text="Veuillez vérifier les informations suivantes :", font=custom_font, bg="#f0f0f0")
    label_infos.pack(pady=(20, 10))

    
    volume_formate = f"{volume:,}".replace(",", " ")
    valeur_formatee = f"{valeur:,}".replace(",", " ")

    # Affichage des variables
    infos = [
        ("enseigne", enseigne),
        ("Date", date),
        ("volume", volume_formate),
        ("Valeur", valeur_formatee)
    ]

    for nom, valeur in infos:
        ligne = tk.Frame(fenetre, bg="#f0f0f0")
        ligne.pack(anchor="w", padx=20)
        
        label_nom = tk.Label(ligne, text=f"{nom} : ", font=custom_font, bg="#f0f0f0")
        label_nom.pack(side="left")
        
        label_valeur = tk.Label(ligne, text=str(valeur), font=info_font, bg="#f0f0f0")
        label_valeur.pack(side="left")


    label_question = tk.Label(fenetre, text="Voulez-vous valider l'écriture des données ?", font=custom_font, bg="#f0f0f0")
    label_question.pack(pady=20)

    frame_boutons = tk.Frame(fenetre, bg="#f0f0f0")
    frame_boutons.pack(pady=10)

    style_bouton = {
        "font": custom_font,
        "width": 10,
        "height": 2,
        "bg": "#4CAF50",
        "fg": "white",
        "activebackground": "#45a049",
        "bd": 0,
        "cursor": "hand2"
    }

    bouton_oui = tk.Button(frame_boutons, text="Oui", command=choisir_oui, **style_bouton)
    bouton_oui.grid(row=0, column=0, padx=10)
    bouton_oui.bind("<Enter>", on_enter)
    bouton_oui.bind("<Leave>", on_leave)

    bouton_non = tk.Button(frame_boutons, text="Non", command=choisir_non, **style_bouton)
    bouton_non.grid(row=0, column=1, padx=10)
    bouton_non.bind("<Enter>", on_enter)
    bouton_non.bind("<Leave>", on_leave)

    bouton_test = tk.Button(fenetre, text="Test", command=test_action, **style_bouton)
    bouton_test.pack(pady=10)
    bouton_test.bind("<Enter>", on_enter)
    bouton_test.bind("<Leave>", on_leave)

    fenetre.mainloop()

    return reponse["valide"]
