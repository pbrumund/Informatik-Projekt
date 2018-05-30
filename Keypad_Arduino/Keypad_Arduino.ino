#include "Key.h"
#include "Keypad.h"
#include <SoftwareSerial.h>
#include "DumbServer.h"


const byte ROWS = 4;
const byte COLS = 4;
unsigned long next_send = 0;

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

void setup()
{
  Serial.begin(9600);
  esp_serial.begin(9600);
  Serial.println("Starting server...");
  esp_server.begin(&esp_serial, "arduino", "password", 30303);
  Serial.println("...server is running");


  /* Get and print the IP-Address the python program
   * should connect to */
  char ip[16];
  esp_server.my_ip(ip, 16);

  Serial.print("My ip: ");
  Serial.println(ip);
}

void loop()
{
  if(millis()>next_send){
    uint8_t key = kpd.getKey();
    bool curr_connected= true;//esp_server.connected();
    if (key && curr_connected) // Check for a valid key.
    {
     esp_server.println(key);
     Serial.println(key);
    }
    else if (curr_connected)
    {
     esp_server.println("t");
    //Serial.println("t");
    }
    next_send+= 10;
    esp_server.available();
  }
  
}

