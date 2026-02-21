void setup() {
  Serial.begin(115200);
  delay(1000);
}

void loop() {

  Serial.print('<');          // Start marker
  Serial.print(sensorValue1); // First data point
  Serial.print(',');          // Delimiter
  Serial.print(sensorValue2); // Second data point
  Serial.print(',');          // Delimiter
  Serial.print(sensorValue3); // Third data point
  Serial.println('>');        // End marker and newline

  delay(1000); // Send a message every second
}
