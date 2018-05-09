import tkinter as tk
import pyautogui as key

class Keypad(object):
    def __init__(self, root):
        self.keys=[
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D']
        ]
        for x in range(4):
            for y in range(4):
                self.create_button(name= self.keys[y][x], x=x, y=y)

    def create_button(self, name, x, y):        
            self.button=tk.Button(root, text= name)
            self.button.grid(row= y, column= x)

    

root = tk.Tk()
root.title("Keypad")


label = tk.Label(root,text="Button1")
label.grid(row=0, column=7)

entryb1= tk.Entry(root)
entryb1.grid(row=0,column=8)

keypad= Keypad(root)

b1 = tk.Button(root, text='set',command=root.destroy)
#b1.grid(row=1, column=7,columnspan=2, stick=W+E)

root.mainloop()