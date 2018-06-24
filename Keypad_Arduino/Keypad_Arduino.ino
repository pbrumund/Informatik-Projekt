//Bibliothek für Keypad
#include "Key.h"
#include "Keypad.h"
#include <SoftwareSerial.h>
#include "DumbServer.h"

//Anzahl der Reihen des Keypads
const byte ROWS = 4;
//Anzahl der Spalten des Keypads
const byte COLS = 4;
//Zeitpunkt, zu dem das nächste Testbyte gesendet wird, in ms
unsigned long next_send = 0;
//Wird auf wahr gesetzt, wenn Nachricht empfangen wird
bool receiving = false;


//Zahlen, die gesendet werden, wenn Taste gedrückt wird, Konfiguration des Keypads
//Eigentlich char, uint8_t hat jedoch selbe Länge
uint8_t keys[ROWS][COLS] = {
  {1, 2, 3, 4},
  {5, 6, 7, 8},
  {9, 10, 11, 12},
  {13, 14, 15, 16}
};

//Pins, an denen die Reihen des Keypads angeschlossen sind, Reihenfolge wie Anschlüsse an Keypad
byte rowPins[ROWS] = {4, 5, 6, 7};
//Pins, an denen die Spalten des Keypads angeschlossen sind, Reihenfolge wie Anschlüsse an Keypad
byte colPins[COLS] = {10, 11, 12, 13};


//Erstellt ein Keypad aus der Keypad-Bibliothek mit den gegebenen Belegungen, Reihen und Spalten
//Gibt später mit get_key aus, ob eine Taste gedrückt wurde
Keypad kpd = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS );

//Verbindet mit WLAN-Shield
SoftwareSerial esp_serial(3, 2);
//Erstellt Server
EspServer esp_server;

//Adresse des Resets, um bei Schließen der Verbindung am Computer neu zu starten und Abstürzen zu verhindern
void(*resetFunc)(void) = 0;

//Überprüft, ob der Computer Daten gesendet hat, wenn der String "off" gesendet wurde, wird der Arduino neu gestartet
void check_off_msg() {
  while (esp_server.available() || receiving) {
    receiving = true;
    String msg = esp_server.readStringUntil('\n');
    if (msg == "off") {
      resetFunc();
    }
  }
}

//Sendet den übermittelten Key (Nummer der Taste, deklariert in keys) an den Computer
void send_pressed_button(uint8_t key) {
  esp_server.println(key);
  //Debugging, nur für Serial Monitor
  Serial.println(key);
}

//Sendet ein "t" an den Computer, um mitzuteilen, dass Arduino noch online ist
void send_test() {
  esp_server.println("t");
  //Serial.println("t");
}

void setup()
{
  //Startet Verbindung über USB, um IP auszugeben, eventuell Debugging
  Serial.begin(9600);
  //Verbindet mit WLAN-Shield
  esp_serial.begin(9600);
  Serial.println("Starting server...");
  //Startet Server auf Port 30303 mit angegebener SSID und Passwort
  esp_server.begin(&esp_serial, "arduino", "password", 30303);
  Serial.println("...server is running");
  //Speichert die IP, um sie mitzuteilen
  char ip[16];
  esp_server.my_ip(ip, 16);
  //Gibt IP-Adresse aus
  Serial.print("My ip: ");
  Serial.println(ip);
}

void loop()
{
  //Überprüft, ob der Computer mit dem Server verbunden ist
  bool curr_connected = esp_server.connected();
  //Überprüft, ob eine Taste gedrückt wurde, falls dies der Fall ist, wird der in keys gespeicherte Wert in der Variable gespeichert
  uint8_t key = kpd.getKey();

  //Überprüft, ob Arduino sich neu starten soll
  check_off_msg();

  //Falls eine Taste gedrückt wurde und diese gesendt werden kann, wird sie dem Computer übermittelt
  if (key && curr_connected) {
    send_pressed_button(key);
  }

  //Falls der Zeitpunkt für das nächste Testbit erreicht ist, wird diese gesendet und next_send um 50ms erhöht
  if (millis() > next_send && curr_connected) {
    send_test();
    next_send = millis() + 50;
  }
/*
  if (!curr_connected)
  {
    Serial.println("no connection");
  }
*///Debugging
}
