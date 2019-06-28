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
int point_one = 512-400;
int point_two = 512-400;

void setup()
{
    SetPosition(1,current); //set the position of servo # 1 to '0'

    delay(100);//wait for servo to move
    Serial.begin(9600);
}

void loop()
{
   
  /*
  //increment from 0 to 1023
  for(int i=0;i<1024;i++)
  {
    SetPosition(1,i); //set the position of servo #1 to the current value of 'i'
    delay(10);//wait for servo to move
  }
  //decrement from 1024 to 0
  for(int i=1024;i>0;i--)
  {
    SetPosition(1,i);//set the position of servo #1 to the current value of 'i'
    delay(10);//wait for servo to move
  }
  */
 

  goPos(point_one,1);
  //delay(500);
  goPos(point_two,1);
  //delay(500);

}

void goPos(int pos,int vel){
  if (current < pos){
    for(int i=current; i<=pos; i+=vel){
      SetPosition(1,i);
      current = i;
      delay(10);
      Serial.println(current);
    }
  }
  
  if(current > pos){
    for(int i=current; i>=pos; i-=vel){
      SetPosition(1,i);
      current = i;
      delay(10);
      Serial.println(current);
    }
  }
}
