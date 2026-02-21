#include <Arduino.h>

// Sensor 1 pins
uint8_t TRIG_1 = 3;
uint8_t ECHO_1 = 2;

// Sensor 2 pins
uint8_t TRIG_2 = 4;
uint8_t ECHO_2 = 5;

float delay_1;
float delay_2;
float distance_1;
float distance_2;
float distance_3 = 10;

float readUltrasonic(uint8_t trigPin, uint8_t echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000); // 30ms timeout
  float distance = duration / 58.0; // Convert µs to cm
  return distance;
}


void setup() {
  Serial.begin(9600);

  pinMode(TRIG_1, OUTPUT);
  pinMode(ECHO_1, INPUT);

  pinMode(TRIG_2, OUTPUT);
  pinMode(ECHO_2, INPUT);
}

void loop() {

  distance_1 = readUltrasonic(TRIG_1, ECHO_1);
  delay(50);  // Prevent interference

  distance_2 = readUltrasonic(TRIG_2, ECHO_2);
  delay(50);

  %distance_3 = readUltrasonic(TRIG_3, ECHO_3);

  // Send data in EXACT format Python expects
  Serial.print("<");
  Serial.print(distance_1);
  Serial.print(",");
  Serial.print(distance_2);
  Serial.print(",");
  Serial.print(distance_3);
  Serial.println(">");

  delay(200);   // 5 readings per second
}


  // Print results
  Serial.print("Sensor 1: ");
  Serial.print(distance_1);
  Serial.print(" cm | ");

  Serial.print("Sensor 2: ");
  Serial.print(distance_2);
  Serial.println(" cm");

  // Wait 1 second before next full cycle
  delay(1000);
}
