import tkinter as tk
import json 

filename = 'profil.json'

a = input("a>>")
b = input("b>>")
c = input("c>>")
d = "*"

class Window(object):
    def __init__(self): 
        self.window= tk.Tk()
        self.window.title("Json")
        

        self.text_field= Text_field(self.window)
        self.text_field1= Text_field(self.window)
        self.text_field2= Text_field(self.window)
        self.save_button= Save_button(self.window)
        self.save_button1= Save_button(self.window)
        self.save_button2= Save_button(self.window)
        self.json_button = Json_button(self.window)
        self.load_button = Load_button(self.window)
        

        self.window.mainloop()

class Save_button (object):     #Button zum speichern
    def __init__(self, window):     #Erzeut Button
        save_button= tk.Button(window, command= self.save_text, text= 'Save')
        save_button1 = tk.Button(window, command=self.save_text, text = 'Save')
        save_button2 = tk.Button(window, command=self.save_text, text = 'Save')
        self.text_field= Text_field(window)
        save_button.grid(row=1, column=2)
        save_button1.grid(row=2,column=2)
        save_button2.grid(row=3,column=2)

    def save_text(self):           
        pass

class Json_button (object):
    def __init__(self,window):
        json_button = tk.Button(window, command=self.save_json,text= 'Profil Speichern')
        json_button.grid(row=4,column=2)

    def save_json(self):
        with open(filename,'w') as file:
            json.dump(d,file)
            json.dump(a,file)
            json.dump(d,file)
            json.dump(b,file)
            json.dump(d,file)
            json.dump(c,file)
            json.dump(d,file)

class Load_button (object):
    def __init__(self,window):
        load_button = tk.Button(window, command = self.load_json,text = 'Profil Laden')
        load_button.grid(row=5,column=2)

    def load_json(self):
        a = json.load(filename)
            

class Text_field (object):
    def __init__(self, window):
        self.text_field= tk.Entry(window) #Entry ist im Gegensatz zu Text von Anfang an sichtbar.
        self.text_field2= tk.Entry(window)
        self.text_field1 = tk.Entry(window)
        self.text_field.insert(1,a)
        self.text_field1.insert(1,b)
        self.text_field2.insert(1,c)
        self.text_field.grid(row= 1, column= 1, columnspan= 1)
        self.text_field1.grid(row = 2, column= 1, columnspan= 1)
        self.text_field2.grid(row = 3, column=1, columnspan= 1)
        



window= Window()  