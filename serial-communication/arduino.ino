const byte led = 13;
char input;

void setup() {
  pinMode(led, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0){
      input = Serial.read();

      if(input == '1'){
        digitalWrite(led, HIGH);
        Serial.println("ON");
      } else if(input == '0') {
        digitalWrite(led, LOW);
        Serial.println("OFF");
      }
  }
}
