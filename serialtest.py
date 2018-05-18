import serial
import tkinter as tk


arduino = serial.Serial('/dev/cu.usbmodem14311',9600,timeout=1)

def led_on():
    arduino.write(b'1')
def led_off():
    arduino.write(b'0')
def curseword():
    arduino.write(b'Spast')


controlwindow = tk.Tk()
controlwindow.title('Nur ein Test')

Button = tk.Button


btn1 = Button(controlwindow, text="ON", command =led_on)
btn2 = Button(controlwindow,text="OFF",command =led_off)
btn3 = Button(controlwindow,text="Curseword",command=curseword)

btn1.grid(row = 0,column = 1)
btn2.grid(row=1,column=1)
btn3.grid(row=2,column=1)
controlwindow.mainloop()