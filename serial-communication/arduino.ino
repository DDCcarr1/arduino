#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
JsonDocument json;
String inputData;

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
      
      const char* text = json["time"];
      lcd_reset();
      lcd.print(text);
      Serial.print(text);
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
}

void lcd_reset(){
  lcd.clear();
  lcd.home();
}
