/***************************
 * AXSimpleTest
 * This sketch sends positional commands to the AX servo 
 * attached to it - the servo must set to ID # 1
 * The sketch will send a value, i, to the servo.
 * 'For' loops are used to increment and decrement the value of 'i'
 ***************************/

//import ax12 library to send DYNAMIXEL commands
#include <ax12.h>

int current = 512;
int ax_1 = 10;
int ax_2 = 11;
int vel_std = 1;
int incomingByte = 0; // for incoming serial data
int target = current;


void setup()
{
    SetPosition(ax_1,current); //set the position of servo # 1 to '0'
    SetPosition(ax_2,current);

    delay(100);//wait for servo to move
    Serial.begin(9600);

}

void loop()
{
  //int target = 512;
  while (Serial.available() > 0) {
    // read the incoming byte:
    target = Serial.parseInt(); 
  }
  
  Serial.println(target);
  delay(5);
  goPos(ax_1,target,vel_std);
 
 
}

void goPos(int servo,int pos,int vel){
  if (current < pos){
    for(int i=current; i<=pos; i+=vel){
      SetPosition(servo,i);
      current = i;
      delay(10);
      //Serial.println(current);
    }
  }
  
  if(current > pos){
    for(int i=current; i>=pos; i-=vel){
      SetPosition(servo,i);
      current = i;
      delay(10);
      //Serial.println(current);
    }
  }
}
