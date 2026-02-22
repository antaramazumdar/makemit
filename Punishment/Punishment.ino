#include <LiquidCrystal.h>
#include <Servo.h>

// RS, E, D4, D5, D6, D7
LiquidCrystal lcd(7, 8, 5, 4, 3, 2);

Servo myServo;

int COM_PIN = A2;
bool lights = false;

int RED = 11;
int GREEN = 10;
int BLUE = 9;

int speed = 1; // lower = faster, higher = slower (ms per step)

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
  myServo.attach(6);
}

void punish() {
  unsigned long currentMillis = millis();
  // rotate to 90°
  myServo.write(0);    // rotate to 0°
  delay(1000);
  myServo.write(90);   // rotate to 90°
  delay(1000);
  myServo.write(180);  // rotate to 180°
  delay(1000);
  // ---- Non-blocking LCD update ----
  if (currentMillis - lastLCDUpdate >= 0.5*lcdInterval) {
    lcd.clear();
    lcd.write("YOU GOT SLAPPED");
    lcd.setCursor(6, 1);
    lcd.write(byte(0));
    lcd.write(byte(0));
    lcd.write(byte(0));
    // delay(200); --> we want the rest of the program to continue, but this
    // should wait 200 ms before updating
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
  punish();
  if (analogRead(COM_PIN) > 512) {
    punish();
  }
  if (lights == true) {
    int zeroedCount = i % (255 * 3);
    int loop = zeroedCount / 255;
    int loopValue = zeroedCount % 255;

    analogWrite(RED, (loop == 0) * (loopValue) + (loop == 1) * (255) +
                        (loop == 2) * (255 - loopValue));
    analogWrite(GREEN, (loop == 0) * (255 - loopValue) +
                          (loop == 1) * (loopValue) + (loop == 2) * (255));
    analogWrite(BLUE, (loop == 0) * (255) + (loop == 1) * (255 - loopValue) +
                          (loop == 2) * (loopValue));
    Serial.println(loopValue);

    i++;
    delay(speed);
  }
}
