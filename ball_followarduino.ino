 #include <Arduino.h>
#include <Servo.h>

Servo servo1;
int servoPin1 = 9;
Servo esc;
int servoPin2 = 10;

void setup() {
  servo1.attach(servoPin1);
  esc.attach (servoPin2);
  Serial.begin(2000000);
  while(!Serial){
    ;//WAITING FOR THE Serial TO CONNECT
  }
  Serial.setTimeout(200);
esc.write(80);
}


int commandfromjetson;
void loop() {
   
  //waiting for jetson command
  if (Serial.available()>0){
  commandfromjetson = Serial.readString().toInt();
 //0 is straight 1 is left 2 is right 3 is bacwards 4 is stop
  if (commandfromjetson == 0){
    servo1.writeMicroseconds(1500);
    esc.write(95);
  }
  if (commandfromjetson == 1){
  servo1.writeMicroseconds(2000);  
  esc.write(95); 
  }                       
  if (commandfromjetson ==2){
  servo1.writeMicroseconds(1000);   
  esc.write(95);
  
  }
  if (commandfromjetson == 3){
    servo1.writeMicroseconds(1500);
    esc.write(60);
  }
  if (commandfromjetson == 4){
    servo1.writeMicroseconds(1500);
    esc.write(80);
  }
  // wait for a second

  }  
  
}
