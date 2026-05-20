// ----- RTC SETUP ----- //
#include <Wire.h>
#include "RTClib.h"
RTC_DS3231 rtc;

// ----- LCD SETUP ----- //
#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 10, 9, 8, 7);

// ----- VARIABLES ----- //
// --- dst --- //
bool dstCurrent = false;

// --- time/date --- //
int dayI, monthI, hourI, minuteI, secondI;
String day, month, year, hour, minute, second;

// --- set time --- //
unsigned long setLast = 0;
const int setDelay = 1000;

// --- read time --- //
unsigned long readLast = 0;
const int readDelay = 1000;

// --- lcd print --- //
unsigned long lcdLast = 0;
const int lcdDelay = 500;

void setup() {
  serialStart();

  lcd.begin(16, 2);
  lcdStart();

  rtcStart();
}

void loop() {
  timeSet();
  timeLCD();

  dstCheck();
}

void dstCheck() {
  DateTime now = rtc.now();

  // Spring Forward: 2nd Sunday in March, 2:00 AM
  if (now.month() == 3 && now.dayOfTheWeek() == 0 && now.day() >= 8 && now.day() <= 14 && now.hour() == 2 && !dstCurrent) {
    print("Setting to Daylight Saving Time");
    rtc.adjust(now + TimeSpan(0, 1, 0, 0));
    dstCurrent = true;
    print("Set to Daylight Saving Time");
  }

  // Fall Back: 1st Sunday in November, 2:00 AM
  if (now.month() == 11 && now.dayOfTheWeek() == 0 && now.day() <= 7 && now.hour() == 2 && dstCurrent) {
    print("Setting to Standard Time");
    rtc.adjust(now - TimeSpan(0, 1, 0, 0));
    dstCurrent = false;
    print("Set to Standard Time");
  }
}

void lcdStart() {
  print("Starting LCD");
  lcdReset();
  lcd.print("Starting.");
  delay(200);
  lcdReset();
  lcd.print("Starting..");
  delay(200);
  lcdReset();
  lcd.print("Starting...");
  delay(200);
  lcdReset();
  print("Started LCD");
}

void lcdReset() {
  lcd.clear();
  lcd.home();
}

void serialStart() {
  Serial.begin(9600);
  for (int i = 0; i < 10; i++) { print(); }
}

// Overloaded print functions
void print(String p, bool nl) {
  Serial.print(p);
  if (nl) { Serial.println(); }
}

void print() {
  Serial.println();
}

void print(String p) {
  Serial.println(p);
}

void rtcStart() {
  print("Starting RTC");
  if (rtc.begin()) {
    print("Started RTC");
  } else {
    print("Failed to Start RTC");
    while (1)
      ;  //stop if rtc not found
  }

  // ONLY USE IF YOU CHANGE THE RTC!!
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)) + TimeSpan(0, 0, 0, 8));
  //add 8 seconds to the time to account for upload lag
}

void timeSet() {
  if ((millis() - setLast) > setDelay) {
    setLast = millis();

    DateTime now = rtc.now();

    dayI = now.day();
    if (dayI < 10) {
      day = "0" + String(dayI);
    } else {
      day = String(dayI);
    }

    monthI = now.month();
    if (monthI < 10) {
      month = "0" + String(monthI);
    } else {
      month = String(monthI);
    }

    year = String(now.year());

    hourI = now.hour();
    if (hourI < 10) {
      hour = "0" + String(hourI);
    } else {
      hour = String(hourI);
    }

    minuteI = now.minute();
    if (minuteI < 10) {
      minute = "0" + String(minuteI);
    } else {
      minute = String(minuteI);
    }

    secondI = now.second();
    if (secondI < 10) {
      second = "0" + String(secondI);
    } else {
      second = String(secondI);
    }
  }
}

//testing function
void timeRead() {
  if ((millis() - readLast) > readDelay) {
    readLast = millis();

    print(year, false);
    print(".", false);
    print(month, false);
    print(".", false);
    print(day, false);
    print(" ", false);
    print(hour, false);
    print(".", false);
    print(minute);
  }
}

void timeLCD() {
  if ((millis() - lcdLast) > lcdDelay) {
    lcdLast = millis();

    String combine = year + "." + month + "." + day + " " + hour + "." + minute;
    lcdReset();
    lcd.setCursor(0, 1);
    lcd.print(combine);
    blockCheck(); // Call the block display logic
    timeRead();
  }
}

void blockCheck() {
  DateTime now = rtc.now();
  int dotw = now.dayOfTheWeek(); 
  
  // Format: 1:55 PM (13:55) becomes 1355
  int time = (now.hour() * 100) + now.minute();
  String value = "No School";

  if (dotw >= 1 && dotw <= 5) {
    if (time >= 900 && time < 948)        value = (dotw == 2) ? "TM OR TA/I Block" : "A Block";
    else if (time >= 948 && time < 953)   value = "Passing";
    else if (time >= 953 && time < 1041)  value = (dotw == 4) ? "TA OR Community" : "B Block";
    else if (time >= 1041 && time < 1046) value = "Passing";
    else if (time >= 1046 && time < 1134) value = (dotw == 2) ? "D Block" : "C Block";
    else if (time >= 1134 && time < 1214) value = "Lunch";
    else if (time >= 1214 && time < 1302) value = (dotw == 2 || dotw == 3) ? "E Block" : "D Block";
    else if (time >= 1302 && time < 1307) value = "Passing";
    else if (time >= 1307 && time < 1355) value = (dotw == 4 || dotw == 5) ? "E Block" : "F Block";
    else if (time >= 1355 && time < 1409) value = "I Block";
    else if (time >= 1409 && time < 1457) value = (dotw == 4) ? "F Block" : "G Block Comp Sci";
    else if (time >= 1457 && time < 1502) value = "Passing";
    else if (time >= 1502 && time < 1550) value = (dotw == 3) ? "TA/I Block" : "H Block Robotics";
  }

  lcd.setCursor(0,0);
  lcd.print(value);
}
