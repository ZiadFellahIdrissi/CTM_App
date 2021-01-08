# import os, psutil
from tkinter import ttk,Tk,Text,Frame,Label,Canvas,Pack,Menu,filedialog,colorchooser,font,Button
import os, sys
import tempfile

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
    results+="|======================= ++++ ======================|============================|\n"
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
    
# ===================================================GUI function==================================================//
def print_file():
    q=my_text.get(1.0,"end")
    file_name0=tempfile.mktemp(".txt")
    open (file_name0 , "w").write(q)
    os.startfile(file_name0,"print")

# Save As File
def save_as_file():
	text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/", title="Save File",
                                             filetypes=(("Text Files", "*.txt"), )
                                            )
	if text_file:
		# Update Status Bars
		name = text_file
		status_bar.config(text=f'Saved: {name}        ')
		name = name.replace("C:/", "")
		root.title(f'{name} - CTM')

		# Save the file
		text_file = open(text_file, 'w')
		text_file.write(my_text.get(1.0, "end"))
		# Close the file
		text_file.close()

# Change bg color
def bg_color():
	my_color = colorchooser.askcolor()[1]
	if my_color:
		my_text.config(bg=my_color)

# Change ALL Text Color
def all_text_color():
	my_color = colorchooser.askcolor()[1]
	if my_color:
		my_text.config(fg=my_color)


#Change Selected Text Color
def text_color():
	# Pick a color
	my_color = colorchooser.askcolor()[1]
	if my_color:
		# Create our font
		color_font = font.Font(my_text, my_text.cget("font"))

		# Configure a tag
		my_text.tag_configure("colored", font=color_font, foreground=my_color)

		# Define Current tags
		current_tags = my_text.tag_names("sel.first")

		# If statment to see if tag has been set
		if "colored" in current_tags:
			my_text.tag_remove("colored", "sel.first", "sel.last")
		else:
			my_text.tag_add("colored", "sel.first", "sel.last")

# Bold Text
def bold_it():
	# Create our font
	bold_font = font.Font(my_text, my_text.cget("font"))
	bold_font.configure(weight="bold")

	# Configure a tag
	my_text.tag_configure("bold", font=bold_font)

	# Define Current tags
	current_tags = my_text.tag_names("sel.first")

	# If statment to see if tag has been set
	if "bold" in current_tags:
		my_text.tag_remove("bold", "sel.first", "sel.last")
	else:
		my_text.tag_add("bold", "sel.first", "sel.last")

# Italics Text
def italics_it():
	# Create our font
	italics_font = font.Font(my_text, my_text.cget("font"))
	italics_font.configure(slant="italic")

	# Configure a tag
	my_text.tag_configure("italic", font=italics_font)

	# Define Current tags
	current_tags = my_text.tag_names("sel.first")

	# If statment to see if tag has been set
	if "italic" in current_tags:
		my_text.tag_remove("italic", "sel.first", "sel.last")
	else:
		my_text.tag_add("italic", "sel.first", "sel.last")
# =================================================================================================================//


# Main
f= open("ctm.txt","r")
f2 = open("tout les entreprises.txt","r")

root = Tk()
root.title('CTM')
root.iconbitmap('./ctm.ico')
root.geometry("1100x550")

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
# Label(second_frame,text=results, justify="left",font="Helvetica 13" ).pack(pady=10, padx=50)
# Label(second_frame,text="Veuillez fermer l'application après avoir consulté les résultats", justify="left",font="Helvetica 13").pack(pady=20, padx=0)

my_text = Text(second_frame, width=100, height=25, font=("Helvetica", 14), selectbackground="yellow", 
               selectforeground="black", undo=True, yscrollcommand=my_scrollbar.set, wrap="none")
my_text.pack()
my_text.insert('end', results)

# Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add file Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='Fichier' , menu=file_menu)
file_menu.add_command(label="Enregistrer sous ...", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Imprimer ...", command = print_file )
file_menu.add_separator()
file_menu.add_command(label="Quitter", command=root.quit)

# Add Color Menu
color_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Couleurs", menu=color_menu)
color_menu.add_command(label="Texte sélectionné", command=text_color)
color_menu.add_command(label="Tout le texte", command=all_text_color)
color_menu.add_command(label="Arrière plan",command=bg_color )

# Add Options Menu
options_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Texte en gras",command=bold_it)
options_menu.add_command(label="Texte en italique",command=italics_it )


# Add Status Bar To Bottom Of App
status_bar = Label(root, text='Ready        ', anchor='e')
status_bar.pack(fill='x', side='bottom', ipady=5)

root.resizable(False,True)  
root.mainloop()

# results(set_ctm_list(f,4),set_ctm_list(f2,0))
# print("\n==================")
# process = psutil.Process(os.getpid())
# print(process.memory_info().rss/1000000,"Megabyte")