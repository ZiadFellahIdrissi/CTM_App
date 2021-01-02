import os, psutil
# from tkinter import *
from tkinter import ttk,Tk,Text,Frame,Label,Canvas,Pack

def set_ctm_list(f,index):
    list_ctm=[]
    while True:
        s=f.readline().strip()
        if s!='':
            l_helper=s.split(" ")
            if len(l_helper) < 6:
                continue
            l_helper=[i for i in l_helper if i != ''][index:]
            while True:
                if ord(l_helper[1][0])>58:
                    l_helper[0]=l_helper[0]+" "+l_helper[1]
                    l_helper.remove(l_helper[1])
                else:
                    break
            list_ctm.append(l_helper)
        else:
            break
    return list_ctm

def chercheEntreprise(list_entreprise,entreprise):
    for el in list_entreprise:
        if el[0]==entreprise:
            return el[1]

def results(list_ctm,list_entreprise):
    j=0
    results=""
    # results+="| Fichie de base                   Fichie de system      |           Résultats        |\n"
    results+="|===================== ++++======================|============================|\n"
    for ele in list_ctm:
        code_entreprise=chercheEntreprise(list_entreprise,ele[0])
        if code_entreprise:
            if code_entreprise!=ele[1][24:48]:
                results+=code_entreprise+"         "+ele[1][24:48]+" (N'est pas bien) // "+ele[0]+"\n"
                j=j+1
            else:
                results+=code_entreprise+"         "+ele[1][24:48]+" (Bien) // "+ele[0]+"\n"
        else:
            results+="l'entreprise "+ele[0]+" n'exist pas dans le fichier de donnees \n"
            j=j+1
        
    if j:
        results+="\n=+=+==+=+=+=+=++=+=+=+=+= Il y a des RIPs qui ne correspondent pas =+=+=+=+=+=+=+=+\n"
    else:
        results+="\n=+=+==+=+=+=+=++=+=+=++=+ Tout est bon =+=+=+=+=+=+=+=+\n"
   
    return results
        
        
# Main
f= open("ctm.txt","r")
f2 = open("tout les entreprises.txt","r")


root = Tk()
root.title('CTM')
root.iconbitmap('./ctm.ico')
root.geometry("1000x550")

# Create A Main Frame
main_frame = Frame(root)
main_frame.pack(fill="both", expand=1)

# Create A Canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side="left", fill="both", expand=1)

# Add A Scrollbar To The Canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
my_scrollbar.pack(side="right", fill="y")

# Configure The Canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

# usig the mouse for scrolling
my_canvas.bind_all("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units"))

# Create ANOTHER Frame INSIDE the Canvas
second_frame = Frame(my_canvas)

# Add that New frame To a Window In The Canvas
my_canvas.create_window((0,0), window=second_frame, anchor="nw")

results =results(set_ctm_list(f,4),set_ctm_list(f2,0))
Label(second_frame,text=results, justify="left",font="Helvetica 13" ).pack(pady=10, padx=50)
Label(second_frame,text="Veuillez fermer l'application après avoir consulté les résultats", justify="left",font="Helvetica 13").pack(pady=20, padx=0)

root.resizable(False,True)  
root.mainloop()

# results(set_ctm_list(f,4),set_ctm_list(f2,0))
print("\n==================")
process = psutil.Process(os.getpid())
print(process.memory_info().rss/1000000,"Megabyte")