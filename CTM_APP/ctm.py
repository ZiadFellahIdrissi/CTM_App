import pandas as pa
from tkinter import Tk,Label,Button,filedialog
from tkinter.messagebox import showinfo
import os


root = Tk()
root.title('CTM')
# root.iconbitmap('./ctm.ico')
root.geometry("540x150")


def traitement_de_fichie_csv():
    text_file = filedialog.askopenfilename(initialdir="C:/", title="Open File", filetypes=(("CSV files", "*.csv"), ))
    if text_file:
        ctm_file = pa.read_csv(text_file , encoding = "ISO-8859-1", engine='python', sep=';')
        # list_entreprise=[]
        # j=0
        # for i in ctm_file["Remettant"]:
        #     mot=i.split(" ")[2:]
        #     mot=" ".join(mot)
        #     ctm_file.iloc[j,2]=mot
        #     j+=1
        
        if ctm_file['Encaissement'].dtype == float:
            d=list(ctm_file.groupby(["Remettant"]))
            for i in d:
                f=i[1][['Chèque paiement' , "Remettant" , "Récépissé" , "Destinataire" , "Ville" , "Date" ,'Encaissement']]
                f=f.append(pa.DataFrame(f.Encaissement.sum(), index = ["Total général"], columns=["Encaissement"]))
                f = f.rename(columns={'Chèque paiement': 'Réf de paiement ', 'Encaissement': 'Somme de Encaissement'})
                f.iloc[1:,0:2] = ""
                f.iloc[-1,0]=f.index[-1] 
                # list_entreprise.append(i[0])
                outname = i[0]+'.csv'

                outFolder = './resultat'
                if not os.path.exists(outFolder):
                    os.mkdir(outFolder)

                fullname = os.path.join(outFolder, outname)    
                f.to_csv(fullname , index=False ,encoding = "ISO-8859-1", sep=';')
                root.config(bg="black")

            btn.destroy()
            Label(root,text="Tout est bien, veuillez consulter le dossier Resultat" , font="15" ,bg="black" , fg="#54e397", pady="50").pack()
            # showinfo("Info_CSV !", "hahhaha")
        else:
            showinfo("Info_CSV !", "Changer la virgule décimale en un point dans la colonne `Encaissement` \n\n 1- Sous l'onglet Fichier, cliquez sur le bouton Options \n 2-Dans la boîte de dialogue Options Excel, sous l'onglet Options Avancé, décochez la case Utiliser les séparateurs système:  ")
            # Label(root,text="" , font="15" ,bg="black" ,height="5", fg="#e37154", pady="50" , padx="30").pack()
            
    # else:
    #     Label(root,text="Selection le fichie !" , font="15" ,bg="black" ,height="5", fg="#e37154", pady="50" , padx="30").pack()


    

    
btn=Button(text="Ajouter le Document", font="Times 15", pady="12", bg="#739998" , padx="8", command=traitement_de_fichie_csv)
btn.pack(pady="50")
root.resizable(False,False)
root.mainloop()
