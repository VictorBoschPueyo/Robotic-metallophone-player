// Imports
#include <Servo.h>
#include <AccelStepper.h>

// Constants
#define dirPin_right 2
#define stepPin_right 3
#define dirPin_left 9 //
#define stepPin_left 10 //

// Variables
Servo servoMotor_right;
Servo servoMotor_left;
AccelStepper motor_right(AccelStepper::DRIVER, stepPin_right, dirPin_right);
AccelStepper motor_left(AccelStepper::DRIVER, stepPin_left, dirPin_left);

void rightMotorMove(int steps, char dir) {
  float newSpeed = (float)1000 * 1000 / steps;

  motor_right.setSpeed(newSpeed);

  if (dir == 'L'){
    motor_right.move(steps);
  }
  else {
    motor_right.move(-steps);
  }

  // Wait for the motor to finish moving
  while (motor_right.distanceToGo() != 0) {
    motor_right.run();
  }
}

void leftMotorMove(int steps, char dir) {  
  float newSpeed = (float)1000 * 1000 / steps;

  motor_left.setSpeed(newSpeed);

  if (dir == 'L'){
    motor_left.move(steps);
  }
  else {
    motor_left.move(-steps);
  }

  // Wait for the motor to finish moving
  while (motor_left.distanceToGo() != 0) {
    motor_left.run();
  }
}

void rightDrumstickCling(){
  servoMotor_right.write(90);
  delay(100);
  servoMotor_right.write(110);
  delay(500);
}

void leftDrumstickCling(){
  servoMotor_left.write(90);
  delay(100);
  servoMotor_left.write(110);
  delay(500);
}

void setup() {
  Serial.begin(9600);

  // Set the maximum speed and acceleration of the motors
  motor_left.setMaxSpeed(1000);
  motor_left.setAcceleration(500);

  motor_right.setMaxSpeed(1000);
  motor_right.setAcceleration(500);

  // Set the initial position of the stepper motor to 0
  motor_left.setCurrentPosition(0);
  motor_right.setCurrentPosition(0);

  // Attach drumsticks
  servoMotor_right.attach(9);
  servoMotor_left.attach(11); //

  // Set drumsticks to top position
  servoMotor_right.write(110);
  servoMotor_left.write(110);
}

void loop() {
  if (Serial.available()>0) {
    String move = Serial.readString(); // ex. LR108
    int last_ind = move.length();

    char motor = move[0];  // L
    char direc = move[1];  // R
    int steps = move.substring(2, last_ind).toInt();  // 108

    if (motor = 'L'){
      leftMotorMove(steps, direc);
      leftDrumstickCling();
    }
    else {
      rightMotorMove(steps, direc);
      rightDrumstickCling();
    }
  }
}




