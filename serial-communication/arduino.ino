#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
JsonDocument json;
String inputData;
const uint8_t degreesCelsius_ico[8] = {
  0b11100,
  0b10100,
  0b11100,
  0b00111,
  0b01000,
  0b01000,
  0b01000,
  0b00111
};
const byte degreesCelsius = 0;

void setup() {
  Serial.begin(9600);

  lcd_start();
}

void loop() {
  if(Serial.available() > 0){
      inputData = Serial.readStringUntil('\n');
      json.clear();

      DeserializationError error = deserializeJson(json, inputData);

      if(error) {
        lcd_reset();
        lcd.print("Error");
        Serial.print("Error: ");
        Serial.println(error.c_str());
        return;
      }
      
      const char* date = json["time"];
      const char* weather = json["weather"];
      const char* temp = json["temp"];
      lcd_reset();
      lcd.print(temp);
      lcd.write(0);
      lcd.print(" | ");
      lcd.print(weather);
      lcd.setCursor(0,1);
      lcd.print(date);
//f      Serial.print(text);
      Serial.println(" is now being displayed.");
  }
}


void lcd_start(){
  lcd.init();
  lcd.clear();
  lcd.backlight();
  lcd.noCursor();
  lcd.home();
  lcd.display();
  lcd.noBlink();
  lcd.createChar(degreesCelsius, degreesCelsius_ico);
}



void lcd_reset(){
  lcd.clear();
  lcd.home();
}
