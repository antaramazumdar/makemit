#include <LiquidCrystal.h>

// RS, E, D4, D5, D6, D7
LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

int PRESS_PIN = A1;
int pressure;

#define RED 9
#define GREEN 10
#define BLUE 11

int speed = 1; // lower = faster, higher = slower (ms per step)

static int i = 0;

byte boom[8] = {
    B01010, B10101, B01110, B11111, B01110, B10101, B01010,
};

unsigned long lastLCDUpdate = 0;
const unsigned long lcdInterval = 200; // 200 ms

void setup() {
  Serial.begin(9600);
  lcd.createChar(0, boom);
  lcd.begin(16, 2); // 16 columns, 2 rows
  lcd.print("Hello Brandon!");
  pinMode(PRESS_PIN, INPUT);
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
}

void punish() {
  unsigned long currentMillis = millis();

  // ---- Non-blocking LCD update ----
  if (currentMillis - lastLCDUpdate >= lcdInterval) {
    lastLCDUpdate = currentMillis;
    lcd.clear();
    lcd.write("YOU GOT SLAPPED");
    lcd.setCursor(6, 1);
    lcd.write(byte(0));
    lcd.write(byte(0));
    lcd.write(byte(0));
    // delay(200); --> we want the rest of the program to continue, but this
    // should wait 200 ms before updating
  }
  int zeroedCount = i % (255 * 3);
  int loop = zeroedCount / 255;
  int loopValue = zeroedCount % 255;

  analogWrite(RED, (loop == 0) * (loopValue) + (loop == 1) * (255) +
                       (loop == 2) * (255 - loopValue));
  analogWrite(GREEN, (loop == 0) * (255 - loopValue) +
                         (loop == 1) * (loopValue) + (loop == 2) * (255));
  analogWrite(BLUE, (loop == 0) * (255) + (loop == 1) * (255 - loopValue) +
                        (loop == 2) * (loopValue));

  i++;
  delay(speed);
}

void loop() {
  // if (slap ==true){
  punish();
  //}
  // lcd.print(pressure);
}