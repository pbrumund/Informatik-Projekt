import tkinter as tk
import pyautogui as key
import serial
from tkinter import ttk
import socket as so
import time

Buttons= []
cur_button= 0

class Arduino(object):
    def __init__(self, window):
        #self.arduino = serial.Serial('COM7',9600,timeout=0.1)
        self.window= window

        #self.socket= so.socket()
        self.connect_window= Connect_window(self)

        self.errors= 0
        self.buffer= bytes()

        

    def close(self):
        self.socket.close()

    def new_connection(self, host, port):
        self.socket= so.socket()
        self.socket.connect((host, port))
        self.socket.setblocking(False)

        self.errors= 0
        self.listen()
        
    def listen(self):
        try:
            read = self.socket.recv(1024)
            self.buffer+= read
            
        except so.error:
            self.errors+= 1
        
            if self.errors>100:
                print('Connection failed')
                self.close()
                self.connect_window= Connect_window(self)
                        
        while b'\n' in self.buffer:
            read, self.buffer= self.buffer.split(b'\n')
            read= read.decode('utf-8').strip()

            if read=="t":
                self.errors= 0
            else:
                i= int(read)-1
                if 0<=i<=15:
                    Buttons[i].exec_command()
            
        if self.errors<= 100:
            self.window.after(10,self.listen)
       
class Connect_window(object):
    def __init__(self, arduino):
        self.arduino= arduino
        self.connect_window= tk.Toplevel()
        self.connect_button= tk.ttk.Button(self.connect_window, text= 'Connect', command= self.connect)
        self.ip_field= tk.Entry(self.connect_window)
        self.port_field= tk.Entry(self.connect_window)
        
        self.ip_field.grid(column= 0, row= 0)
        self.port_field.grid(column= 0, row= 1)
        self.connect_button.grid(column= 0, row= 2)

        self.ip_field.insert(0, 'Enter IP-Adress')
        self.port_field.insert(0, 'Enter Port')

    def __del__(self):
        self.connect_window.destroy()

    def connect(self):
        host= self.ip_field.get()
        port= int(self.port_field.get())
        self.arduino.new_connection(host, port)
        self.__del__()


class Window(object):
    def __init__(self):
        self.window= tk.Tk()
                
        self.label1 = tk.Label(self.window, text="Neue Belegung für Taste:")
        self.label1.grid(row=4,column=0, columnspan= 2)
        self.text_field= Text_field(self.window)
        self.command_checkbutton= Command_checkbutton(self.window)
        self.save_button= Save_button(self.window, self.text_field, self.command_checkbutton)
        self.keypad= Keypad(self.window, self.text_field, self.command_checkbutton)  #Erzeugt Keypad



        #host= input('Hostname: ')
        #port= input('Port: ')

        self.arduino= Arduino(self.window)                
        self.window.mainloop()
    
            

class Keypad(object):   #Erzeugt die Buttons des Keypads
     def __init__(self, window, text_field, command_checkbutton):
        self.keys=[     #Beschriftungen der Buttons
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D'] 
        ]
        for y in range(4):      #Erzeugt die Buttons
            for x in range(4):
                Buttons.append(Button(window, text_field, command_checkbutton, name= self.keys[y][x], x=x, y=y, index=x+(4*y)))  #Werden in Liste gespeichert
        
class Button (object):
    def __init__(self, window, text_field, command_checkbutton, name, x, y, index):
        style= tk.ttk.Style()
        style.configure("Active_Button.TButton", foreground="black", background="blue")
        self.button=tk.ttk.Button(window, command= self.set_cur_button, text= name) #Erzeugt Button über tkinter
        self.button.grid(row= y, column= x)     
        self.button_text= ''   #geespeicherter Text, der geändert werden kann

        self.index= index   #Position in der Liste
        self.window= window
        self.text_field= text_field
        self.command_checkbutton= command_checkbutton
        self.is_command= 0

    def change_text(self, new_text, is_command):    #ändert den Text
        self.button_text= new_text
        self.is_command= is_command
        
    def exec_command(self):
        if self.is_command:     
            #Führt Tastenkombination aus
            command_keys= self.button_text.split()
            for command_key in command_keys:
                key.keyDown(command_key, pause=0.1)
            for command_key_up in reversed(command_keys):    
                key.platformModule._keyUp(command_key_up)   #Normales keyUp funktioniert nicht
        else:              
            #gibt Text ein
            key.typewrite(self.button_text, interval= 0.00)
        
    def get_text(self):     #Gibt den gespeicherten Text aus
        return self.button_text

    def set_cur_button(self):      #Setzt den angeklickten Button als aktuell ausgewählten Button, der bearbeitet werden soll
        global cur_button
        Buttons[cur_button].button.configure(style= "TButton")
        cur_button=self.index
        Buttons[cur_button].button.configure(style= "Active_Button.TButton")
        self.text_field.update_text(self.button_text)      #Zeigt den Text des ausgewählten Buttons im Textfeld an
        self.command_checkbutton.update_checked(self.is_command)

class Save_button (object):     #Button zum speichern
    def __init__(self, window, text_field, command_checkbutton):     #Erzeut Button
        save_button= tk.ttk.Button(window, command= self.save_text, text= 'Save')
        save_button.grid(row=5, column=2)
        self.text_field= text_field
        self.command_checkbutton= command_checkbutton

    def save_text(self):       #Speichert den eingegebenen Text im Button
        global cur_button
        text= self.text_field.text_field.get()
        is_command= self.command_checkbutton.checked.get()
        Buttons[cur_button].change_text(text, is_command)

        
class Text_field (object):
    def __init__(self, window):
        self.text_field= tk.Entry(window) #Entry ist im Gegensatz zu Text von Anfang an sichtbar.
        self.text_field.grid(row= 5, column= 0, columnspan= 2)
        
    def update_text(self, text):# Ändert den gegebenen Text
        self.text_field.delete(0,'end') #Leert das Feld
        self.text_field.insert(0,text)  #Neuer Text

class Command_checkbutton(object):
    def __init__(self, window):
        self.checked= tk.IntVar()
        self.checkbutton= tk.ttk.Checkbutton(window, text= 'Command', variable= self.checked)
        self.checkbutton.grid(row=5, column= 3)
        
    def update_checked(self, checked):
        self.checked.set(checked)

window= Window()  

