import serial
import tkinter as tk


t = 0
arduino = serial.Serial('/dev/cu.usbmodem14311',9600,timeout=1)

def listen():
    read = arduino.readline()
    if (read):
        print("Aktion registriert")
        

while t < 100000000:
    listen()
    t+=1
