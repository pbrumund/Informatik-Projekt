import tkinter as tk
import pyautogui as key

Buttons= []
tk_Buttons= []
cur_button= 0
class Keypad(object):
     def __init__(self, Window):
        self.keys=[
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D'] 
        ]
        for y in range(4):
            for x in range(4):
                Buttons.append(Button(name= self.keys[y][x], x=x, y=y, index=x+(4*y), button_text= 'empty'))
        for i in range(16):
            tk_Buttons[i].config(command= Buttons[i].set_cur_button)
class Button (object):
    def __init__(self, name, x, y, index, button_text= 'empty'):
        tk_Buttons.append(tk.Button(Window, 
        text= name))
        tk_Buttons[index].grid(row= y, column= x)
        self.button_text= button_text
        self.index= index
    def change_text(self, new_text):
        self.button_text= new_text
    def print_text(self):
        print (self.button_text)
    def exec_command(self):
        pass    
    def get_text(self):
        return self.button_text
    def set_cur_button(self):
        global cur_button
        cur_button=self.index
        Text_field.update_text(self.button_text)
        #print (cur_button)
class Save_button (object):
    def __init__(self, Window):
        save_button= tk.Button(Window, command= Save_button.save_text, text= 'Save')
        save_button.grid(row=1, column=5)
    def save_text():
        global cur_button
        Buttons[cur_button].print_text()
        #print (cur_button)
class Text_field (object):
    def __init__(self, Window):
        self.text_field= tk.Entry(Window) #Entry ist im Gegensatz zu Text von Anfang an sichtbar.
        self.text_field.grid(row= 1, column= 4)
    def update_text(self, text):
        self.text_field.delete(0,'end')
        self.text_field.insert(0,text)

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
    
    
Window= tk.Tk()
Window.title('Keypad')
Keypad= Keypad(Window)
Save_button= Save_button(Window)
Submit_button=Submit_button(Window)
label1 = tk.Label(Window, text="Neue Belegung für Taste:")
label1.grid(row=0,column=4)
label2 = tk.Label(Window, text="Zu verändernde Taste:")
label2.grid(row=2,column=4)
Text_field= Text_field(Window)
Text_field2=Text_field2(Window)
Button.change_text(Buttons[3], new_text= 'test')
Button.change_text(Buttons[5], new_text= 'text')
Button.change_text(Buttons[0], new_text= r'\frac{}{}')
print(Buttons[3].get_text())
Window.mainloop()