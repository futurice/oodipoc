// include stepper library header file
#include <AccelStepper.h>
// motor speed in steps per second
#define motorSpeed 2400

// motor acceleration in steps per second per second
#define motorAccel 32000

// left eyeball step and direction pins
#define xstep 2
#define xdir  3

// right eyeball step and direction pins
#define ystep 4
#define ydir  5

// ttur
#define MYSERIAL Serial
// ttur
String readString;

// left eyeball accelstepper instance
AccelStepper stepper1 (1, xstep, xdir);

// right eyeball accelstepper instance
AccelStepper stepper2 (1, ystep, ydir);


void setup()
{
    // ttur
    //MYSERIAL.begin(19200);
    MYSERIAL.begin(19200);
    MYSERIAL.println("Serial Initialised");
    
    // set step and direction pins to outputs
    pinMode (xstep, OUTPUT);
    pinMode (xdir,  OUTPUT);
    pinMode (ystep, OUTPUT);
    pinMode (ydir,  OUTPUT);

    // left eyeball stepper setup
    stepper1.setMaxSpeed(motorSpeed);
    stepper1.setSpeed(motorSpeed);
    stepper1.setAcceleration(motorAccel);

    // right eyeball stepper setup
    stepper2.setMaxSpeed(motorSpeed);
    stepper2.setSpeed(motorSpeed);
    stepper2.setAcceleration(motorAccel);
}


void loop()
{
  //int rxChar;

  // if a serial char is available
  //if (MYSERIAL.available())
  //{
  //  rxChar = MYSERIAL.read();
  //  eyenum = (int) rxChar;
  //  MYSERIAL.println(rxChar);
  //}

  while (MYSERIAL.available()) 
  {
    delay(2);  //delay to allow byte to arrive in input buffer
    char c = Serial.read();
    readString += c;
  }

  if (readString.length() >0) 
  {
    MoveEyes(readString.toInt());
    MYSERIAL.println(readString);
    readString="";
  } 
  
  //LookLeft ();
}


void MoveEyes (int eyenum)
{
    stepper1.moveTo(eyenum);
    stepper2.moveTo(eyenum);
    
    while ((stepper1.distanceToGo() != 0) || (stepper2.distanceToGo() != 0)) {
        stepper1.run();
        stepper2.run();
    }
}
