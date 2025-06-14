def verifier_integrite_donnees(df_agregee, df_magasin, df_brut, enseigne, date, annee, merged_df=None):
    """
    Description
        Vérifie l'intégrité des volumes et du chiffre chiffre_affaire_brut'affaires (CA) en comparant les totaux issus des différentes sources.
        En cas chiffre_affaire_brut'incohérence, lève une exception avec un message explicite. Sinon, affiche les valeurs comparées et confirme la cohérence.

    Args : 
        df_agregee(DataFrame)
        df_magasin(DataFrame)
        df_brut(DataFrame)
        enseigne(str)
        date(str)
        annee(str)
        merded_df(DataFrame)
        
    Returns : 
        volume_aggrege(int)
        volume_brut(int)

    """
    # Vérification des volumes
    volume_aggrege = df_agregee['Volume'].astype(int).sum()
    volume_magasin = df_magasin['Volume'].astype(int).sum()

    match enseigne:
        case "bricomarche":
            volume_brut = df_brut['Qté Vendue Période N'].astype(int).sum()
            
        case 'botanic':
            volume_brut = df_brut['Qté.'].astype(int).sum()

        case 'gammvert':
            volume_brut = df_brut['Quantité Vente'].astype(int).sum()

        case 'sevea':
            volume_brut = df_brut[f"Quantité {annee}"].astype(int).sum()

        case 'leroy' | 'leroy es' | 'leroy portugal':
            volume_brut = df_brut['Quantité vendue'].astype(int).sum()

        case 'amazon':
            volume_brut = df_brut['Unités expédiées'].astype(int).sum()

        case 'cdiscount':
            volume_brut = df_brut['Nombre de commandes'].astype(int).sum()

        case 'truffaut':
            volume_brut = df_brut['Qté vendue'].astype(int).sum()

        case 'jardiland':
            volume_brut = df_brut['Quantité N'].astype(int).sum()

        case 'weldom':
            volume_brut = df_brut['Qtt'].astype(int).sum()

        case 'crf super' | 'crf hyper':
            volume_brut = df_brut['Qtés UVC ou UCT'].astype(int).sum()

        case 'system u':
            volume_brut = df_brut["Nb d'UVC vendus"].astype(int).sum()

        case 'vilmorin' | 'vilmorin.fr':
            volume_brut = df_brut["Quantité"].astype(int).sum()

        case 'castorama':
            volume_brut = df_brut["Quantités"].astype(int).sum()

        case 'bricorama':
            if date[5:7] != '01':
                volume_brut = (merged_df[' QTE VENTE data'] - merged_df[' QTE VENTE LastMonthDf']).astype(int).sum()
            else:
                volume_brut = df_brut[' QTE VENTE '].astype(int).sum()

        case _:
            raise SystemExit("enseigne non référencée, vérifier le nom")

    if volume_aggrege == volume_brut and volume_magasin == volume_brut:
        print(f"Volume agg: {volume_aggrege} / Volume magasin : {volume_magasin} / Volume data brutes : {volume_brut} / OK")
    else:
        print(f"Volume agg: {volume_aggrege} / Volume magasin : {volume_magasin} / Volume data brutes : {volume_brut} / NOT OK")
        raise SystemExit("Volume différent !")

    # Vérification du CA
    chiffre_affaire_agregge = round(df_agregee['Valeur TTC'].sum())
    chiffre_affaire_magasin = round(df_magasin['Valeur TTC'].sum())

    match enseigne:
        case "bricomarche":
            chiffre_affaire_brut = round(df_brut['CATTC Vendue Période N'].sum())

        case 'botanic':
            chiffre_affaire_brut = 0

        case "gammvert":
            chiffre_affaire_magasin = round(df_magasin['Valeur HT'].sum())
            chiffre_affaire_agregge = round(df_agregee['Valeur HT'].sum())
            chiffre_affaire_brut = round(df_brut['CA HT'].sum())

        case 'sevea':
            chiffre_affaire_brut = round(df_brut[f"CA Net TTC {annee}"].sum())

        case 'leroy' | 'leroy es' | 'leroy portugal':
            chiffre_affaire_brut = round(df_brut['Ventes - montant'].sum())

        case 'amazon':
            chiffre_affaire_brut = round(df_brut['Chiffre d’affaires basé sur les expéditions'].sum())

        case 'cdiscount':
            chiffre_affaire_brut = 0

        case 'truffaut':
            chiffre_affaire_brut = round(df_brut['CA TTC vendu'].sum())

        case 'jardiland':
            chiffre_affaire_agregge = round(df_agregee['Valeur HT'].sum())
            chiffre_affaire_magasin = round(df_magasin['Valeur HT'].sum())
            chiffre_affaire_brut = round(df_brut['CA HT N'].sum())

        case 'weldom' | 'crf super' | 'crf hyper' | 'system u':
            chiffre_affaire_brut = round(df_brut['CA TTC'].astype(float).sum())

        case 'vilmorin' | 'vilmorin.fr':
            chiffre_affaire_brut = round(df_brut["Chiffre chiffre_affaire_brut'affaires TTC"].sum())

        case 'castorama':
            chiffre_affaire_brut = 0

        case 'bricorama':
            if date[5:7] != '01':
                chiffre_affaire_brut = round((merged_df[' CA HT data'] - merged_df[' CA HT LastMonthDf']).astype(float).sum())
            else:
                chiffre_affaire_brut = round(df_brut[' CA HT '].astype(float).sum())
                
            chiffre_affaire_agregge = round(df_agregee['Valeur HT'].astype(float).sum())
            chiffre_affaire_magasin = chiffre_affaire_agregge
        case _:
            raise SystemExit("Stop right there!")

    if chiffre_affaire_brut == chiffre_affaire_magasin == chiffre_affaire_brut:
        print(f"Valeur agg: {chiffre_affaire_agregge} / Valeur magasin : {chiffre_affaire_magasin} / Valeur data brutes : {chiffre_affaire_brut} / OK")
        erreur = False
        
    else:
        print(f"Valeur agg: {chiffre_affaire_agregge} / Valeur magasin : {chiffre_affaire_magasin} / Valeur data brutes : {chiffre_affaire_brut} / NOT OK")
        erreur = True
    
    return volume_aggrege, chiffre_affaire_agregge, erreur
