#include <Arduino.h>

// Sensor 1 pins
uint8_t TRIG_1 = 3;
uint8_t ECHO_1 = 2;

// Sensor 2 pins
uint8_t TRIG_2 = 5;
uint8_t ECHO_2 = 4;

// Sensor 3 pins
uint8_t TRIG_3 = 7;
uint8_t ECHO_3 = 6;

// Sensor 4 pins
uint8_t TRIG_4 = 9;
uint8_t ECHO_4 = 8;

// Sensor 5 pins
uint8_t TRIG_5 = 9;
uint8_t ECHO_5 = 8;

// Sensor 6 pins
uint8_t TRIG_6 = 9;
uint8_t ECHO_6 = 8;

float delay_1;
float delay_2;
float distance_1;
float distance_2;
float distance_3;
float distance_4;
float distance_5;
float distance_6;

int PRESS_PIN = A1;
int pressure;
bool sitting = false;

float readUltrasonic(uint8_t trigPin, uint8_t echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000); // 30ms timeout
  float distance = duration / 58.0;              // Convert µs to cm
  return distance;
}

// Forward declaration
bool wait_for_sit();

void setup() {
  Serial.begin(115200);

  pinMode(TRIG_1, OUTPUT);
  pinMode(ECHO_1, INPUT);

  pinMode(TRIG_2, OUTPUT);
  pinMode(ECHO_2, INPUT);

  pinMode(TRIG_3, OUTPUT);
  pinMode(ECHO_3, INPUT);

  pinMode(TRIG_4, OUTPUT);
  pinMode(ECHO_4, INPUT);

  pinMode(TRIG_5, OUTPUT);
  pinMode(ECHO_5, INPUT);

  pinMode(TRIG_6, OUTPUT);
  pinMode(ECHO_6, INPUT);

  pinMode(PRESS_PIN, INPUT);

  // Set A2-A5 as outputs to send 4-bit binary value to the Punishment Arduino
  pinMode(A2, OUTPUT);
  pinMode(A3, OUTPUT);
  pinMode(A4, OUTPUT);
  pinMode(A5, OUTPUT);
  // Default all to LOW
  digitalWrite(A2, LOW);
  digitalWrite(A3, LOW);
  digitalWrite(A4, LOW);
  digitalWrite(A5, LOW);
}

void loop() {
  wait_for_sit();

  if (Serial.available() > 0) {
    int incomingByte = Serial.read(); // Will be 0-16

    // Write the value as 4-bit binary across A2 (bit 0) through A5 (bit 3)
    digitalWrite(A2, (incomingByte & 0x01) ? HIGH : LOW); // bit 0
    digitalWrite(A3, (incomingByte & 0x02) ? HIGH : LOW); // bit 1
    digitalWrite(A4, (incomingByte & 0x04) ? HIGH : LOW); // bit 2
    digitalWrite(A5, (incomingByte & 0x08) ? HIGH : LOW); // bit 3
  }

  // 2. Continue reading sensors
  distance_1 = readUltrasonic(TRIG_1, ECHO_1);
  delay(50); // Prevent interference

  distance_2 = readUltrasonic(TRIG_2, ECHO_2);
  delay(50);

  distance_3 = readUltrasonic(TRIG_3, ECHO_3);
  delay(50);

  distance_4 = readUltrasonic(TRIG_4, ECHO_4);
  delay(50);

  distance_5 = readUltrasonic(TRIG_5, ECHO_5);
  delay(50);

  distance_6 = readUltrasonic(TRIG_6, ECHO_6);

  // Send data in EXACT format Python expects: <d1,d2,d3,d4,d5,d6>
  Serial.print("<");
  Serial.print(distance_1);
  Serial.print(",");
  Serial.print(distance_2);
  Serial.print(",");
  Serial.print(distance_3);
  Serial.print(",");
  Serial.print(distance_4);
  Serial.print(",");
  Serial.print(distance_5);
  Serial.print(",");
  Serial.print(distance_6);
  Serial.println(">");

  delay(200); // 5 readings per second
}

bool wait_for_sit() {
  while (sitting == false) {
    pressure = analogRead(PRESS_PIN);
    // Serial.println(pressure);
    if (pressure > 10) {
      sitting = true;
    } else {
      delay(100);
      continue;
    }
  }
  return sitting;
}
