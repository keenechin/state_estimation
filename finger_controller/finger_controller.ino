/***************************
 * AXSimpleTest
 * This sketch sends positional commands to the AX servo 
 * attached to it - the servo must set to ID # 1
 * The sketch will send a value, i, to the servo.
 * 'For' loops are used to increment and decrement the value of 'i'
 ***************************/

//import ax12 library to send DYNAMIXEL commands
#include <ax12.h>


int ax_1 = 10;
int ax_2 = 11;

int current_1 = 512;
int current_2 = 512;
int target_1 = current_1;
int target_2 = current_2;


int new_target = current_1;
int axis = ax_1;

int vel_std = 1;

int command_data = 0;// for incoming serial data

char buffer[50];

void setup()
{
    SetPosition(ax_1,target_1); //set the position of servo # 1 to '0'
    SetPosition(ax_2,target_2);

    delay(500);//wait for servo to move
    Serial.begin(9600);

}

void loop()
{
  //int target = 512;
  while (Serial.available() > 0) {
    // read the incoming byte:
    command_data = Serial.parseInt(); //5 digit format, 1st digit is axis, next 4 are position
    //Serial.println(command_data);
    //delay(5);
    axis = (command_data / 10000)+9; // send "1" for servo 10, "2" for servo 11
    new_target = command_data % 10000;//send 4 digit target position from 0000 to 1024
    switch(axis){
      case 10:
        target_1 = new_target;
        //Serial.println(target_1);
        //Serial.println(target_2);
        break;
      case 11:
        target_2 = new_target;
        //Serial.println(target_1);
        //Serial.println(target_2);        
        break;
      default:
        break;
    }
    //Serial.println();
    
    
  }
  
  goPos(ax_1,&current_1,target_1,vel_std);
  goPos(ax_2,&current_2,target_2,vel_std);
  sprintf(buffer,"%d\t%d",current_1,current_2);
  Serial.println(buffer);
  delay(50);

 
 
}

void goPos(int servo,int *current, int pos,int vel){
  if(*current == pos){
    return;
  }
  
  if (*current < pos){
    for(int i=*current; i<=pos; i+=vel){
      SetPosition(servo,i);
      *current = i;
      delay(10);
      //Serial.println(*current);
    }
  }
  
  if(*current > pos){
    for(int i=*current; i>=pos; i-=vel){
      SetPosition(servo,i);
      *current = i;
      delay(10);
      //Serial.println(*current);
    }
  }
  Serial.println(7777777);
  delay(10);
}
