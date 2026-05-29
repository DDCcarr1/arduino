#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

String received;

void setup() {
  Serial.begin(9600);
  lcd_start();
}

void loop() {
  if(Serial.available() > 0){
      received = Serial.readStringUntil('\n');

      if (received != ""){
        lcd_reset();
        lcd.print(received);
        Serial.print(received);
      }
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
  lcd.backlight();
  lcd.noCursor();
  lcd.home();
  lcd.display();
  lcd.noBlink();
}
