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
        #command= Buttons[index].print_text(),
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
        #print (cur_button)
class Save_button (object):
    def __init__(self, Window):
        save_button= tk.Button(Window, command= Save_button.save_text, text= 'Save')
        save_button.grid(row=0, column=5)
    def save_text():
        global cur_button
        Buttons[cur_button].print_text()
        #print (cur_button)
class Text_field (object):
    def __init__(self, Window):
        text_field= tk.Text(Window, height= 1, width= 30)
        text_field.grid(row= 0, column= 4)
Window= tk.Tk()
Window.title('Keypad')
Keypad= Keypad(Window)
Save_button= Save_button(Window)
Text_field= Text_field(Window)
Button.change_text(Buttons[3], new_text= 'test')
Button.change_text(Buttons[5], new_text= 'text')
Button.change_text(Buttons[0], new_text= r'\frac{}{}')
print(Buttons[3].get_text())
Window.mainloop()