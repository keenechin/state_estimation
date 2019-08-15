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

//char command_data[8];// for incoming serial data
String command_data;
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
  while (Serial.available()) {
    delay(3);
    if (Serial.available()>0){      
      char digit = Serial.read();
      command_data += digit;
    }
    
    if (command_data.length()==8){
      Serial.println(command_data);
      target_1 = command_data.substring(0,4).toInt();
      target_2 = command_data.substring(4,8).toInt();
      command_data = "";
    }    
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
