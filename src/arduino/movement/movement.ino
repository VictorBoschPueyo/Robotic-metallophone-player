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
Servo servo_left;
Servo servo_right;

// Positions array
int left_positions[25] = {-635, -555, -475, -395, -315, -235, -155, -75, 0, 85, 160, 235, 315, 407, 480, 560, 640, 715, 795, 875, 955, 1035, 0, 0, 0};
int right_positions[25] = {0, 0, 0, -1035, -955, -875, -795, -710, -640, -555, -480, -400, 315, -233, -160, -80, 0, 75, 155, 234, 315, 390, 480, 555, 635};

// Functions
void move_left_hand(int pos)
{
  left_hand.moveTo(left_positions[pos]);
  while (left_hand.distanceToGo() != 0)
  {
    left_hand.run();
  }
}

void move_right_hand(int pos)
{
  right_hand.moveTo(right_positions[pos]);
  while (right_hand.distanceToGo() != 0)
  {
    right_hand.run();
  }
}

void move_motors(int left_pos, int right_pos){
  left_hand.moveTo(left_positions[left_pos]);
  right_hand.moveTo(right_positions[right_pos]);

  while (left_hand.distanceToGo() != 0 || right_hand.distanceToGo() != 0)
  {
    left_hand.run();
    right_hand.run();
  } 
}

void left_Drumstick_cling()
{
  servo_left.write(85);
  delay(150);
  servo_left.write(104);
  delay(500);
}

void right_Drumstick_cling()
{
  servo_right.write(91);
  delay(150);
  servo_right.write(110);
  delay(500);
}

int set_motor_option(String left_ins,  String right_ins){
  if (left_ins == "WW" && right_ins == "WW"){
    return 0;
  }
  else if (right_ins == "WW"){
    return 1;
  }
  else if (left_ins == "WW"){
    return 2;
  }
  else{
    return 3;
  }
}


void setup()
{
  Serial.begin(9600);

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

void loop()
{
  servo_left.write(104);
  servo_right.write(110);

  if (Serial.available() > 0)
  {
    String input = Serial.readString(); // ex. L09WRWWP
    Serial.println(input);

    String left_move = input.substring(1, 3);  // ex. 09
    String left_play = input.substring(3, 4);  // ex. W
    String right_move = input.substring(5, 7); // ex. WW
    String right_play = input.substring(7, 8);  // ex. P

    // OPTIONS
    // 1: move LEFT
    // 2: move RIGHT
    // 3: move BOTH
    int option = set_motor_option(left_move, right_move);

    if (option == 1){
      int left_position = left_move.toInt();
      move_left_hand(left_position);
    }
    else if (option == 2){
      int right_position = right_move.toInt();
      move_right_hand(right_position);
    }
    else if (option == 3){
      int left_position = left_move.toInt();
      int right_position = right_move.toInt();
      move_motors(left_position, right_position);
    }

    if (left_play == "P")
    {
      left_Drumstick_cling();
    }

    if (right_play == "P")
    {
      right_Drumstick_cling();
    }
  }
}
