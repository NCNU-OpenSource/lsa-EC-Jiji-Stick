// generated by mBlock5 for mBot
// codes make you happy

#include <MeMCore.h>
#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>

MeIR ir;
MeDCMotor motor_9(9); 
MeDCMotor motor_10(10);

void move(int direction, int speed) {
  int leftSpeed = 0;
  int rightSpeed = 0;
  if(direction == 1) {
    leftSpeed = speed;
    rightSpeed = speed;
  } else if(direction == 2) {
    leftSpeed = -speed;
    rightSpeed = -speed;
  } else if(direction == 3) {
    leftSpeed = -speed;
    rightSpeed = speed;
  } else if(direction == 4) {
    leftSpeed = speed;
    rightSpeed = -speed;
  }
  motor_9.run((9) == M1 ? -(leftSpeed) : (leftSpeed));
  motor_10.run((10) == M1 ? -(rightSpeed) : (rightSpeed));
}

void _delay(float seconds) {
  long endTime = millis() + seconds * 1000;
  while(millis() < endTime) _loop();
}

void setup() {
  ir.begin();
  while(1) {
      if(ir.keyPressed(64)){

          move(2, 40 / 100.0 * 255);
          _delay(0.1);
          move(2, 0);

      }
      if(ir.keyPressed(25)){

          move(1, 40 / 100.0 * 255);
          _delay(0.1);
          move(1, 0);

      }
      if(ir.keyPressed(7)){

          move(3, 30 / 100.0 * 255);
          _delay(0.1);
          move(3, 0);

      }
      if(ir.keyPressed(9)){

          move(4, 30 / 100.0 * 255);
          _delay(0.1);
          move(4, 0);

      }

      _loop();
  }

}

void _loop() {
  ir.loop();
}

void loop() {
  _loop();
}
