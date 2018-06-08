#include "Key.h"
#include "Keypad.h"
#include <SoftwareSerial.h>
#include "DumbServer.h"


const byte ROWS = 4;
const byte COLS = 4;
unsigned long next_send = 0;
bool closed = 0;
bool receiving = 0;

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

void setup()
{
  Serial.begin(9600);
  esp_serial.begin(9600);
  Serial.println("Starting server...");
  esp_server.begin(&esp_serial, "arduino", "password", 30303);
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

  uint8_t key = kpd.getKey();
  bool curr_connected = esp_server.connected();
  while (esp_server.available() || receiving) {
    //resetFunc();
    receiving = true;
    String msg = esp_server.readStringUntil('\n');
    Serial.println("Read message");
    if (msg == "off") {
      closed = 1;
      //next_send = millis() + 200;
      delay(200);
      Serial.println("Tried to close the connection");
      receiving = false;
      resetFunc();
      }
    else{
      Serial.println(msg);
    }
  }
  if(closed){
    curr_connected = false;
  }


  if (key && curr_connected) // Check for a valid key.
  {
    esp_server.println(key);
    Serial.println(key);
  }
  if (millis() > next_send && curr_connected) {
    if (esp_server.connected()) {
      esp_server.println("t");
      Serial.println("t");
    }

    //Serial.println(millis());
    next_send = millis() + 50;
    //esp_server.available();

  }
  
  if (!curr_connected) {
    Serial.println("no connection");
  }
  
}

