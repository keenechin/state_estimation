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

  goState(ax_1,&current_1,target_1, ax_2,&current_2,target_2,5);
  sprintf(buffer,"%d\t%d",current_1,current_2);
  Serial.println(buffer);
  delay(50);
  Serial.flush();

 
 
}

void goState(int servo1,int *current1, int pos1,int servo2, int *current2, int pos2, int vel){
  if((abs(*current1-pos1)<(1)) & (abs(*current2 - pos2)<(1))){
    return;
  }
  
  int start1 = *current1;
  int start2 = *current2;
  
  double dist1 = pos1 - *current1;
  double dist2 = pos2 - *current2;
  double fast_dist = min(abs(dist1),abs(dist2));
  int num_steps = ceil(fast_dist/vel);
  
  double slope1 = dist1/num_steps;
  double slope2 = dist2/num_steps;

  for(int i=0;i<=num_steps;i++){
    
     if (i<num_steps){
     *current1 = start1 + round(i*slope1);
     *current2 = start2 + round(i*slope2);
     }
     else {
       *current1 = pos1;
       *current2 = pos2;
     }
     
     SetPosition(servo2,*current2);
     delay(10);
     SetPosition(servo1,*current1);
     delay(10);

  }

  Serial.println(7777777);
  delay(20);
  
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
