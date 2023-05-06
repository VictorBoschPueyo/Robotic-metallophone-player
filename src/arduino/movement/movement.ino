#include <AccelStepper.h>
#include <Servo.h>
 
// Define the stepper motor driver pins
#define dirPin_left 2
#define stepPin_left 3
#define dirPin_right 4
#define stepPin_right 5

// Define the servo pins
#define left_pin 11
#define right_pin 10

// Create an instance of the AccelStepper class
AccelStepper left_hand(AccelStepper::DRIVER, stepPin_left, dirPin_left);
AccelStepper right_hand(AccelStepper::DRIVER, stepPin_right, dirPin_right);
 
// Create an instance of the servos
Servo servo_right;
Servo servo_left;

void setup() {
  // Set the maximum speed and acceleration of the stepper motors
  // Also set the current position as 0
  left_hand.setMaxSpeed(20000);
  left_hand.setAcceleration(5000);
  left_hand.setCurrentPosition(0);

  right_hand.setMaxSpeed(20000);
  right_hand.setAcceleration(5000);
  right_hand.setCurrentPosition(0);

  // Assign the pin to each servo
  servo_left.attach(left_pin);
  servo_right.attach(right_pin);

}

void loop() {
  servo_left.write(106);
  delay(500);
  servo_left.write(88);
  delay(150);
  servo_left.write(106);
  delay(1500);

  servo_right.write(110);
  delay(500);
  servo_right.write(91);
  delay(150);
  servo_right.write(110);
  delay(1500);

  
  left_hand.move(200);
  right_hand.move(200);

  while (left_hand.distanceToGo() != 0) {
    left_hand.run();
  }
  while (right_hand.distanceToGo() != 0) {
    right_hand.run();
  }
  delay(1000);

  left_hand.move(-200);
  right_hand.move(-200);

  while (left_hand.distanceToGo() != 0) {
    left_hand.run();
  }
  while (right_hand.distanceToGo() != 0) {
    right_hand.run();
  }
  delay(1000);

}
