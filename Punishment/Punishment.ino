#include "Servo.h"
#include <LiquidCrystal.h>

// RS, E, D4, D5, D6, D7
LiquidCrystal lcd(7, 8, 5, 4, 3, 2);

Servo myServo;

int COM_1 = A1;
int COM_2 = A2;
int COM_3 = A3;
int COM_4 = A4;

bool lights = false;

int RED = 11;
int GREEN = 10;
int BLUE = 9;

int led_speed = 1; // lower = faster, higher = slower (ms per step)

// FIXED PIN CONFLICT: Swapped to 12 and 13 so they don't clash with GREEN (10)
// and BLUE (9)
const int stepPin = 12;
const int dirPin = 13;

static int i = 0;

byte boom[8] = {
    B01010, B10101, B01110, B11111, B01110, B10101, B01010, B00000,
};

byte shrimp[8] = {
  B00110,
  B01100,
  B11110,
  B01111,
  B00111,
  B00011,
  B00001,
  B00000  // empty row (required for 5x8 LCD char format)
};

unsigned long currentMillis;
unsigned long lastLCDUpdate = 0;
const unsigned long lcdInterval = 2000; // 200 ms
const unsigned long shrimpterval = 100;

void setup() {
  Serial.begin(9600);
  lcd.createChar(0, boom);
  lcd.createChar(1, shrimp);
  lcd.begin(16, 2); // 16 columns, 2 rows
  lcd.setCursor(6, 0);
  lcd.print("!!!");
  lcd.setCursor(4, 1);
  lcd.print("PREPARE");
  pinMode(COM_1, INPUT);
  pinMode(COM_2, INPUT);
  pinMode(COM_3, INPUT);
  pinMode(COM_4, INPUT);

  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);

  // Attach servo and tell it to STOP IMMEDIATELY on boot (90 is usually STOP
  // for continuous servos)
  myServo.attach(6);
  myServo.write(90);
}

void punish() {
  // 1. Continuous Servo Slap: Spin forward, wait, stop, spin backward, wait,
  // stop (You might need to adjust the delay(500) to get exactly a 90-degree
  // swing)
  lcd.clear();
  lcd.print("SLAP INCOMING");
  lcd.setCursor(6, 1);
  delay(1000);
  lcd.print("3");
  lcd.setCursor(7, 1);
  delay(1000);
  lcd.print("2");
  lcd.setCursor(8, 1);
  delay(1000);
  lcd.print("1");

  myServo.write(180); // Spin full speed forward
  delay(500);         // Time it takes to swing ~90 degrees
  myServo.write(90);  // Stop

  delay(500); // Wait a moment at the peak of the slap

  myServo.write(0);  // Spin full speed backward
  delay(500);        // Time it takes to return to start
  myServo.write(90); // Stop
  delay(500);        // Wait before doing the stepper motor reset

  // 2. Stepper Drive: 10 full rotations (4000 pulses) to reset the system
  // Sets the two pins as Outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  digitalWrite(dirPin, HIGH); // Set rotation direction
  for (int x = 0; x < 4000; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }
  delay(1000); // Wait after spinning
  lcd.clear();
  lcd.print("YOU GOT SLAPPED");
  lcd.setCursor(6, 1);
  lcd.write(byte(0));
  lcd.write(byte(0));
  lcd.write(byte(0));

  lights = true;
  Serial.println(lights);
  lastLCDUpdate = millis();
}

void loop() {
  currentMillis = millis();
  // Check if we are being told to punish
  bool slouch_1 = analogRead(COM_1) > 512;
  bool slouch_2 = analogRead(COM_2) > 512;
  bool slouch_3 = analogRead(COM_3) > 512;
  bool slouch_4 = analogRead(COM_4) > 512;
  int slouch_data = (slouch_1 + 2*slouch_2 + 4*slouch_3 + 8*slouch_4);

  if (slouch_data == 15) {
    punish();
  }

  // Update LEDs continuously if the light show has started
  if (lights == true) {
    lcd.clear();
    lcd.print("TAKE THAT SHRIMP");
    if (currentMillis - lastLCDUpdate >= lcdInterval) {
      lights = false;
      lcd.setCursor(5, 1);
      lcd.write(byte(0));
      lcd.write(byte(0));
      lcd.write(byte(0));
      lcd.write(byte(0));
      lcd.write(byte(0));   
      lastLCDUpdate = millis();
      // IDEA --> SHRIMP METER - detects how close you are to triggering it, 16 shrimps causes a slap.
    }

    int zeroedCount = i % (255 * 3);
    int loopVar = zeroedCount / 255;
    int loopValue = zeroedCount % 255;

    analogWrite(RED, (loopVar == 0) * (loopValue) + (loopVar == 1) * (255) +
                         (loopVar == 2) * (255 - loopValue));
    analogWrite(GREEN, (loopVar == 0) * (255 - loopValue) +
                           (loopVar == 1) * (loopValue) +
                           (loopVar == 2) * (255));
    analogWrite(BLUE, (loopVar == 0) * (255) +
                          (loopVar == 1) * (255 - loopValue) +
                          (loopVar == 2) * (loopValue));
    // Serial.println(loopValue);

    i++;
    delay(led_speed);
  } else {
    if (currentMillis - lastLCDUpdate >= shrimpterval) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("ANALYZING SHRIMP");
      for (int i = 0; i < slouch_data; i++) {
        lcd.setCursor(i, 1);
        lcd.write(byte(1));
    }
      lastLCDUpdate = millis();

    }

  }
}