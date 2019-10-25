/***************************
 * AXSimpleTest
 * This sketch sends positional commands to the AX servo 
 * attached to it - the servo must set to ID # 1
 * The sketch will send a value, i, to the servo.
 * 'For' loops are used to increment and decrement the value of 'i'
 ***************************/

//import ax12 library to send DYNAMIXEL commands
#include <ax12.h>


int s0 = 10;
int s1 = 11;
int s2 = 12;
int s3 = 13;

int current_1 = 512;
int current_2 = 512;
int target_1 = current_1;
int target_2 = current_2;


int new_target = current_1;

int vel_std = 1;

//char command_data[8];// for incoming serial data
String command_data;
char buffer[50];


void setup()
{
    SetPosition(s0,target_1); //set the position of servo # 1 to '0'
    SetPosition(s1,1024-target_1);
    SetPosition(s2,target_2);
    SetPosition(s3,1024-target_2);

    delay(500);//wait for servo to move
    Serial.begin(9600);

}

void loop()
{
  command_data = "";
  //int target = 512;
  while (Serial.available()) {
    delay(3);
    if (Serial.available()>0){      
      char digit = Serial.read();
      command_data += digit;
    }
    
    if (command_data.length()==8){
      Serial.println(command_data);
      target_1 = max(min(command_data.substring(0,4).toInt(),1023),1);
      target_2 = max(min(command_data.substring(4,8).toInt(),1023),1);
      command_data = "";
    }    
  }


  goState(&current_1, target_1, &current_2, target_2, 4);
  sprintf(buffer,"%d\t%d",current_1,current_2);
  Serial.println(buffer);
  delay(50);
  Serial.flush();

 
 
}

void goState(int *current1, int pos1,int *current2, int pos2, int vel){
  if((abs(*current1-pos1)<(1)) & (abs(*current2 - pos2)<(1))){
    return;
  }
  int start1 = *current1;
  int start2 = *current2;
  
  double dist1 = pos1 - *current1;
  double dist2 = pos2 - *current2;
  
  double fast_dist = max(abs(dist1),abs(dist2));
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
     
     

     SetPosition(s0,*current1);
     SetPosition(s1,1024-*current1);
     SetPosition(s2,*current2);
     SetPosition(s3,1024-*current2);
     delay(12);

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
