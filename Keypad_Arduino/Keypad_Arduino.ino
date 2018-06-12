#include "Key.h"
#include "Keypad.h"
#include <SoftwareSerial.h>
#include "DumbServer.h"


const byte ROWS = 4;
const byte COLS = 4;
unsigned long next_send = 0;
bool receiving = false;


uint8_t keys[ROWS][COLS] = {
  {1, 2, 3, 4},
  {5, 6, 7, 8},
  {9, 10, 11, 12},
  {13, 14, 15, 16}
};

byte rowPins[ROWS] = {4, 5, 6, 7};
byte colPins[COLS] = {10, 11, 12, 13};

Keypad kpd = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS );

SoftwareSerial esp_serial(3, 2);
EspServer esp_server;

void(*resetFunc)(void) = 0;

void check_off_msg() {
  while (esp_server.available() || receiving) {
    receiving = true;
    String msg = esp_server.readStringUntil('\n');
    if (msg == "off") {
      resetFunc();
    }
  }
}

void send_pressed_button(uint8_t key) {
  esp_server.println(key);
  //Serial.println(key);
}

void send_test() {
  esp_server.println("t");
  //Serial.println("t");
}

void setup()
{
  Serial.begin(9600);
  esp_serial.begin(9600);
  Serial.println("Starting server...");
  esp_server.begin(&esp_serial, "FRITZ!Box Fon WLAN 7390", "byron1234", 30303);
  Serial.println("...server is running");
  /* Get and print the IP-Address the python program
     should connect to */
  char ip[16];
  esp_server.my_ip(ip, 16);

  Serial.print("My ip: ");
  Serial.println(ip);
}

void loop()
{
  bool curr_connected = esp_server.connected();
  uint8_t key = kpd.getKey();

  check_off_msg();

  if (key && curr_connected) {
    send_pressed_button(key);
  }

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
