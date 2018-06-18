import tkinter as tk
"""Bibliothek zum Simulieren von Tasteneingaben, Änderungen im Quelltext der Dateien (__init__ und _pyautogui_win)"""
import pyautogui as key
from tkinter import ttk, filedialog
import socket as so
import json


class Arduino(object):
    
    ##Erstellt einen Arduino
    #@param window Objekt der Klasse Window
    
    def __init__(self, window):
        ##@brief Objekt der Klasse Window zum Zugreifen auf dessen Parameter
        self.window= window
        
        ##@brief Variable zum Zwischenspeichern der empfangenen Daten
        self.buffer= bytes()
        ##@brief gibt an, ob Verbindung besteht
        self.connected= False
        #Erstellt Fenster zum Verbinden
        self.connect_window= Connect_window(self)

    ## Schließt beim Löschen die Verbindung
    def __del__(self):
        self.close()

    """
    Sendet Nachricht an den Arduino, dass Verbndung geschlossen werden soll,
    dieser startet sich neu, um nicht abzustürzen.
    """
    def send_off(self):
        
        try:
            self.socket.send('off'.encode('utf-8') + b'\n')
            self.window.window.after(20, self.send_off) #Nachricht wird nicht jedes mal empfangen, also wird Text mehrmals gesendet
        except:
            pass
        
    ##Schließt die Verbindung zum Arduino
    def close(self):
        ##@brief Setzt den Zustand auf nicht verbunden
        self.connected= False
        try:
            #Stoppt, Nachrichten zu senden
            self.window.window.after_cancel(self.send_off)
            #Schließt den Socket
            self.socket.close()
            print('Tried to close the connection')
        except:
            #Erscheint, wenn beim Schließen keine Verbinfung besteht
            print('Was not able to close the connection')
        
    """
    Methode, die die Verbindung mit dem Arduino herstellt.
    @param host IP-Adresse des Arduinos
    @param port Port des Arduinos
    """
    def new_connection(self, host, port):   
        ##@brief Erstellt ein Objekt der Klasse Socket
        self.socket= so.socket()
        try:
            #Versucht, Verbindung herzustellen
            self.socket.connect((host, port))
            self.socket.setblocking(False)
            #Setzt die Anzahl der Fehler zurück
            self.errors= 0
            #Setzt den Verbindungsstatus auf verbunden
            self.connected= True
            print('Connection successful')
            #Wartet auf Kommandos vom Arduino
            self.listen()            
        except:
            #Erzeugt neues Fenster zum Verbinden
            self.connect_window= Connect_window(self)
            print('Error')
        
    def listen(self):
        """
        Empfängt vom Arduino versendete Daten und stellt fest, ob 
        überhaupt eine fehlerfreie Verbindung mit dem Arduino besteht.
        """
        try:
            #Empfängt gesendete Daten, speichert sie im Buffer
            read = self.socket.recv(1024)
            self.buffer+= read
            
        except:
            #Arduino hat keine Daten gesendet
            self.errors+= 1      
            if self.errors>500: 
                """   
                Wenn die Anzahl der gescheiterten Empfangsversuche 500 übersteigt, also 2,5s nichts empfangen wurde,
                wird eine Fehlermeldung ausgegeben und das Verbindungsfenster wieder aufgerufen.
                """
                print('Connection failed') 
                self.close()
                self.connect_window= Connect_window(self)
                        
        while b'\n' in self.buffer:
            #Teilt den Buffer in Zeilen auf und verarbeitet diese 
            try:
                #Decodiert den Buffer
                read, self.buffer= self.buffer.split(b'\n')
                read= read.decode('utf-8').strip()

                if read=="t":
                    #Es wurde ein Testbyte empfangen, der Arduino ist also verbunden
                    #Setzt die Fehler zurück
                    self.errors= 0
                else:
                    try:
                        #Wandelt empfangene Zahl in Index um
                        i= int(read)-1
                        if 0<=i<=15:
                            #Ruft den Befehl des Buttons auf
                            self.window.buttons[i].exec_command()
                    except ValueError:
                        pass
            except:
                pass
            
        if self.connected:
            #Falls der Arduino noch verbunden ist, wird nach 5ms erneut auf Kommandos geprüft
            self.window.window.after(5,self.listen)


class Connect_window(object):
    """
    Definiert und erzeugt das Verbindungsfenster, dass zeitgleich mit dem Aufruf des eigentlichen
    Bedienfensters aufgerufen wird um die IP-Adresse und den Port für die aufzubauende 
    Verbindung festzulegen.
    @param arduino Objekt der Klasse Arduino 
    """
    def __init__(self, arduino):
        ##@brief Speichert den gegebenen Arduino
        self.arduino= arduino
        #Erzeugt Fenster
        self.connect_window= tk.Toplevel()
        #Verschiebt Fenster nach oben
        self.connect_window.attributes("-topmost", True)

        #Erzeugt Bedienelemente
        self.connect_button= tk.ttk.Button(self.connect_window, text= 'Connect', command= self.connect)
        self.ip_label= tk.Label(self.connect_window, text= "IP-Adresse:")
        self.ip_field= tk.Entry(self.connect_window)
        self.port_label= tk.Label(self.connect_window, text= "Port:")
        self.port_field= tk.Entry(self.connect_window)
        #Zeigt Bedienelemente an
        self.ip_label.grid(column= 0, row= 0)
        self.ip_field.grid(column= 1, row= 0)
        self.port_label.grid(column= 0, row= 1)
        self.port_field.grid(column= 1, row= 1)
        self.connect_button.grid(column= 1, row= 2)

    def __del__(self):
        """
        Schließt das Verbindungsfenster nach Eingabe der Verbindungsdaten(IP,Port)
        """

        try:
            self.connect_window.destroy()
        except:
            pass        

    def connect(self):
        """
        Stellt die Verbindung mit dem Arduino her, indem es die Verbindungsdaten
        an die "new-connection"-Methode der Klasse Arduino weitergibt.
        """
        try:
            host= self.ip_field.get()
            port= int(self.port_field.get())
            self.arduino.new_connection(host, port)
            self.__del__()
        except ValueError:
            #Falsche Eingaben
            print('Value Error')


class Window(object):
    """
    Definiert und erzeugt das Hauptfenster. Inhalte des Hauptfensters sind:
    Keypad(keypad), Textfeld(text_field) , Speicherknopf(save_button) und Checkbox(command_checkbutton)
    Profilspeicherknopf(json_button), Profilladeknopf(load_button).
    """
    def __init__(self):
        self.window= tk.Tk()
        self.window.title('Keypad')
        #Ändert die Routine, die beim Schließen des Fensters ausgeführt wird, um den Arduino zu benachrichtigen
        self.window.protocol("WM_DELETE_WINDOW", self.on_closed)
        ##@brief Der aktuell zum Bearbeiten ausgewählte Button
        self.cur_button= 0
        ##@brief Liste, in der die Button-Objekte gespeichert sind
        self.buttons= []

        #Erzeugt Label     
        self.label= tk.Label(self.window, text="Neue Belegung für Taste:") 
        self.label.grid(row=5,column=0, columnspan= 2)
        #Textfeld zum Eingeben der neuen Tastenbelegung
        self.text_field= Text_field(self)
        #Checkbutton zum Auswählen, ob eine Tastenkombination eingegeben werden soll
        self.command_checkbutton= Command_checkbutton(self)
        #Button zum Speichern des Textes
        self.save_button= Save_button(self)
        #Erzeugt Keypad
        self.keypad= Keypad(self)
        #Buttons zum Speichern des Presets
        self.json_save_button = Json_save_button(self)
        self.json_load_button = Json_load_button(self)
        
        #Erzeugt Arduino
        self.arduino= Arduino(self)

        #Übergabe an Tkinter         
        self.window.mainloop()


    ##Sendet beim Schließen des Fensters Nachricht an Arduino, um diesen neu zu starten
    #und so Abstürzen zu verhindern
    def on_closed(self):
        try:
            self.arduino.send_off()
        except AttributeError:
            pass
        #Wartet bis zum Schließen des Fensters eine Sekunde, damit Nachricht empfangen wird
        self.window.after(1000, self.__del__)

    def __del__(self):
        try:
            self.window.destroy()
        except:
            pass


class Keypad(object):   
    """
    Die Klasse Keypad definiert, wie die Buttons im späteren Programm
    angeordnet sind und erzeugt sie.
    """
    def __init__(self, window):
        self.window= window
        ##Anordnung der Buttons mit Beschriftung
        self.keys=[     
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D'] 
        ]
        ##Erzeugt die Buttons und speichert sie in zum Fenster gehörenden Liste
        for y in range(4):      
            for x in range(4):
                self.window.buttons.append(Button(self.window, label= self.keys[y][x], x=x, y=y+1, index=x+(4*y)))  #Werden in Liste gespeichert


class Button (object):
    """
    Die Klasse Button definiert den Aufbau eines Buttons und die dazugehörigen Parameter.
    Die Buttons werden im ttk-Style dargestellt.
    Jedem Button kann ein Text zugeordnet werden, die Variable is_command gibt mit 0 = Nein
    und 1 = Ja an, ob es sich hierbei um  einen Tastatur-Kurzbefehl handelt.
    """
    ##Konstruktor
    #@param window Objekt der Klasse Window
    #@param label Beschriftung, die dargestellt wird
    #@param x x-Koordinate
    #@param y y-Koordinate
    #@param index Index in der Liste
    def __init__(self, window, label, x, y, index):
        #Fenster, in dem sich Buttons befinden, für Zugriff auf Variablen/Funtionen
        self.window= window
        #Position in der Liste
        self.index= index 
        #Gibt an, ob es sich um Tastenkombinatioin handelt
        self.is_command= 0 
        #gespeicherter Text, der geändert werden kann, dieser wird beim Drücken des Buttons am Auduino getippt bzw. als Tastenkombination ausgeführt   
        self.button_text= ''   
        #Erzeugt ttk-Style
        style= tk.ttk.Style()
        style.configure("Active_Button.TButton", foreground="black", background="blue")

        #Erzeugt Button über tkinter
        self.button=tk.ttk.Button(self.window.window, command= self.set_cur_button, text= label) 
        self.button.grid(row= y, column= x)     
        
    
    def change_text(self, new_text, is_command):   
        """
        Methode mit der der dem Button zugewiesene Text geändert wird.
        """
        self.button_text= new_text
        self.is_command= is_command
        
    def exec_command(self):
        """
        Wenn der zugewiesene Text ein Tastatur-Kurzbefehl sein soll,
        wird mit dieser Methode bewirkt, dass er auch als solcher 
        ausgeführt wird.
        """
        if self.is_command:     
            """
            Führt Tastenkombination aus. Der dem Button zugewiesene Text wird
            hierfür zunächst in eine Liste einzelner Elemente aufgeteilt.
            Mit einer For-Schleife werden die Buttons zuerst gedrückt und dann losgelassen
            """
            command_keys= self.button_text.split()
            for command_key in command_keys:
                key.keyDown(command_key, pause=0.1)
            for command_key_up in reversed(command_keys):    
                key.platformModule._keyUp(command_key_up)   
        else:              
            """
            Falls der Text kein Tastatur-Kurzbefehl ist, wird dieser einfach mittels der typewrite-Methode von Pyautogui getippt.
            """
            key.typewrite(self.button_text, interval= 0.00)

    def set_cur_button(self): 
        """
        Setzt den angeklickten Button als aktuell ausgewählten Button, der bearbeitet werden soll.
        Der dem Button aktuell zugewiesene Text wird im Textfeld angezeigt.
        """
        self.window.buttons[self.window.cur_button].button.configure(style= "TButton")
        self.window.cur_button=self.index
        self.window.buttons[self.window.cur_button].button.configure(style= "Active_Button.TButton")
        self.window.text_field.update_text(self.button_text)      
        self.window.command_checkbutton.update_checked(self.is_command)


class Json_save_button (object):
    """
    Definiert und erzeugt einen Button um das Speichern von Profilen zu ermöglichen.
    """
    def __init__(self,window):
        self.window= window
        self.json_button = tk.ttk.Button(window.window, command=self.save_json,text= 'Profil speichern')
        self.json_button.grid(row=0, column=0, columnspan= 2, sticky= tk.W+tk.E)
        

    def save_json(self):
        """
        Methode, mit der der den Einzelnen Tasten zugewiesene Text und der jeweilige
        Status(Bezogen auf 'Is_command') in einer Datei gespeichert wird. Hierfür wird 
        eine Liste(json_list) mit den Tastenbelegungen angelegt und eine Liste(is_command_list) 
        mit dem Status der Tasten(bezogen auf die "Command"-Checkbox) angelegt. Die beiden Listen
        werden in ein Dictionary(write_to_json) zusammengefügt und im Json-Format gespeichert. 
        Die Wahl des Dateinamens geschieht mithilfe des Tkinter-Moduls Filedialog.
        """
        json_list = []
        is_command_list = []
        write_to_json = {}

        filename= tk.filedialog.asksaveasfilename(filetypes= [("JSON File","*.json")])

        if filename:
            for button in self.window.buttons:
                json_list.append(button.button_text)
                is_command_list.append(button.is_command)

            for i in range(16):
                write_to_json['Content'+str(i)]= str(json_list[i])
                write_to_json['Is_Command'+str(i)]= str(is_command_list[i]) 
          
            with open(filename+'.json','w') as file:
                json.dump(write_to_json,file)      
                

class Json_load_button(object):
    """
    Definiert und erzeugt einen Button um das Laden von Profilen zu ermöglichen.
    """
    def __init__(self,window):
        self.window= window
        self.load_button = tk.ttk.Button(window.window, command = self.load,text= 'Profil laden')
        self.load_button.grid(row=0, column=2, columnspan= 2, sticky= tk.W+tk.E)

    def load(self):

        """
        Die im Profil im Json-Format gespeicherten Daten werden in ein temporäres Dictionary("dictionary") geladen und
        anschließend in zwei Listen("Content" und "Is_Command")  aufgeteilt. Anschließend wird den Tasten der 
        im jeweiligen Profil abgelegte Inhalt und Status mit einer For-Schleife zugewiesen. Die Auswahl der zu 
        ladenden Datei geschieht mithilfe des Tkinter-Moduls Filedialog.
        """
        
        content = []
        iscmd = []

        filename= tk.filedialog.askopenfilename(filetypes= [("JSON File","*.json")])
        
        if filename and filename.endswith('.json'):
            with open(filename) as file:
                try:
                    dictionary = json.load(file)
                    for i in range(16):
                        content.append(dictionary["Content"+str(i)])
                        iscmd.append(int(dictionary["Is_Command"+str(i)]))
                    for button in self.window.buttons:
                        button.change_text(content[button.index], iscmd[button.index])
                    self.window.buttons[0].set_cur_button()
                    
                except TypeError:
                    print('Wrong Format')


class Save_button (object):     
    """
    Die Klasse Save_button definiert und erzeugt den im Programmfenster angezeigten Button mit der Beschriftung 'Save', 
    mit dem der im Textfeld eingegebene Text dem ausgewählten Button zugewiesen wird.
    @param window Objekt der Klasse Window
    """
    def __init__(self, window):     
        self.window= window
        self.save_button= tk.ttk.Button(window.window, command= self.save_text, text= 'Speichern')
        self.save_button.grid(row=6, column=2)
        

    def save_text(self):       
        """
        Dem Button Save_button zugewiesenes Kommando, speichert den eingegebenen Text im Button.
        """
        text= self.window.text_field.text_field.get()
        is_command= self.window.command_checkbutton.checked.get()
        self.window.buttons[self.window.cur_button].change_text(text, is_command)


class Text_field (object):
    """
    Die Klasse Textfield definiert und erzeugt das im Programmfenster angezeigte Textfeld. Hier wird der Text eingegeben,
    der dem ausgewählten Button zugewiesen werden soll. Wird ein Button ausgewählt wird hier zudem der dem Button bisher
    zugeordnete Text angezeigt.
    @param window Objekt der Klasse Window
    """
    def __init__(self, window):
        self.text_field= tk.Entry(window.window) 
        self.text_field.grid(row= 6, column= 0, columnspan= 2)

    # Ändert den gegebenen Text, um Text des neu ausgewählten Buttons anzuzeigen       
    def update_text(self, text):
        #Leert das Feld
        self.text_field.delete(0,'end') 
        #Neuer Text
        self.text_field.insert(0,text)  
        


class Command_checkbutton(object):
    """
    Die Klasse Command_checkbutton definiert und erzeugt die Checkbox(ttk-Style) mit der festgelegt wird, ob der 
    dem ausgewählten Button zuzuweisende Text ein Tastatur-Kurzbefehl ist oder nicht.
    @param window Objekt der Klasse Window
    """
    def __init__(self, window):
        ##Variable, in der Zustand des Checkbuttons gespeichert wird
        self.checked= tk.IntVar()
        self.checkbutton= tk.ttk.Checkbutton(window.window, text= 'Command', variable= self.checked)
        self.checkbutton.grid(row=6, column= 3)

    #Ändert den Zustand, wird aufgerufen, wenn neuer Button ausgewählt wird  
    def update_checked(self,checked):
        self.checked.set(checked)


window= Window()