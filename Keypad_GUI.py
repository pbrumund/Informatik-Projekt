import tkinter as tk
import pyautogui as key
from tkinter import ttk, filedialog
import socket as so
import json


class Arduino(object):
    """
    """
    def __init__(self, window):
        """
        """
        self.window= window
        
        self.buffer= bytes()
        self.connected= False

        self.connect_window= Connect_window(self)

    def __del__(self):
        self.close()

    def send_off(self):
        """
        Sendet Nachricht an den Arduino, dass Verbndung geschlossen werden soll,
        dieser startet sich neu, um nicht abzustürzen.
        """
        try:
            self.socket.send('off'.encode('utf-8') + b'\n')
            self.window.window.after(20, self.send_off) #Nachricht wird nicht jedes mal empfangen, also wird Text mehrmals gesendet
        except:
            pass
        

    def close(self):
        self.connected= False
        try:
            self.window.window.after_cancel(self.send_off)
            self.socket.close()
            print('Tried to close the connection')
        except:
            print('Was not able to close the connection')
        

    def new_connection(self, host, port):
        """
        Methode, die die Verbindung mit dem Arduino herstellt.
        """
        self.socket= so.socket()
        try:
            self.socket.connect((host, port))
            self.socket.setblocking(False)

            self.errors= 0
            self.connected= True
            self.listen()            
        except:
            self.connect_window= Connect_window(self)
            print('Error')
        
    def listen(self):
        """
        Empfängt vom Arduino versendete Daten und stellt fest, ob 
        überhaupt eine fehlerfreie Verbindung mit dem Arduino besteht.
        """
        try:
            read = self.socket.recv(1024)
            self.buffer+= read
            
        except:
            self.errors+= 1      
            if self.errors>500: 
                """   
                Wenn die Anzahl der gescheiterten Verbindungsversuche 500 übersteigt,
                wird eine Fehlermeldung ausgegeben und das Verbindungsfenster wieder aufgerufen.
                """
                print('Connection failed') 
                self.close()
                self.connect_window= Connect_window(self)
                        
        while b'\n' in self.buffer:
            """

            """
            try:
                read, self.buffer= self.buffer.split(b'\n')
                read= read.decode('utf-8').strip()

                if read=="t":
                    """
                    """
                    self.errors= 0
                else:
                    try:
                        """
                        """
                        i= int(read)-1
                        if 0<=i<=15:
                            self.window.buttons[i].exec_command()
                    except ValueError:
                        pass
            except:
                pass
            
        if self.connected:
            self.window.window.after(5,self.listen)


class Connect_window(object):
    """
    Definiert und erzeugt das Verbindungsfenster, dass zeitgleich mit dem Aufruf des eigentlichen
    Bedienfensters aufgerufen wird um die IP-Adresse und den Port für die aufzubauende 
    Verbindung festzulegen. 
    """
    def __init__(self, arduino):
        self.arduino= arduino
        self.connect_window= tk.Toplevel()
        self.connect_window.attributes("-topmost", True)
       
        self.connect_button= tk.ttk.Button(self.connect_window, text= 'Connect', command= self.connect)
        self.ip_label= tk.Label(self.connect_window, text= "IP-Adresse:")
        self.ip_field= tk.Entry(self.connect_window)
        self.port_label= tk.Label(self.connect_window, text= "Port:")
        self.port_field= tk.Entry(self.connect_window)
        
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
        an die "new-connection" Methode der Klasse Arduino weitergibt.
        """
        try:
            host= self.ip_field.get()
            port= int(self.port_field.get())
            self.arduino.new_connection(host, port)
            self.__del__()
        except ValueError:
            print('Value Error')


class Window(object):
    """
    Definiert und erzeugt das Hauptfenster. Inhalte des Hauptfensters sind:
    Keypad(keypad), Textfeld(text_field) , Speicherknopf(save_button) und Checkbox(command_checkbutton)
    Profilspeicherknopf(json_button), Profilladeknopf(load_button) und ein Textfeld um das zu 
    ladende/speichernde Profil auszuwählen/anzulegen(save_text_field).
    """
    def __init__(self):
        self.window= tk.Tk()
        self.window.title('Keypad')
        self.window.protocol("WM_DELETE_WINDOW", self.on_closed)

        self.cur_button= 0
        self.buttons= []
                
        self.label= tk.Label(self.window, text="Neue Belegung für Taste:") 
        self.label.grid(row=5,column=0, columnspan= 2)

        self.text_field= Text_field(self)
        self.command_checkbutton= Command_checkbutton(self)
        self.save_button= Save_button(self)
        self.keypad= Keypad(self)  #Erzeugt Keypad
        self.json_save_button = Json_save_button(self)
        self.json_load_button = Json_load_button(self)
        self.arduino= Arduino(self)
                         
        self.window.mainloop()

    def on_closed(self):
        try:
            self.arduino.send_off()
        except AttributeError:
            pass
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
        self.keys=[     
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D'] 
        ]

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
    def __init__(self, window, label, x, y, index):
        self.window= window
        self.index= index   #Position in der Liste
        self.is_command= 0      
        self.button_text= ''   #geespeicherter Text, der geändert werden kann

        style= tk.ttk.Style()
        style.configure("Active_Button.TButton", foreground="black", background="blue")

        self.button=tk.ttk.Button(self.window.window, command= self.set_cur_button, text= label) #Erzeugt Button über tkinter
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
            Mit einer For-Schleife , 
            """
            command_keys= self.button_text.split()
            for command_key in command_keys:
                key.keyDown(command_key, pause=0.1)
            for command_key_up in reversed(command_keys):    
                key.platformModule._keyUp(command_key_up)   #Normales keyUp funktioniert nicht
        else:              
            """
            Falls der Text kein Tastatur-Kurzbefehl ist, wird dieser einfach ausgegeben.
            """
            key.typewrite(self.button_text, interval= 0.00)

    def set_cur_button(self): 
        """
        Setzt den angeklickten Button als aktuell ausgewählten Button, der bearbeitet werden soll.
        Der dem Button aktuell zugewiesene Text, wird im Textfeld angezeigt.
        """
        self.window.buttons[self.window.cur_button].button.configure(style= "TButton")
        self.window.cur_button=self.index
        self.window.buttons[self.window.cur_button].button.configure(style= "Active_Button.TButton")
        self.window.text_field.update_text(self.button_text)      
        self.window.command_checkbutton.update_checked(self.is_command)


class Json_save_button (object):
    """
    Definiert und erzeugt einen Button um das Speichern von Profilen zu ermöglichen.
    Den gewünschten Dateinamen für das Profil bezieht vom "Save_text_field" .
    """
    def __init__(self,window):
        self.window= window
        self.json_button = tk.ttk.Button(window.window, command=self.save_json,text= 'Profil speichern')
        self.json_button.grid(row=0, column=0, columnspan= 2, sticky= tk.W+tk.E)
        

    def save_json(self):
        """
        Methode, mit der der den Einzelnen Tasten zugewiesene Text und der jeweilige
        Status(Bezogen auf 'Is_command') in einer Datei(xy.json) gespeichert wird.
        Hierfür ein Dateiname(xy) aus dem "Save_text_field" bezogen, eine Liste(json_list)
        mit den Tastenbelegungen angelegt und eine Liste(is_command_list) mit dem Status 
        der der Tasten(bezogen auf die "Command"-Checkbox) angelegt.
        Die beiden Listen werden in ein Dictionary(write_to_json) zusammengefügt und 
        im Json-Format gespeichert.
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
    Den Namen des zu öffnenden Profils bezieht er aus dem "Save_text_field" .
    """
    def __init__(self,window):
        self.window= window
        self.load_button = tk.ttk.Button(window.window, command = self.load,text= 'Profil laden')
        self.load_button.grid(row=0, column=2, columnspan= 2, sticky= tk.W+tk.E)

    def load(self):

        """
        Die im Profil im Json-Format gespeicherten Daten werden in ein Dictionary("dictionary") geladen und
        anschließend in zwei Listen("Content" und "Is_Command")  aufgeteilt. Anschließend wird den Tasten der 
        im jeweiligen Profil abgelegte Inhalt und Status mit einer For-Schleife zugewiesen. 
        """
        
        content = []
        iscmd = []

        filename= tk.filedialog.askopenfilename(filetypes= [("JSON File","*.json")])
        
        if filename:
            with open(filename) as file:
                try:
                    dictionary = json.load(file)
                    for i in range(16):
                        content.append(dictionary["Content"+str(i)])
                        iscmd.append(dictionary["Is_Command"+str(i)])
            
                    for button in self.window.buttons:
                        button.button_text = content[button.index]
                        button.is_command = iscmd[button.index]

                    self.window.buttons[0].set_cur_button()
                except TypeError:
                    print('Wrong Format')


class Save_button (object):     
    """
    Die Klasse Save_button definiert und erzeugt den im Programmfenster angezeigten Button mit der Beschriftung 'Save', 
    mit dem der im Textfeld eingegebene Text dem ausgewählten Button zugewiesen wird. 
    """
    def __init__(self, window):     
        self.window= window
        self.save_button= tk.ttk.Button(window.window, command= self.save_text, text= 'Speichern')
        self.save_button.grid(row=6, column=2)
        

    def save_text(self):       #Speichert den eingegebenen Text im Button
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
    """
    def __init__(self, window):
        self.text_field= tk.Entry(window.window) 
        self.text_field.grid(row= 6, column= 0, columnspan= 2)
        
    def update_text(self, text):# Ändert den gegebenen Text
        self.text_field.delete(0,'end') #Leert das Feld
        self.text_field.insert(0,text)  #Neuer Text


class Command_checkbutton(object):
    """
    Die Klasse Command_checkbutton definiert und erzeugt die Checkbox(ttk-Style) mit der festgelegt wird, ob der 
    dem ausgewählten Button zuzuweisende Text ein Tastatur-Kurzbefehl ist oder nicht.
    """
    def __init__(self, window):
        self.checked= tk.IntVar()
        self.checkbutton= tk.ttk.Checkbutton(window.window, text= 'Command', variable= self.checked)
        self.checkbutton.grid(row=6, column= 3)
        
    def update_checked(self,checked):
        self.checked.set(checked)


window= Window()