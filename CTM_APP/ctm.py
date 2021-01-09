import pandas as pa
from tkinter import Tk,Label
import os
ctm_file = pa.read_csv("ctm_base.csv" , encoding = "ISO-8859-1", engine='python', sep=';')

root = Tk()
root.title('CTM')
# root.iconbitmap('./ctm.ico')
root.geometry("540x150")

if ctm_file['Encaissement'].dtype == float:
    d=list(ctm_file.groupby(["Remettant"]))
    for i in d:
        f=i[1][['Chèque paiement' , "Remettant" , "Récépissé" , "Destinataire" , "Ville" , "Date" ,'Encaissement']]
        f=f.append(pa.DataFrame(f.Encaissement.sum(), index = ["Total général"], columns=["Encaissement"]))
        f = f.rename(columns={'Chèque paiement': 'Réf de paiement ', 'Encaissement': 'Somme de Encaissement'})
        f.iloc[1:,0:2] = ""
        f.iloc[-1,0]=f.index[-1] 
        outname = i[0]+'.csv'

        outFolder = './resultat'
        if not os.path.exists(outFolder):
            os.mkdir(outFolder)

        fullname = os.path.join(outFolder, outname)    
        f.to_csv(fullname , index=False ,encoding = "ISO-8859-1", sep=';')
        root.config(bg="black")
    Label(root,text="Tout est bien, veuillez consulter le dossier Resultat" , font="15" ,bg="black" , fg="#54e397", pady="50").pack()
else:
    Label(root,text="Changer la virgule décimale en un point dans la colonne `Encaissement` \n\n 1- Sous l'onglet Fichier, cliquez sur le bouton Options \n 2-Dans la boîte de dialogue Options Excel, sous l'onglet Options Avancé, \n  décochez la case Utiliser les séparateurs système:  " , font="15" ,bg="black" ,height="5", fg="#e37154", pady="50" , padx="30").pack()
    print("impossible")
root.resizable(False,False)
root.mainloop()
