char serialData;
int pin = 10;


void setup() {
    pinMode(pin, OUTPUT);
    Serial.begin(9600);
    Serial.println("###Ready###");
}

void loop() {
  /*if(Serial.available() > 0) {
        serialData= Serial.read();
        Serial.print(serialData);
  }
  if(serialData == '1'){
    digitalWrite(pin, HIGH);
  }
  else if(serialData == '0'){
    digitalWrite(pin, LOW);*/
Serial.println("a");
delay(500);

  }

    