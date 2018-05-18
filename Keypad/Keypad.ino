#include <Keypad.h>

const byte ROWS = 4;
const byte COLS = 4;

/*String keys[ROWS][COLS] = {
 {'0','1','2','3'},
 {'4','5','6','7'},
 {'8','9','10','11'},
 {'12','13','14','15'}
};*/

uint8_t keys[ROWS][COLS] = {
 {1,2,3,4},
 {5,6,7,8},
 {9,10,11,12},
 {13,14,15,16}
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
  uint8_t key = kpd.getKey();
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

