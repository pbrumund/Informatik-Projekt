import tkinter as tk
import pyautogui as key
import serial
from tkinter import ttk
import socket as so

Buttons= []
cur_button= 0

#not_working_keys= ['ü','ö','ä','Ü','Ö','Ä','^','ß','´','°','§','²','³','{','}','+','~','#','@','€','<','|']
#windows_commands= ['ü','ö','ä','Ü','Ö','','','','','^','','ctrl alt 2','ctrl alt 3','ctrl alt 7','ctrl alt 0','','ctrl alt +',
#'','ctrl alt q','ctrl alt e','','ctrl alt <']


class Arduino(object):
    def __init__(self, window):
        self.arduino = serial.Serial('COM7',9600,timeout=0.1)
        self.window= window


    def listen(self):
        read = self.arduino.readline()
        if (read):
            i= int(read)-1
            Buttons[i].exec_command()
        self.window.after(10,self.listen)
        

class Window(object):
    def __init__(self):
        self.window= tk.Tk()

        #self.update_keys()
                
        self.label1 = tk.Label(self.window, text="Neue Belegung für Taste:")
        self.label1.grid(row=4,column=0, columnspan= 2)
        self.text_field= Text_field(self.window)
        self.save_button= Save_button(self.window, self.text_field)  
        self.keypad= Keypad(self.window, self.text_field)  #Erzeugt Keypad

        self.arduino= Arduino(self.window)
        self.arduino.listen()
        
        self.window.mainloop()
    
            

class Keypad(object):   #Erzeugt die Buttons des Keypads
     def __init__(self, window, text_field):
        self.keys=[     #Beschriftungen der Buttons
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D'] 
        ]
        for y in range(4):      #Erzeugt die Buttons
            for x in range(4):
                Buttons.append(Button(window, text_field, name= self.keys[y][x], x=x, y=y, index=x+(4*y)))  #Werden in Liste gespeichert
        
class Button (object):
    def __init__(self, window, text_field, name, x, y, index, button_text= ''):
        style= tk.ttk.Style()
        style.configure("Active_Button.TButton", foreground="black", background="blue")
        self.button=tk.ttk.Button(window, command= self.set_cur_button, text= name) #Erzeugt Button über tkinter
        self.button.grid(row= y, column= x)     
        self.button_text= button_text   #geespeicherter Text, der geändert werden kann
        self.index= index   #Position in der Liste
        self.window= window
        self.text_field= text_field

    def change_text(self, new_text):    #ändert den Text
        self.button_text= new_text
        
    def exec_command(self):
        key.typewrite(self.button_text, interval= 0.01)
        
    def get_text(self):     #Gibt den gespeicherten Text aus
        return self.button_text

    def set_cur_button(self):      #Setzt den angeklickten Button als aktuell ausgewählten Button, der bearbeitet werden soll
        global cur_button
        Buttons[cur_button].button.configure(style= "TButton")
        cur_button=self.index
        Buttons[cur_button].button.configure(style= "Active_Button.TButton")
        self.text_field.update_text(self.button_text)      #Zeigt den Text des ausgewählten Buttons im Textfeld an
              

class Save_button (object):     #Button zum speichern
    def __init__(self, window, text_field):     #Erzeut Button
        save_button= tk.ttk.Button(window, command= self.save_text, text= 'Save')
        save_button.grid(row=5, column=2)
        self.text_field= text_field

    def save_text(self):       #Speichert den eingegebenen Text im Button
        global cur_button
        text= self.text_field.text_field.get()
        Buttons[cur_button].change_text(text)
        
class Text_field (object):
    def __init__(self, Window):
        self.text_field= tk.Entry(Window) #Entry ist im Gegensatz zu Text von Anfang an sichtbar.
        self.text_field.grid(row= 5, column= 0, columnspan= 2)
        
    def update_text(self, text):# Ändert den gegebenen Text
        self.text_field.delete(0,'end') #Leert das Feld
        self.text_field.insert(0,text)  #Neuer Text


    
window= Window()  
