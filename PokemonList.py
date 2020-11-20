
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
import json
import requests
from operator import itemgetter
import re
from PIL import Image
from io import BytesIO

fields = 'Letters of the Pokemon', '___ before the letters', '___ after the letters'
api_url_base = 'https://pokeapi.co/api/v2/' # Indirizzo endpoint per l'API
headers = {'Content-Type': 'application/json'} # headers della chiamata

resultListPokemonNameSprite = []

class SampleApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PageOne")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        if page_name == "PageTwo":
            frame.event_generate("<<UpdateFrame>>")
        frame.tkraise()
        
        
        
        
class PageTwo(tk.Frame):
    tree = None
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<UpdateFrame>>", self.on_show_frame)
        label = tk.Label(self, text="This is result query", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go back to search",
                           command=lambda: controller.show_frame(page_name = "PageOne"))
        button.pack()
        
        
    def on_show_frame(self, event):
        index = 0
        self.tree=ttk.Treeview(self)
        self.tree["columns"]=("Nome Pokemon","Immagine Pokemon")
        self.tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
        self.tree.column("Nome Pokemon", width=150, minwidth=150, stretch=tk.NO)
        self.tree.column("Immagine Pokemon", width=400, minwidth=200)
        # tree.column("three", width=80, minwidth=50, stretch=tk.NO)
            
        self.tree.heading("#0",text="Nome Pokemon",anchor=tk.W)
        self.tree.heading("Nome Pokemon", text="Immagine",anchor=tk.W)
        self.tree.heading("Immagine Pokemon", text="",anchor=tk.W)
        # tree.heading("three", text="Size",anchor=tk.W)
                        
                        # Level 1
        for resultPokemonNameSprite in resultListPokemonNameSprite:
            self.tree.bind("<Double-1>", self.link_tree)
            self.tree.insert("",index, str(index), text = resultPokemonNameSprite["name"], values = resultPokemonNameSprite["urlSprite"])
            index = index + 1
        ''' folder1=tree.insert("", 1, "1", text="Folder 1", values=("23-Jun-17 11:05","File folder",""))
        tree.insert("", 2, "6", text="text_file.txt", values=("23-Jun-17 11:25","TXT file","1 KB"))
        # Level 2
        tree.insert(folder1, "end", "2", text="photo1.png", values=("23-Jun-17 11:28","PNG file","2.6 KB"))
        tree.insert(folder1, "end", "3", text="photo2.png", values=("23-Jun-17 11:29","PNG file","3.2 KB"))
        tree.insert(folder1, "end", "4", text="photo3.png", values=("23-Jun-17 11:30","PNG file","3.1 KB")) '''
            
        self.tree.pack(side=tk.TOP,fill=tk.X)

    def link_tree(self,event):
        input_id = self.tree.selection()
        self.input_item = self.tree.item(input_id,"values")
        stringInputItem = str(self.input_item)
        splitHTTPS = stringInputItem.split("//")
        resultSplitHTTPS = splitHTTPS[1]
        splitEndURL = resultSplitHTTPS.split("'")
        stringResultSplit = str(splitEndURL[0])

        #for opening the link in browser
        import webbrowser
        webbrowser.open('{}'.format(stringResultSplit))
        #do whatever you want
        
        
    

        


class PageOne(tk.Frame):
    res = ""
    pokemonList = []
    pokemonNameLetters = ""
    pokemonNameLengthBeforePreparedForFunction = ""
    pokemonNameLengthBeforePreparedForFunction = ""
    listOfPokemonNames = []
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is pokemon name search", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        data = get_account_info() # Incapsulo risposta della chiamata API nella variabile data
        self.pokemonList = data['results'] # Estraggo dalla variabile data la lista di dizionari contenente il risultato e lo assegno a pokemonList
        self.res = list(map(itemgetter('name'), self.pokemonList))
        show_entry_fields(controller, self)
        #button = tk.Button(self, text="Make the Query",
                           #command=lambda: controller.show_frame("PageTwo"))
        #button.pack()
        
#def __main__():
    
#    data = get_account_info() # Incapsulo risposta della chiamata API nella variabile data
#    pokemonList = data['results'] # Estraggo dalla variabile data la lista di dizionari contenente il risultato e lo assegno a pokemonList
#    res = list(map(itemgetter('name'), pokemonList)) # Estraggo dalla lista di dizionari il valore della chiave 'name' per ogni dizionario presente
#    show_entry_fields()
#    get_result_Pokemon_Name(res)

#    input("Premi invio per uscire.")


    # Esempio Print
    # 'bulbasaur' , 'ivysaur', 'venusaur', 'charmender', 'charmeleon', etc....



def get_account_info():
    
    api_url = '{0}pokemon?limit=893'.format(api_url_base) #vado a puntare all'entry pokemon con limite 893 (tutti i pokemon)

    response = requests.get(api_url, headers=headers) #effettuo la chiamata con attributi della funzione url ed headers precedentemente dichiarati

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def get_result_Pokemon_Name(self):
    pokemonNameLettersResult = self.pokemonNameLetters
    pokemonNameLengthBeforePreparedForFunctionResult = self.pokemonNameLengthBeforePreparedForFunction
    pokemonNameLengthAfterPreparedForFunctionResult = self.pokemonNameLengthAfterPreparedForFunction
    
    regexString = rf"\b\w{pokemonNameLengthBeforePreparedForFunctionResult}{pokemonNameLettersResult}\w{pokemonNameLengthAfterPreparedForFunctionResult}\b"
    for element in self.res:
        match = re.match(regexString, element)
        if match != None:    
            if match.group():
                self.listOfPokemonNames.append(match.group())
                if len(self.listOfPokemonNames) > 0:
                    get_result_Pokemon_Image(self)
                
        
       
            
def get_result_Pokemon_Image(self):
    global resultListPokemonNameSprite
    imageData = None
    for pokemonName in self.listOfPokemonNames:
        pokemonDataListMatch = list(filter(lambda pokemon: pokemon['name'] == pokemonName, self.pokemonList))
    for pokemonDataMatch in pokemonDataListMatch:
        nameData = pokemonDataMatch['name']
        urlData = pokemonDataMatch['url']
        response = requests.get(urlData, headers=headers) #effettuo la chiamata con attributi della funzione url ed headers precedentemente dichiarati
        if response.status_code == 200:
            imageData = json.loads(response.content.decode('utf-8'))
            spriteDataList = imageData['sprites']
            spriteData = spriteDataList['front_default']
            resultListPokemonNameSprite.append( {"name" : nameData, "urlSprite" : spriteData} )
        else:
            imageData = None
        
                

def fetch(self, controller, entries):
    for entry in entries:
        if entry[0] == fields[0]:
            self.pokemonNameLetters = entry[1].get()
            pass
        if entry[0] == fields[1]:
            resultBefore = entry[1].get()
            self.pokemonNameLengthBeforePreparedForFunction = '{' + resultBefore + '}'
            pass
        if entry[0] == fields[2]:
            resultAfter = entry[1].get()
            self.pokemonNameLengthAfterPreparedForFunction = '{' + resultAfter + '}'
            pass
    get_result_Pokemon_Name(self)
    controller.show_frame(page_name = "PageTwo")

def makeform(self, fields):
    entries = []
    for field in fields:
        row = tk.Frame(self)
        lab = tk.Label(row, width=30, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=20, pady=20)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries            
            
                        
def show_entry_fields(controller, self):
    ents = makeform(self, fields)
    self.bind('<Return>', (lambda event, e=ents: fetch(self, e)))   
    b1 = tk.Button(self, text='Show',
                  command=(lambda e=ents, controller=controller: fetch(self, controller, e)))
    b1.pack(side=tk.LEFT, padx=20, pady=20)
    b2 = tk.Button(self, text='Quit', command=self.quit)
    b2.pack(side=tk.LEFT, padx=20, pady=20)
    

 

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
