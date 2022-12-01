#include <Servo.h>
int action;
int time;
int light = 8;
String received;
Servo Entrada;
Servo Salida;
int posE = 0;
int posS = 0;
boolean newData = false;
void setup() {
  Entrada.attach(7);
  Salida.attach(6);
  Serial.begin(115200);
  Serial.setTimeout(1);
  Entrada.write(posE);
  Salida.write(posS);
}

void loop() {

  if (Serial.available())
  {
    received = Serial.readString();
    action = received.toInt();
    moveServos();
  }
} 


void moveServos(){
  
  switch (action){
    case 1:
      for (posE = 0; posE <= 150; posE += 5) { // goes from 0 degrees to 180 degrees
        Entrada.write(posE);             // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15 ms for the servo to reach the position
      }
      break; 
    case 2:
      for (posE = 150; posE >= 0; posE -= 5) { // goes from 180 degrees to 0 degrees
        Entrada.write(posE);              // tell servo to go to position in variable 'pos'
        delay(15);  
      }    
      break;
    case 3:
      for (posS = 0; posS <= 150; posS += 5) { // goes from 0 degrees to 180 degrees
        Salida.write(posS);             // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15 ms for the servo to reach the position
      }                     
      break; 
    case 4:
      for (posS = 150; posS >= 0; posS -= 5) { // goes from 180 degrees to 0 degrees
        Salida.write(posS);              // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15 ms for the servo to reach the position
      }  
      break;
    case 5:
      digitalWrite(light,HIGH);
      break;
    case 6:
      digitalWrite(light,LOW);
      break;
    default:
      break;
  }
  
}