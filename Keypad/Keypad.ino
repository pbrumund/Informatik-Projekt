#include <Keypad.h>

const byte ROWS = 4;
const byte COLS = 4;

char keys[ROWS][COLS] = {
 {'A','B','C','D'},
 {'E','F','G','H'},
 {'I','J','K','L'},
 {'M','N','O','X'}
};


byte rowPins[ROWS] = {7,6,5,4};
byte colPins[COLS] = {10,11,12,13};

Keypad kpd = Keypad(makeKeymap(keys), rowPins, colPins, ROWS,COLS );

 #define ledpin 13

 
void setup()
{
  pinMode(ledpin,OUTPUT);
  digitalWrite(ledpin, HIGH);
  Serial.begin(9600);
}

void loop()
{
  char key = kpd.getKey();
  if(key)  // Check for a valid key.
  {
    switch (key)
    {
      case '*':
        digitalWrite(ledpin, LOW);
        break;
      case '#':
        digitalWrite(ledpin, HIGH);
        break;
      default:
        Serial.println(key);
    }
  }
}

