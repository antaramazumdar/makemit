#include "Servo.h"
#include <LiquidCrystal.h>

// RS, E, D4, D5, D6, D7
LiquidCrystal lcd(7, 8, 5, 4, 3, 2);

Servo myServo;

int COM_PIN = A2;
bool lights = false;

int RED = 11;
int GREEN = 10;
int BLUE = 9;

int speed = 1; // lower = faster, higher = slower (ms per step)

// FIXED PIN CONFLICT: Swapped to 12 and 13 so they don't clash with GREEN (10)
// and BLUE (9)
const int stepPin = 12;
const int dirPin = 13;

static int i = 0;

byte boom[8] = {
    B01010, B10101, B01110, B11111, B01110, B10101, B01010, B00000,
};

unsigned long lastLCDUpdate = 0;
const unsigned long lcdInterval = 200; // 200 ms

void setup() {
  Serial.begin(9600);
  lcd.createChar(0, boom);
  lcd.begin(16, 2); // 16 columns, 2 rows
  lcd.print("Hello Brandon!");
  pinMode(COM_PIN, INPUT);
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);

  // Attach servo and tell it to STOP IMMEDIATELY on boot (90 is usually STOP
  // for continuous servos)
  myServo.attach(6);
  myServo.write(90);
}

void punish() {
  unsigned long currentMillis = millis();

  // 1. Continuous Servo Slap: Spin forward, wait, stop, spin backward, wait,
  // stop (You might need to adjust the delay(500) to get exactly a 90-degree
  // swing)

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

  // ---- Non-blocking LCD update ----
  if (currentMillis - lastLCDUpdate >= 0.5 * lcdInterval) {
    lcd.clear();
    lcd.write("YOU GOT SLAPPED");
    lcd.setCursor(6, 1);
    lcd.write(byte(0));
    lcd.write(byte(0));
    lcd.write(byte(0));
  } else if (currentMillis - lastLCDUpdate >= lcdInterval) {
    lastLCDUpdate = currentMillis;
    lcd.clear();
    lcd.write("BOOOM");
    lcd.setCursor(6, 1);
    lcd.write(byte(0));
    lcd.write(byte(0));
    lcd.write(byte(0));
  }

  lights = true;
  Serial.println(lights);
}

void loop() {
  // Check if we are being told to punish
  if (analogRead(COM_PIN) > 512) {
    punish();
  }

  // Update LEDs continuously if the light show has started
  if (lights == true) {
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
    delay(speed);
  }
}
