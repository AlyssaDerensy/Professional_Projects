import os
import csv

def output(enseigne,df) :
    '''
     Description
        Fonction qui permet à l'utilisateur de vérifier les informations puis d'accepter, ou non, l'écriture des données.

    Args : 
        enseigne(str)
        df(DataFrame)
        
    Returns : 
        aucun
    
    '''
    match enseigne :
            
            case 'leroy' | 'weldom' | 'castorama':
                if os.path.isfile(r'data\output\adeo.csv'):
                    header = False
                else:
                    header = True

                df.to_csv(r'data\output\adeo.csv', index = False, mode = "a",header = header, sep = ';',decimal = ",",quoting=csv.QUOTE_NONNUMERIC)
                print("Fichier magasin modifié")

            case 'gammvert' :
                if os.path.isfile(r'data\output\gammvert.csv'):
                    header = False
                else:
                    header = True

                df.to_csv(r'data\output\gammvert.csv', index = False, mode = "a",header = header, sep = ';',decimal = ",",quoting=csv.QUOTE_NONNUMERIC)
                print("Fichier magasin modifié")

            case "bricomarche":
                
                if os.path.isfile(r"data\output\bricomarche.csv"):
                    header = False
                else:
                    header = True

                df.to_csv(r"data\output\bricomarche.csv", index = False, mode = "a",header = header, sep = ';',decimal = ",",quoting=csv.QUOTE_NONNUMERIC)
                print("Fichier magasin modifié")

            case "crf super" | "crf hyper" :

                if os.path.isfile(r'data\output\carrefour.csv'):
                    header = False
                else:
                    header = True

                df.to_csv(r'data\output\carrefour.csv', index = False, mode = "a",header = header, sep = ';',decimal = ",",quoting=csv.QUOTE_NONNUMERIC)
                print("Fichier magasin modifié")
            
            case "sevea" | "botanic" | "truffaut" | 'jardiland':

                if os.path.isfile(r'data\output\jardin.csv'):
                    header = False
                else:
                    header = True

                df.to_csv(r'data\output\jardin.csv', index = False, mode = "a",header = header, sep = ';',decimal = ",",quoting=csv.QUOTE_NONNUMERIC)
                print("Fichier magasin modifié")

            case _ :
                print("Pas de fichier magasins")