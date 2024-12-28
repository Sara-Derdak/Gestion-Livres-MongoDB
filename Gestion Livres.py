import time
from pymongo import MongoClient 

connexion = MongoClient("mongodb://localhost:27017/")

# Livres = list(connexion.Tp8.Livre.find())
# print(Livres)

def LivreID(id=""): 
    if(id!=""):
        return list(connexion.Tp8.Livre.find({"_id":id}))
    else :
        return list(connexion.Tp8.Livre.find({}))


while True :
    while True:
        print("********************** Menu **********************")
        print(" 1-Inseres un livre \n 2-Affiches tous les livres \n 3-Tri des resultats \n 4-Limition des resultats \n 5-Recherche un livre par auteur \n 6-Mise a jour la disponibilite d'un exemplaire d'un livre \n 7-Supprimer un livre \n 8-Affiche le nombre total des livres \n 9-Recherche des livres par disponibilite et genre \n 10-Le nombres de livres par auteur \n 11-Quitter")
        try :
            choix = int(input("Donner un nombre : "))
            if (choix in [1,2,3,4,5,6,7,8,9,10,11]):
                break
            else :
                print("Nombre Invalide , Choissiez une auter fois !!")
        except Exception as e :
            print(e)

    if (choix==1):
        id=int(input("Donner l'id : "))
        if (len(LivreID(id))!=0):
            time.sleep(1)
            print("ID deja existe !!")
        else :
            titre=input("Donner le titre :")
            auteur=input("Donner l'auteur :")
            anneeP=int(input("Donner l'annee de publication :"))
            nbrMotsCles=int(input("Donner le nombre de mots cles pour le genres : "))
            genres=[]
            for i in range(0,nbrMotsCles):
                g=input("Donner le mot cle : ")
                genres.append(g)
            nbrExemplaires=int(input("Donner le nombre d'exemplaires : "))
            exemplaires=[]
            for i in range(0,nbrExemplaires):
                e=input(f"Donner la disponibilitee d'exemplaire {i+1} (t/f)  : ")
                if(e=="t" or e=="T"):
                    e=True
                else :
                    e=False
                exemplaires.append({"numero":i+1,"disponibel":e})
            Livre={"_id":id,"titre":titre,"auteur":auteur,"annéePublication":anneeP,"genres":genres,"exemplaires":exemplaires}
            if(connexion.Tp8.Livre.insert_one(Livre)):
                time.sleep(1)
                print("Livre ajoutee avec succees !!")
            else :
                time.sleep(1)
                print("Insertion echec !!")
        

    elif (choix==2):
        L=list(connexion.Tp8.Livre.find({},{"titre":1,"auteur":1,"annéePublication":1,"_id":0,"genres":1}))
        if(len(L)>0):
            print("Liste des livres : ")
            time.sleep(1)
            for l in L :
                print(f"Titre : {l['titre']} , Auteur : {l['auteur']} , Annee de publication : {l['annéePublication']} , Genres : {l['genres']}")
        else :
            print("N'existes aucun Livres !!")


    elif (choix==3):
        L=list(connexion.Tp8.Livre.find({},{"titre":1,"auteur":1,"annéePublication":1,"_id":0}).sort({"annéePublication":-1}))
        if(len(L)>0):
            print("Liste des Livres triee : ")
            time.sleep(1)
            for l in L :
                print(l)
        else :
            print("N'existes aucun Livres !!")


    elif (choix==4):
        n=int(input("Combient de livre voulez vous voir : "))
        L=list(connexion.Tp8.Livre.find({},{"titre":1,"auteur":1,"annéePublication":1,"_id":0}))
        if(len(L)<n):
            time.sleep(1)
            print(f"On a juste {len(L)} livres")
        elif (len(L)==0):
            time.sleep(1)
            print("N'exist aucun Livres !!")
        else :
            print(f"Voici les {n} livres vous voulez :")
            time.sleep(1)
            for i in range(0,n):
                print(f"Titre : {L[i]['titre']} , Auteur : {L[i]['auteur']} , Annee de publication : {L[i]['annéePublication']}")


    elif (choix==5):
        a=input("Donner le nom d'auteur : ")
        L=list(connexion.Tp8.Livre.find({"auteur":a},{"titre":1,"genres":1,"annéePublication":1,"_id":0}))
        if(len(L)==0):
            time.sleep(1)
            print("N'existe aucun livre !!")
        else :
            print("Les livres d'auteur "+a+" :")
            time.sleep(1)
            for l in L :
                print(f"Titre : {l['titre']} , Annee de publication : {l['annéePublication']} , Genres : {l['genres']}")


    elif (choix==6):
        id = int(input("Donner l'ID du livre : "))
        # Vérifier si le livre existe
        livre = connexion.Tp8.Livre.find_one({"_id": id}, {"exemplaires": 1, "_id": 0})
        if livre:
            exemplaires = livre.get("exemplaires", [])
            if not exemplaires:
                print("Ce livre n'a pas d'exemplaires.")
            else:
                print("Liste des exemplaires :")
                for ex in exemplaires:
                    print(f"Numéro : {ex['numero']}, Disponible : {ex['disponibel']}")

                exp = int(input("Donner le numéro de l'exemplaire à changer : "))
                # Recherche manuelle de l'exemplaire
                exemplaire = None
                for e in exemplaires:
                    if e["numero"] == exp:
                        exemplaire = e
                        break

                if exemplaire:
                    nouvelle_dispo = not exemplaire["disponibel"] 
                    result = connexion.Tp8.Livre.update_one(
                        {"_id": id, "exemplaires.numero": exp},
                        {"$set": {"exemplaires.$.disponibel": nouvelle_dispo}}
                    )
                    if result.modified_count > 0:
                        print("Disponibilité modifiée avec succès !")
                    else:
                        print("Aucune modification effectuée.")
                else:
                    print("Numéro d'exemplaire invalide.")
        else:
            print("Livre introuvable.")



    elif (choix==7):
        annee = int(input("Entrez l'année limite pour la suppression des livres : "))
        if(len(list(connexion.Tp8.Livre.find({"annéePublication": {"$lt": annee}})))):
            resultats = connexion.Tp8.Livre.delete_many({"annéePublication": {"$lt": annee}})
            if(resultats.deleted_count!=0):
                time.sleep(1)
                print("Supp avec success !!")
            else :
                time.sleep(1)
                print("Erreur !!")
        else :
            time.sleep(1)
            print("N'exist aucun Livres dans notre collection publiee avant cette date !!")


    elif (choix==8):
        count=len(LivreID())
        if(count!=0):
            time.sleep(1)
            print("Le nombre total des livres est : ",count)
        else :
            time.sleep(1)
            print("N'existe aucun livre !!")


    elif (choix==9):
        g=input("Donner le genre qui vous voulez : ")
        if(len(LivreID())==0):
            time.sleep(1)
            print("N'existe aucun Livres ,il faut l'ajouter !!")
        else :
            livreGenre=list(connexion.Tp8.Livre.find({"disponible":True,"genres":g},{"_id":0,"titre":1,"auteur":1,"annéePublication":1}))
            if(len(livreGenre)==0):
                time.sleep(1)
                print("N'existe aucun livre avec ce genre disponible !!")
            else :
                print(f"Voici les livres de genre {g} :")
                time.sleep(1)
                for l in livreGenre :
                    print(l)


    elif (choix==10):
        a=input("Donner le nom d'auteur : ")
        if(len(LivreID())==0):
            time.sleep(1)
            print("N'existe aucun livre , il faut l'ajouter !")
        else :
            nbrLivreAuteur=list(connexion.Tp8.Livre.aggregate([{"$match":{"auteur":a}},{"$group":{"_id":"$auteur","Nombre de livres":{"$count":{}}}},{"$project":{"_id":0,"Nombre de livres":1}}]))
            if len(nbrLivreAuteur)==0 :
                time.sleep(1)
                print("N'existe aucun Livre de votre auteur !!")
            else :
                print(nbrLivreAuteur)

    else:
        print("Au revoir !!")
        break
   

    v=input("Voulez vous continue (n/o) :")
    if(v=="n" or v=="N"):
        print("Au revoir !!")
        break
