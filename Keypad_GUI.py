import tkinter as tk
import pyautogui as key
import serial
from tkinter import ttk
import socket as so
import time

class Arduino(object):
    def __init__(self, window):
        self.window= window
        
        self.buffer= bytes()
        self.connected= False

        self.connect_window= Connect_window(self)
       
    #def __del__(self):
     #   try:
      #      self.close()
       # except OSError:
        #    pass
        

    def close(self):
        self.connected= False
        #try:
        off_msg= 'off'
        self.socket.send(off_msg.encode('utf-8') + b'\n')
        time.sleep(0.05)
        try:
            self.socket.recv(1024)
        except:
            pass
        time.sleep(0.2)
        #self.socket.close()
        print('Tried to close the connection')
        #except:
        #    print('Was not able to close the connection')
        

    def new_connection(self, host, port):
        self.socket= so.socket()
        try:
            self.socket.connect((host, port))
            self.socket.setblocking(False)

            self.errors= 0
            self.connected= True
            self.listen()            
        except OSError:
            self.connect_window= Connect_window(self)
            print('Error')
        
    def listen(self):
        try:
            read = self.socket.recv(1024)
            self.buffer+= read
            
        except:
            self.errors+= 1
        
            if self.errors>500:
                print('Connection failed')
                self.close()
                self.connect_window= Connect_window(self)
                        
        while b'\n' in self.buffer:
            read, self.buffer= self.buffer.split(b'\n')
            read= read.decode('utf-8').strip()

            if read=="t":
                self.errors= 0
            else:
                try:
                    i= int(read)-1
                    if 0<=i<=15:
                        self.window.buttons[i].exec_command()
                except ValueError:
                    pass
            
        if self.connected:
            self.window.window.after(5,self.listen)
       
class Connect_window(object):
    def __init__(self, arduino):
        self.arduino= arduino
        self.connect_window= tk.Toplevel()
        self.connect_window.attributes("-topmost", True)
       
        self.connect_button= tk.ttk.Button(self.connect_window, text= 'Connect', command= self.connect)
        self.ip_label= tk.Label(self.connect_window, text= "Enter IP-Adress:")
        self.ip_field= tk.Entry(self.connect_window)
        self.port_label= tk.Label(self.connect_window, text= "Enter Port:")
        self.port_field= tk.Entry(self.connect_window)
        
        self.ip_label.grid(column= 0, row= 0)
        self.ip_field.grid(column= 1, row= 0)
        self.port_label.grid(column= 0, row= 1)
        self.port_field.grid(column= 1, row= 1)
        self.connect_button.grid(column= 1, row= 2)

    def __del__(self):
        try:
            self.connect_window.destroy()
        except:
            pass
        

    def connect(self):
        host= self.ip_field.get()
        port= int(self.port_field.get())
        self.arduino.new_connection(host, port)
        self.__del__()


class Window(object):
    def __init__(self):
        self.window= tk.Tk()
        self.window.title('Keypad')
        self.window.protocol("WM_DELETE_WINDOW", self.on_closed)

        self.cur_button= 0
        self.buttons= []
                
        self.label= tk.Label(self.window, text="Neue Belegung für Taste:")
        self.label.grid(row=4,column=0, columnspan= 2)
        self.text_field= Text_field(self)
        self.command_checkbutton= Command_checkbutton(self)
        self.save_button= Save_button(self, self.text_field, self.command_checkbutton)
        self.keypad= Keypad(self, self.text_field, self.command_checkbutton)  #Erzeugt Keypad

        self.arduino= Arduino(self)
                 
        self.window.mainloop()

    def on_closed(self):
        self.arduino.close()
        time.sleep(1)
        self.__del__()

    def __del__(self):
        #self.arduino.close()
        #time.sleep(1)
        try:
            self.window.destroy()
        except:
            pass
            

class Keypad(object):   #Erzeugt die Buttons des Keypads
     def __init__(self, window, text_field, command_checkbutton):
        self.window= window
        self.keys=[     #Beschriftungen der Buttons
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D'] 
        ]

        for y in range(4):      #Erzeugt die Buttons
            for x in range(4):
                self.window.buttons.append(Button(self.window, text_field, command_checkbutton, name= self.keys[y][x], x=x, y=y, index=x+(4*y)))  #Werden in Liste gespeichert
        
class Button (object):
    def __init__(self, window, text_field, command_checkbutton, name, x, y, index):
        self.window= window
        self.index= index   #Position in der Liste
        self.text_field= text_field
        self.command_checkbutton= command_checkbutton
        self.is_command= 0
        self.button_text= ''   #geespeicherter Text, der geändert werden kann

        style= tk.ttk.Style()
        style.configure("Active_Button.TButton", foreground="black", background="blue")

        self.button=tk.ttk.Button(self.window.window, command= self.set_cur_button, text= name) #Erzeugt Button über tkinter
        self.button.grid(row= y, column= x)     
         
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

    def set_cur_button(self):      #Setzt den angeklickten Button als aktuell ausgewählten Button, der bearbeitet werden soll
        self.window.buttons[self.window.cur_button].button.configure(style= "TButton")
        self.window.cur_button=self.index
        self.window.buttons[self.window.cur_button].button.configure(style= "Active_Button.TButton")
        self.text_field.update_text(self.button_text)      #Zeigt den Text des ausgewählten Buttons im Textfeld an
        self.command_checkbutton.update_checked(self.is_command)

class Save_button (object):     #Button zum speichern
    def __init__(self, window, text_field, command_checkbutton):     #Erzeut Button
        self.window= window
        self.save_button= tk.ttk.Button(window.window, command= self.save_text, text= 'Save')
        self.save_button.grid(row=5, column=2)
        self.text_field= text_field
        self.command_checkbutton= command_checkbutton

    def save_text(self):       #Speichert den eingegebenen Text im Button
        text= self.text_field.text_field.get()
        is_command= self.command_checkbutton.checked.get()
        self.window.buttons[self.window.cur_button].change_text(text, is_command)

        
class Text_field (object):
    def __init__(self, window):
        self.text_field= tk.Entry(window.window) #Entry ist im Gegensatz zu Text von Anfang an sichtbar.
        self.text_field.grid(row= 5, column= 0, columnspan= 2)
        
    def update_text(self, text):# Ändert den gegebenen Text
        self.text_field.delete(0,'end') #Leert das Feld
        self.text_field.insert(0,text)  #Neuer Text

class Command_checkbutton(object):
    def __init__(self, window):
        self.checked= tk.IntVar()
        self.checkbutton= tk.ttk.Checkbutton(window.window, text= 'Command', variable= self.checked)
        self.checkbutton.grid(row=5, column= 3)
        
    def update_checked(self, checked):
        self.checked.set(checked)

window= Window()