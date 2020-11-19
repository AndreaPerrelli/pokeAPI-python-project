
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

pokemonNameLetters = ""
pokemonNameLengthBeforePreparedForFunction = ""
pokemonNameLengthAfterPreparedForFunction = ""
listOfPokemonNames = []
res = []
listOfUrlPokemon = []
pokemonList = []
resultListPokemonNameSprite = []
ifClear = True

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
        global resultListPokemonNameSprite
        global ifClear
        '''Show a frame for the given page name'''
        if page_name == "PageTwo" and ifClear:
            self.frames[page_name].refresh(controller=self)
        frame = self.frames[page_name]
        frame.tkraise()
        
        
        
        
class PageTwo(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is result query", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go back to search",
                           command=lambda: controller.show_frame(page_name = "PageOne"))
        button.pack()
        tree=ttk.Treeview(self)
        tree["columns"]=("one","two","three")
        tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
        tree.column("one", width=150, minwidth=150, stretch=tk.NO)
        tree.column("two", width=400, minwidth=200)
        tree.column("three", width=80, minwidth=50, stretch=tk.NO)
            
        tree.heading("#0",text="Name",anchor=tk.W)
        tree.heading("one", text="Date modified",anchor=tk.W)
        tree.heading("two", text="Type",anchor=tk.W)
        tree.heading("three", text="Size",anchor=tk.W)
                        
                        # Level 1
        folder1=tree.insert("", 1, "1", text="Folder 1", values=("23-Jun-17 11:05","File folder",""))
        tree.insert("", 2, "6", text="text_file.txt", values=("23-Jun-17 11:25","TXT file","1 KB"))
        # Level 2
        tree.insert(folder1, "end", "2", text="photo1.png", values=("23-Jun-17 11:28","PNG file","2.6 KB"))
        tree.insert(folder1, "end", "3", text="photo2.png", values=("23-Jun-17 11:29","PNG file","3.2 KB"))
        tree.insert(folder1, "end", "4", text="photo3.png", values=("23-Jun-17 11:30","PNG file","3.1 KB"))
            
        tree.pack(side=tk.TOP,fill=tk.X)
        
    def refresh(self, controller):
        self.destroy()
        self.__init__(self, controller)

        
        
    

        


class PageOne(tk.Frame):
    
    def __init__(self, parent, controller):
        global res
        global listOfUrlPokemon
        global pokemonList
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is pokemon name search", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        data = get_account_info() # Incapsulo risposta della chiamata API nella variabile data
        pokemonList = data['results'] # Estraggo dalla variabile data la lista di dizionari contenente il risultato e lo assegno a pokemonList
        res = list(map(itemgetter('name'), pokemonList))
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

def get_result_Pokemon_Name():
    global res
    global pokemonNameLetters
    global pokemonNameLengthAfterPreparedForFunction
    global pokemonNameLengthBeforePreparedForFunction
    regexString = rf"\b\w{pokemonNameLengthBeforePreparedForFunction}{pokemonNameLetters}\w{pokemonNameLengthAfterPreparedForFunction}\b"
    for element in res:
        global listOfPokemonNames
        match = re.match(regexString, element)
        if match != None:    
            if match.group():
                listOfPokemonNames.append(match.group())
                if len(listOfPokemonNames) > 0:
                    get_result_Pokemon_Image()
                
        
       
            
def get_result_Pokemon_Image():
    global listOfPokemonNames
    global resultListPokemonNameSprite
    imageData = None
    for pokemonName in listOfPokemonNames:
        pokemonDataListMatch = list(filter(lambda pokemon: pokemon['name'] == pokemonName, pokemonList))
        ''' for urlPokemon in listOfUrlPokemon:
            if (pokemonName in pokemonList) and (urlPokemon in pokemonList) :
                response = requests.get(urlPokemon, headers=headers) #effettuo la chiamata con attributi della funzione url ed headers precedentemente dichiarati
                if response.status_code == 200:
                    imageData = json.loads(response.content.decode('utf-8'))
                else:
                    imageData = None '''
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
        
                

def fetch(controller, entries):
    global ifClear
    for entry in entries:
        if entry[0] == fields[0]:
            global pokemonNameLetters
            pokemonNameLetters = entry[1].get()
            pass
        if entry[0] == fields[1]:
            global pokemonNameLengthBeforePreparedForFunction
            resultBefore = entry[1].get()
            pokemonNameLengthBeforePreparedForFunction = '{' + resultBefore + '}'
            pass
        if entry[0] == fields[2]:
            global pokemonNameLengthAfterPreparedForFunction
            resultAfter = entry[1].get()
            pokemonNameLengthAfterPreparedForFunction = '{' + resultAfter + '}'
            pass
    get_result_Pokemon_Name()
    ifClear = False
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
    self.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = tk.Button(self, text='Show',
                  command=(lambda e=ents, controller=controller: fetch(controller, e)))
    b1.pack(side=tk.LEFT, padx=20, pady=20)
    b2 = tk.Button(self, text='Quit', command=self.quit)
    b2.pack(side=tk.LEFT, padx=20, pady=20)
 

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
