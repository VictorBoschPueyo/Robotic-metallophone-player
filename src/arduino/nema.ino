// Imports
#include <Servo.h>


// Variables
#define dirPin 2
#define stepPin 3
#define stepsPerRevolution 75

Servo servoMotor;

void rightMotorMoveRight(int n) {
  digitalWrite(dirPin, LOW);

  for (int i = 0; i < stepsPerRevolution * n; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }
}

void rightMotorMoveLeft(int n) {
  digitalWrite(dirPin, HIGH);
  
  for (int i = 0; i < stepsPerRevolution * n; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }
}

bool motorMoved = 0;

void rightDrumstickCling(){
  servoMotor.write(90);
  delay(100);
  servoMotor.write(110);
  delay(500);
  
}

void setup() {
  Serial.begin(9600);

  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  servoMotor.attach(9);
}

void loop() {
  // Posar baquetes a dalt
  servoMotor.write(110);

  rightMotorMoveRight(2);
  delayMicroseconds(1000);
  rightDrumstickCling();  

}




