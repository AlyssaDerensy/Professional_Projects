import pandas as pd
import numpy as np

#from src.utils import importer_fichier
from src.utils import uniformisation

def transformation(df_brut, table_article, table_magasin, enseigne, date) :
    """
    Description
        Fonction permettant d'effectuer la transformation des dataframes selon l'enseigne de provenance.

    Args : 

        df_brut(DataFrame)
        table_article(DataFrame)
        table_magasin(DataFrame)
        enseigne(str)
        date(date)
        
    Returns : 
        df_clean(DataFrame)
        df_brut(DataFrame)

    """
    match enseigne :
        case "bricomarche" :
            df_clean = df_brut.copy()
            
            #Supprime la ligne Totaux
            df_clean = df_clean.dropna(subset=['EAN13'])
                            
        case 'botanic' :
            df_clean = df_brut.copy()

            df_clean = df_clean.dropna(subset = ['Référence'])
            df_clean['Référence'] = df_clean['Référence'].astype(str)
            df_clean['Référence'] = df_clean['Référence'].str.replace('.0','')
            df_clean['Référence'] = df_clean['Référence'].str.upper()

            df_clean = pd.merge(df_clean, table_article, left_on='Référence', right_on="Code table_article", how='left')

            magasin_filtre = table_magasin.loc[table_magasin['id_enseigne'] == 'BTN']
            
            df_clean['Code Mag'] = df_clean['Code Mag'].astype(str)

            df_clean = pd.merge(df_clean, magasin_filtre, left_on='Code Mag', right_on="Code enseigne", how='inner', indicator= True)

        case 'gammvert' :
            df_brut['CA HT'] = df_brut['CA HT'].astype(str)
            df_brut['CA HT'] = df_brut['CA HT'].str.replace('\u00A0', '')
            df_brut['CA HT'] = df_brut['CA HT'].str.replace(' ', '')
            df_brut['CA HT'] = df_brut['CA HT'].str.replace('€', '')
            df_brut['CA HT'] = df_brut['CA HT'].str.replace(',', '.')

            df_brut['CA HT'] = df_brut['CA HT'].astype(float)
            

            if pd.isna(df_brut.iloc[0]['EAN table_article']) or df_brut.iloc[0]['EAN table_article'] == '':
                df_brut = df_brut.drop(df_brut.index[0])


            df_clean = df_brut.copy()

            df_clean['GLN table_magasin'] = df_clean["GLN table_magasin"].astype(str).str.replace('.0', '')
            df_clean = df_clean.dropna(subset = ['EAN table_article'])
            
        case 'sevea' :
            df_clean = df_brut.copy()

            magasin_filtre = table_magasin.loc[table_magasin['id_enseigne'] == 'VV']
            magasin_filtre['table_magasin'] = magasin_filtre['Code enseigne'].astype(str)
            
            df_clean = pd.merge(df_clean, magasin_filtre, left_on='table_magasin', right_on="Code enseigne", how='left', indicator= True)
        
        case 'leroy' :
            df_brut['Quantité vendue'] = df_brut['Quantité vendue'].fillna(0)
            df_brut['Ventes - montant'] = df_brut['Ventes - montant'].fillna(0)

            df_clean = df_brut.copy()


            magasin_filtre = table_magasin.loc[table_magasin['id_enseigne'] == 'LM']
            
            df_clean['Identifiant table_magasin/entrepôt'] = df_clean['Identifiant table_magasin/entrepôt'].astype(str)

            df_clean = pd.merge(df_clean, magasin_filtre, left_on='Identifiant table_magasin/entrepôt', right_on="Code enseigne", how='left', indicator= True)    

        case 'leroy es' | 'leroy portugal' :
            df_brut['Quantité vendue'] = df_brut['Quantité vendue'].fillna(0)
            df_brut['Ventes - montant'] = df_brut['Ventes - montant'].fillna(0)
            
            df_clean = df_brut.copy()
        
        case 'truffaut' :
            df_brut["Qté vendue"] = df_brut["Qté vendue"].fillna(0)
            df_brut["CA TTC vendu"] = df_brut["CA TTC vendu"].fillna(0)
            df_brut.dropna(subset = 'Libellé',inplace = True)

            df_clean = df_brut.copy()

            magasin_filtre = table_magasin.loc[table_magasin['id_enseigne'] == 'TFT']

            df_clean.dropna(subset = 'Qté vendue',inplace = True)
            
            df_clean['Qté vendue'] = df_clean['Qté vendue'].astype(float).round().astype(int)
            df_clean = pd.merge(df_clean, magasin_filtre, left_on='table_magasin', right_on="Nom table_magasin enseigne", how='left', indicator= True)

            
            df_clean.drop(df_clean[(df_clean['EAN'] == 0)].index,inplace = True)
            
        case 'jardiland' :

            df_brut.drop(df_brut.index[0], inplace=True)
            df_brut.drop(df_brut.index[0], inplace=True)

            df_brut['CA HT N'] = df_brut['CA HT N'].astype(str)
            df_brut['CA HT N'] = df_brut['CA HT N'].str.replace('\u00A0','')
            df_brut['CA HT N'] = df_brut['CA HT N'].str.replace('€','')
            df_brut['CA HT N'] = df_brut['CA HT N'].str.replace(',','.')
            df_brut['CA HT N'] = df_brut['CA HT N'].astype(float)

            df_clean = df_brut.copy()
            
            magasin_filtre = table_magasin.loc[table_magasin['id_enseigne'] == 'JDL']

            df_clean['Code MAG'] = df_clean['Code MAG'].astype(str)
            df_clean['Code MAG'] = df_clean['Code MAG'].str.replace('.0','')
            
            df_clean = pd.merge(df_clean, magasin_filtre, left_on='Code MAG', right_on="Code enseigne", how='left')
            
        case 'castorama' :
            df_brut['Quantités'] = df_brut['Quantités'].fillna(0)
            
            df_clean = df_brut.copy()

            magasin_filtre = table_magasin.loc[table_magasin['id_enseigne'] == 'CASTO']
            
            df_clean['table_magasin'] = df_clean['table_magasin'].astype(str)
            table_magasin['id_enseigne'] = table_magasin['id_enseigne'].astype(str)

            df_clean = pd.merge(df_clean, magasin_filtre, left_on='table_magasin', right_on="Code enseigne", how='left', indicator= True)
            
        case 'weldom' :
            df_brut.columns = df_brut.iloc[0]
            df_brut.drop(df_brut.index[:1], inplace=True)
            df_brut.reset_index(drop = True, inplace = True)

            df_brut["Qtt"] = df_brut["Qtt"].fillna(0)
            df_brut["CA TTC"] = df_brut["CA TTC"].fillna(0)

            df_clean = df_brut.copy()

            df_clean.dropna(subset = ['EAN'], inplace = True)
            df_clean.dropna(subset = ['Qtt'], inplace = True)
            
            df_clean['CA TTC'] = df_clean['CA TTC'].astype(str)
            df_clean['Qtt'] = df_clean['Qtt'].astype(str)
            df_clean['CA TTC'] = df_clean['CA TTC'].str.replace(',','.')
            df_clean['Qtt'] = df_clean['Qtt'].str.replace(',','.')
            df_clean['CA TTC'] = df_clean['CA TTC'].astype(float)
            df_clean['Qtt'] = df_clean['Qtt'].astype(float).round().astype(int)

            df_clean['Cque'] = df_clean['Cque'].astype(str)
            
            magasin_filtre = table_magasin.loc[table_magasin['id_enseigne'] == 'WD']
            df_clean = pd.merge(df_clean, magasin_filtre, left_on='Cque', right_on="Code enseigne", how='left')
            
        case 'crf hyper' | 'crf super':
            df_brut.columns = df_brut.columns.str.replace('"', '')
            df_brut.columns = df_brut.columns.str.replace('�', 'é')

            df_brut = df_brut.applymap(lambda x: x.replace('"', '') if isinstance(x, str) else x)

            df_brut['Qtés UVC ou UCT'] = df_brut['Qtés UVC ou UCT'].fillna(0)
            df_brut['CA TTC'] = df_brut['CA TTC'].fillna(0)
            
            df_brut.drop(df_brut[(df_brut['Magasins'] == "Total Magasins") | (df_brut['Magasins'] == "Total magasins")].index,inplace = True)
            df_brut.drop(df_brut[(df_brut['EAN'] == "Total table_magasin")].index,inplace = True)
            df_brut.dropna(subset = ['EAN','Magasins'], inplace = True)

            df_clean = df_brut.copy()

            df_clean['Ean13lfd'] = df_clean['Ean13lfd'].astype(str)
            df_clean = pd.merge(df_clean, table_magasin, left_on='Ean13lfd', right_on="GLN", how='left')

        case 'system u' :
            df_brut.columns = df_brut.iloc[1]
            df_brut.drop(df_brut.index[:3], inplace=True)

            df_brut["Nb d\'UVC vendus"] = df_brut["Nb d\'UVC vendus"].fillna(0)

            df_clean = df_brut.copy()

            df_clean.dropna(subset = ["Nb d'UVC vendus"], inplace = True)
        
        case 'amazon' :
            df_brut.columns = df_brut.iloc[0]

            df_brut.dropna(subset = ['Unités expédiées'], inplace = True)
            df_brut.drop(df_brut.index[0], inplace=True)
            
            df_brut['Chiffre d’affaires basé sur les expéditions'] = df_brut['Chiffre d’affaires basé sur les expéditions'].astype(str)
            df_brut['Chiffre d’affaires basé sur les expéditions'] = df_brut['Chiffre d’affaires basé ' 
                                                                    'sur les expéditions'].str.replace('\u00A0','')
            df_brut['Chiffre d’affaires basé sur les expéditions'] = df_brut['Chiffre d’affaires basé ' 
                                                                        'sur les expéditions'].str.replace('€','')
            df_brut['Chiffre d’affaires basé sur les expéditions'] = df_brut['Chiffre d’affaires ' 
                                                                    'basé sur les expéditions'].str.replace(',', '.')
            df_brut['Chiffre d’affaires basé sur les expéditions'] = df_brut['Chiffre d’affaires basé ' 
                                                                    'sur les expéditions'].str.replace('\u202F','')
            df_brut['Chiffre d’affaires basé sur les expéditions'] = df_brut['Chiffre d’affaires basé '
                                                                    'sur les expéditions'].str.replace(' ','')
            df_brut['Chiffre d’affaires basé sur les expéditions'] = df_brut['Chiffre d’affaires basé sur les expéditions'].astype(float)
            

            
            df_brut['Unités expédiées'] = df_brut['Unités expédiées'].astype(str)
            df_brut['Unités expédiées'] = df_brut['Unités expédiées'].str.replace('\u00A0', '')
            df_brut['Unités expédiées'] = df_brut['Unités expédiées'].str.replace('\u202F', '')

            
            df_brut['Unités expédiées'] = df_brut['Unités expédiées'].astype(float)
            df_clean = df_brut.copy()

        case 'cdiscount' : 
            
            if df_brut.columns[1] == "Unnamed: 1":

                df_brut.columns = df_brut.iloc[2]
                df_brut.drop(df_brut.index[:3], inplace=True)
                df_brut.reset_index(drop = True, inplace = True)

            df_clean = df_brut.copy()
            df_clean.drop(df_clean[(df_clean['Nombre de commandes'] == 0)].index,inplace = True)
        
        case 'vilmorin' :

            df_clean = df_brut.copy()

            df_clean['SKU'] = df_clean['SKU'].astype(str)

            df_clean['Nom de la marketplace'].fillna('MKTP VJ', inplace=True)
            
            df_clean = pd.merge(df_clean, table_article, left_on='SKU', right_on="Code table_article", how='left')

        case _ :
            raise SystemExit("enseigne non référencée")

 
    return df_clean, df_brut

def case_uniformisation(enseigne,df_clean,date,annee,last_month_df) :
    
    match enseigne :
        case 'bricomarche' :
            standardized_df,standardized_df_aggregated = uniformisation(df_clean['EAN13'],np.nan,df_clean['Qté Vendue Période N'],np.nan,df_clean['CATTC Vendue Période N'],df_clean['PDV'],date,'BCM')
            
        case 'botanic' :
            standardized_df, standardized_df_aggregated = uniformisation(df_clean['EAN'],df_clean['Référence'],df_clean['Qté.'],np.nan,np.nan, df_clean['code nielsen'],date,"BTN")
            standardized_df_aggregated['Code_article'] =  standardized_df_aggregated['Code_article'].str.replace('.0','')
        
        case 'gammvert' :
            standardized_df, standardized_df_aggregated = uniformisation(df_clean['EAN table_article'],np.nan,df_clean['Quantité Vente'],df_clean['CA HT'],np.nan, df_clean['GLN table_magasin'],date,"GV")

        case 'sevea' :
            standardized_df, standardized_df_aggregated = uniformisation(df_clean['EAN'],np.nan,df_clean['{} {}'.format("Quantité", annee)],np.nan,df_clean['{} {}'.format("CA Net TTC", annee)], df_clean['code nielsen'],date,"VV")

        case 'leroy' :
            standardized_df,standardized_df_aggregated = uniformisation(df_clean['GTIN (EAN)'],np.nan,df_clean['Quantité vendue'],np.nan,df_clean['Ventes - montant'], df_clean['code nielsen'],date,"LM")

            #Séparation pour avoir uniquement les articles vendus en table_magasin
            tab_magasin = standardized_df[(standardized_df['PDV'] != 'BO Internet LEROY') & (standardized_df['PDV'] != 'Internet') & (standardized_df['PDV'] != 'Internet leroy es')]

            tab_internet = standardized_df[(standardized_df['PDV'] == 'BO Internet LEROY') | (standardized_df['PDV'] == 'Internet') | (standardized_df['PDV'] == 'Internet leroy es')]
            tab_internet['enseigne'] = 'LMFR'
            
            nb_magasin = standardized_df['Volume'] > 0

            new_magasin = tab_magasin.groupby('Gencode').agg({
                                            'Code_article':'first',
                                            'Volume':'sum',
                                            'Valeur HT': 'sum',
                                            'Valeur TTC' : 'sum',
                                            'PDV' : lambda x: x[nb_magasin].nunique(),
                                            'date' : 'first',
                                            'enseigne' : 'first'})
            new_magasin.reset_index(inplace= True)

            new_internet = tab_internet.groupby('Gencode').agg({
                                            'Code_article':'first',
                                            'Volume':'sum',
                                            'Valeur HT': 'sum',
                                            'Valeur TTC' : 'sum',
                                            'PDV' : lambda x: x[nb_magasin].nunique(),
                                            'date' : 'first',
                                            'enseigne' : 'first'})
            
            new_internet['PDV'] = np.nan
            new_internet.reset_index(inplace= True)

            #Concaténation des deux tableux en un seul, en ignorant l'index et suppresion des valeurs sans ventes
            standardized_df_aggregated = pd.concat([new_magasin, new_internet], ignore_index = True)

        case 'leroy es':
            standardized_df,standardized_df_aggregated = uniformisation(df_clean['GTIN (EAN)'],np.nan,df_clean['Quantité vendue'],np.nan,df_clean['Ventes - montant'], df_clean['Identifiant table_magasin/entrepôt'],date,"LMESP")

            nb_magasin = standardized_df['Volume'] > 0

            #Séparation pour avoir uniquement les articles vendus en table_magasin
            tab_magasin = standardized_df[(standardized_df['PDV'] != '58')]

            tab_internet = standardized_df[(standardized_df['PDV'] == '58')]
            tab_internet['enseigne'] = 'LMES'

            new_magasin = tab_magasin.groupby('Gencode').agg({
                                            'Code_article':'first',
                                            'Volume':'sum',
                                            'Valeur HT': 'sum',
                                            'Valeur TTC' : 'sum',
                                            'PDV' : lambda x: x[nb_magasin].nunique(),
                                            'date' : 'first',
                                            'enseigne' : 'first'})
            new_magasin.reset_index(inplace= True)

            new_internet = tab_internet.groupby('Gencode').agg({
                                            'Code_article':'first',
                                            'Volume':'sum',
                                            'Valeur HT': 'sum',
                                            'Valeur TTC' : 'sum',
                                            'PDV' : lambda x: x[nb_magasin].nunique(),
                                            'date' : 'first',
                                            'enseigne' : 'first'})
            
            new_internet['PDV'] = np.nan
            new_internet.reset_index(inplace= True)

            if not new_internet.empty :
                raise ValueError("le dataFrame internet est vide")

            #Concaténation des deux tableux en un seul, en ignorant l'index et suppresion des valeurs sans ventes
            standardized_df_aggregated = pd.concat([new_magasin, new_internet], ignore_index = True)
        
        case 'leroy portugal':
            standardized_df, standardized_df_aggregated = uniformisation(df_clean['GTIN (EAN)'],np.nan,df_clean['Quantité vendue'],np.nan,df_clean['Ventes - montant'], df_clean['Identifiant table_magasin/entrepôt'],date,"LMPORT")
            
        case 'amazon' :
            standardized_df, standardized_df_aggregated = uniformisation(df_clean['EAN'],np.nan,df_clean['Unités expédiées'],np.nan,df_clean['Chiffre d’affaires basé sur les expéditions'], df_clean['ASIN'],date,"AMZ")
            standardized_df_aggregated['PDV'] = np.nan
    
        case 'cdiscount' :
            standardized_df, standardized_df_aggregated = uniformisation(df_clean['EAN'],np.nan,df_clean['Nombre de commandes'],np.nan,np.nan,df_clean['Marque'],date,"CDIS")
            standardized_df_aggregated['PDV'] = np.nan

        case 'truffaut' :
            standardized_df,standardized_df_aggregated = uniformisation(df_clean['EAN'],np.nan,df_clean['Qté vendue'],np.nan,df_clean['CA TTC vendu'], df_clean['code nielsen'],date,"TFT")

            nb_magasin = standardized_df['Volume'] > 0
            
            tab_magasin = standardized_df[(standardized_df['PDV'] != 'E-COMMERCE')]
            tab_internet = standardized_df[(standardized_df['PDV'] == 'E-COMMERCE')]
            tab_internet['enseigne'] = 'TFTFR'

            new_magasin = tab_magasin.groupby('Gencode').agg({
                                            'Code_article':'first',
                                            'Volume':'sum',
                                            'Valeur HT': 'sum',
                                            'Valeur TTC' : 'sum',
                                            'PDV' : lambda x: x.where(nb_magasin).count() ,
                                            'date' : 'first',
                                            'enseigne' : 'first'})
            new_magasin['PDV'] = new_magasin['PDV'].astype(int)
            new_magasin.reset_index(inplace= True)
    
            new_internet = tab_internet.groupby('Gencode').agg({
                                            'Code_article':'first',
                                            'Volume':'sum',
                                            'Valeur HT': 'sum',
                                            'Valeur TTC' : 'sum',
                                            'PDV' : lambda x: x.where(nb_magasin).count() ,
                                            'date' : 'first',
                                            'enseigne' : 'first'})
            new_internet['PDV'] = np.nan
            new_internet.reset_index(inplace= True)

            standardized_df_aggregated = pd.concat([new_magasin, new_internet], ignore_index = True)
            standardized_df_aggregated = standardized_df_aggregated[standardized_df_aggregated['Volume'] != 0]
            
        case 'jardiland' :
            standardized_df, standardized_df_aggregated = uniformisation(df_clean['GENCOD table_article'],np.nan,df_clean['Quantité N'],df_clean['CA HT N'],np.nan,df_clean['code nielsen'],date,"JDL")

        case 'weldom' :
            standardized_df, standardized_df_aggregated = uniformisation(df_clean['EAN'],np.nan,df_clean['Qtt'],np.nan,df_clean['CA TTC'],df_clean['code nielsen'],date,"WD")

        case 'crf super' :
            standardized_df, standardized_df_aggregated = uniformisation(df_clean['EAN'],np.nan,df_clean['Qtés UVC ou UCT'],np.nan,df_clean['CA TTC'],df_clean['code nielsen'],date,"crf super")

        case 'crf hyper' :
            standardized_df, standardized_df_aggregated = uniformisation(df_clean['EAN'],np.nan,df_clean['Qtés UVC ou UCT'],np.nan,df_clean['CA TTC'],df_clean['code nielsen'],date,"crf hyper")

        case 'system u' :
            #standardized_df, standardized_df_aggregated = uniformisation(df_clean['EAN'],np.nan,df_clean["Nb d'UVC vendus"],np.nan,df_clean['CA TTC'],df_clean['Nb de PDV vendeurs'],date,"SU")
            standardized_df = pd.DataFrame()
            
            standardized_df['Gencode'] = df_clean['EAN'].astype(str)
            standardized_df['Code_article'] = np.nan
            standardized_df['Volume'] = df_clean["Nb d'UVC vendus"].astype(int)
            standardized_df['Valeur HT'] = np.nan
            standardized_df['Valeur TTC'] = df_clean['CA TTC'].astype(float)
            standardized_df['PDV'] = df_clean['Nb de PDV vendeurs']
            standardized_df['date'] = date
            standardized_df['enseigne'] = "SU"
            
            standardized_df_aggregated = standardized_df.groupby('Gencode').agg({
                                            'Code_article':'first',
                                            'Volume':'sum',
                                            'Valeur HT': 'sum',
                                            'Valeur TTC' : 'sum',
                                            'PDV' : 'sum' ,
                                            'date' : 'first',
                                            'enseigne' : 'first'})
            

        case 'vilmorin' :
            standardized_df, standardized_df_aggregated = uniformisation(df_clean['EAN'],np.nan,df_clean["QuantitÃ©"],np.nan,df_clean["Chiffre d'affaires TTC"],df_clean['Nom de la marketplace'],date,"np.nan")

            nb_magasin = standardized_df['Volume'] > 0

            leroy = standardized_df[(standardized_df['PDV'] == 'LERO_FR') ]
            cdiscount = standardized_df[(standardized_df['PDV'] == 'CD_FR') ]
            manomano = standardized_df[(standardized_df['PDV'] == 'MANO_FR') ]
            vilmorin = standardized_df[(standardized_df['PDV'] == 'MKTP VJ') ]

            def transformation(dataframe,id_enseigne):
                df = dataframe.groupby('Gencode').agg({
                                            'Code_article':'first',
                                            'Volume':'sum',
                                            'Valeur HT': 'sum',
                                            'Valeur TTC' : 'sum',
                                            'PDV' : 'first' ,
                                            'date' : 'first',
                                            'enseigne' : 'first'})
                
                df['enseigne'] = id_enseigne
                df.reset_index(inplace= True)

                return df
                
            tab_leroy = transformation(leroy,'MKTP LR')
            
            tab_cdiscount = transformation(cdiscount,'MKTP CD')
            
            tab_manomano = transformation(manomano,'MKTP MANO')
            
            tab_vilmo = transformation(vilmorin,'MKTP VJ')

            standardized_df_aggregated = pd.concat([tab_leroy, tab_cdiscount,tab_manomano,tab_vilmo], ignore_index = True)
            standardized_df_aggregated['PDV'] = 0

        case 'castorama' :
            standardized_df = pd.DataFrame()

            standardized_df['Gencode'] = df_clean['Code EAN'].astype(str)
            standardized_df['Code_article'] = np.nan
            standardized_df['Volume'] = df_clean['Quantités'].astype(int)
            standardized_df['Valeur HT'] = np.nan
            standardized_df['Valeur TTC'] = np.nan
            standardized_df['PDV'] = df_clean['code nielsen'].astype(str)
            standardized_df['date'] = date
            standardized_df['enseigne'] = "CASTO"
            standardized_df['canal'] = df_clean['Canal de vente']
            
            tab_magasin = standardized_df[standardized_df['canal'] == 'nb_magasin']


            nb_magasin = tab_magasin['Volume'] > 0

            new_magasin = tab_magasin.groupby(['Gencode']).agg({
                                            'Code_article':'first',
                                            'Volume':'sum',
                                            'Valeur HT': 'sum',
                                            'Valeur TTC' : 'sum',
                                            'PDV' : lambda x: x[nb_magasin].nunique() ,
                                            'date' : 'first',
                                            'enseigne' : 'first'})
            new_magasin.reset_index(inplace= True)
            
            
            tab_internet = standardized_df[standardized_df['canal'] == 'W']
            new_internet = tab_internet.groupby('Gencode').agg({
                                            'Code_article':'first',
                                            'Volume':'sum',
                                            'Valeur HT': 'sum',
                                            'Valeur TTC' : 'sum',
                                            'PDV' : 'first' ,
                                            'date' : 'first',
                                            'enseigne' : 'first'})
            new_internet['enseigne'] = 'CASTOFR'
            new_internet['PDV'] = np.nan
            new_internet.reset_index(inplace= True)
            
            
            standardized_df_aggregated = pd.concat([new_magasin, new_internet], ignore_index = True)
            standardized_df_aggregated = standardized_df_aggregated[standardized_df_aggregated['Volume'] != 0]

            standardized_df_aggregated = standardized_df_aggregated[['Gencode', 'Code_article', 'Volume', 'Valeur HT', 'Valeur TTC', 'PDV' , 'date' , 'enseigne']]

            standardized_df.drop(columns='canal', inplace = True)
            
        case "bricorama" :
            standardized_df = pd.DataFrame()

            if date[5:7] != '01' :
                merged_df = pd.merge(df_clean, last_month_df, left_on=' CODE EAN ', right_on=' CODE EAN ', how='left', suffixes=('df_clean', 'last_month_df'),indicator=True)

                #EAN parfois pas présent dans le fichier précédent (pas de vente précédemment), on setup les vides à 0
                merged_df[' QTE VENTE last_month_df'].fillna(0, inplace=True)
                merged_df[' CA HT last_month_df'].fillna(0, inplace=True)
                merged_df = merged_df.drop_duplicates()


                standardized_df['Gencode'] = merged_df[' CODE EAN '].astype(str)
                standardized_df['Code_article'] = np.nan
                standardized_df['Volume'] = (merged_df[' QTE VENTE df_clean'] - merged_df[' QTE VENTE last_month_df']).astype(int)
                standardized_df['Valeur HT'] = (merged_df[' CA HT df_clean']- merged_df[' CA HT last_month_df']).astype(float)
                standardized_df['Valeur TTC'] = np.nan
                standardized_df['PDV'] = np.nan
                standardized_df['date'] = date
                standardized_df['Enseigne'] = "BRM"

            else :
                standardized_df['Gencode'] = df_clean[' CODE EAN '].astype(str)
                standardized_df['Code_article'] = np.nan
                standardized_df['Volume'] = df_clean[' QTE VENTE '].astype(int)
                standardized_df['Valeur HT'] = df_clean[' CA HT '].astype(float)
                standardized_df['Valeur TTC'] = np.nan
                standardized_df['PDV'] = np.nan
                standardized_df['date'] = date
                standardized_df['Enseigne'] = "BRM"
            
            standardized_df.dropna(subset="Gencode",inplace=True)

            standardized_df.drop(standardized_df[(standardized_df['Volume'] == 0) | (standardized_df['Volume'] == 0.0) | (standardized_df['Volume'].isnull())].index, inplace=True)

            nb_magasin = standardized_df['Volume'] > 0

            standardized_df_aggregated = standardized_df.groupby('Gencode').agg({
                                            'Code_article':'first',
                                            'Volume':'sum',
                                            'Valeur HT': 'sum',
                                            'Valeur TTC' : 'sum',
                                            'PDV' : 'first' ,
                                            'date' : 'first',
                                            'Enseigne' : 'first'})
            
                #Stop le programme si aucune enseigne répertorié est décrite
        case _ :
            raise SystemExit("enseigne non référencée, vérifier le nom de l'enseigne ou ajouter la")
            
    return standardized_df,standardized_df_aggregated