import tkinter as tk
import pyautogui as key
from tkinter import ttk

Buttons= []
cur_button= 0
class Keypad(object):   #Erzeugt die Buttons des Keypads
     def __init__(self, Window):
        self.keys=[     #Beschriftungen der Buttons
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D'] 
        ]
        for y in range(4):      #Erzeugt die Buttons
            for x in range(4):
                Buttons.append(Button(name= self.keys[y][x], x=x, y=y, index=x+(4*y)))  #Werden in Liste gespeichert
        
class Button (object):
    def __init__(self, name, x, y, index, button_text= ''):
        style= tk.ttk.Style()
        style2= tk.ttk.Style()

        #style.configure("Standard_Button.TButton", foreground="black", background="white")
        style2.configure("Active_Button.TButton", foreground="black", background="blue")
        self.button=tk.ttk.Button(Window, command= self.set_cur_button, text= name) #Erzeugt Button über tkinter
        self.button.grid(row= y, column= x)     
        self.button_text= button_text   #geespeicherter Text, der geändert werden kann
        self.index= index   #Position in der Liste
    def change_text(self, new_text):    #ändert den Text
        self.button_text= new_text
    #def print_text(self):
     #   print (self.button_text)
    def exec_command(self):
        pass    
    def get_text(self):     #Gibt den gespeicherten Text aus
        return self.button_text
    def set_cur_button(self):      #Setzt den angeklickten Button als aktuell ausgewählten Button, der bearbeitet werden soll
        global cur_button
        Buttons[cur_button].button.configure(style= "TButton")
        cur_button=self.index
        Buttons[cur_button].button.configure(style= "Active_Button.TButton")
        Text_field.update_text(self.button_text)      #Zeigt den Text des ausgewählten Buttons im Textfeld an
        #Text_field.text_field.icursor(0)
        

class Save_button (object):     #Button zum speichern
    def __init__(self, Window):     #Erzeut Button
        save_button= tk.ttk.Button(Window, command= Save_button.save_text, text= 'Save')
        save_button.grid(row=5, column=2)
    def save_text():       #Speichert den eingegebenen Text im Button
        global cur_button
        text= Text_field.text_field.get()
        Buttons[cur_button].change_text(text)
        
class Text_field (object):
    def __init__(self, Window):
        self.text_field= tk.Entry(Window) #Entry ist im Gegensatz zu Text von Anfang an sichtbar.
        self.text_field.grid(row= 5, column= 0, columnspan= 2)
    def update_text(self, text):# Ändert den gegebenen Text
        self.text_field.delete(0,'end') #Leert das Feld
        self.text_field.insert(0,text)  #Neuer Text

class Text_field2 (object):
    def __init__(self, Window):
        text_field2= tk.Entry(Window) 
        text_field2.grid(row= 3, column= 4)


class Submit_button (object):
    def __init__(self, Window):
        submit_button= tk.Button(Window, command= Submit_button.submit_text, text= 'Submit')
        submit_button.grid(row=3, column=5)
    def submit_text():
        pass #noch keine Funktion
    
    
Window= tk.Tk()     #Erzeut Fenster
Window.title('Keypad')



Keypad= Keypad(Window)  #Erzeugt Keypad
Save_button= Save_button(Window)  
#Submit_button=Submit_button(Window)
label1 = tk.Label(Window, text="Neue Belegung für Taste:")
label1.grid(row=4,column=0, columnspan= 2)
#label2 = tk.Label(Window, text="Zu verändernde Taste:")
#label2.grid(row=2,column=4)
Text_field= Text_field(Window)
#Text_field2= Text_field2(Window)

Window.mainloop()