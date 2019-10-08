// test code for 
// CNC Single Axis 4A TB6600 Stepper Motor Driver Controller 
// use Serial Monitor to control 115200 baud
//
// https://www.hackster.io/ashleyblack/tb6600-stepper-motor-driver-tester-85a29e
//
//
// NE: This code was modified to work with an Arduino UNO.


word  X;
word NX;
int MoveSpeed=600; //step in Microseconds
String     inputString = "help\n"; // a string to hold incoming data
boolean stringComplete = true;     // whether the string is completet
boolean        ComData = false;    // whether com data is on when motors are moving will slow them down

// NE: GND   # define X_ENgnd  2 //ENA-(ENA) stepper motor enable , active low     Gray 
# define X_EN_5v  2 //ENA+(+5V) stepper motor enable , active low     Orange
// NE: GND   # define X_DIRgnd 4 //DIR-(DIR) axis stepper motor direction control  Blue
# define X_DIR_5v 3 //DIR+(+5v) axis stepper motor direction control  Brown
// NE: GND   # define X_STPgnd 6 //PUL-(PUL) axis stepper motor step control       Black
# define X_STP_5v 4 //PUL+(+5v) axis stepper motor step control       RED


void setup() {// *************************************************************     setup
// NE: GND   pinMode (X_ENgnd ,OUTPUT); //ENA-(ENA)
pinMode (X_EN_5v ,OUTPUT); //ENA+(+5V)
// NE: GND   pinMode (X_DIRgnd,OUTPUT); //DIR-(DIR)
pinMode (X_DIR_5v,OUTPUT); //DIR+(+5v)
// NE: GND   pinMode (X_STPgnd,OUTPUT); //PUL-(PUL)
pinMode (X_STP_5v,OUTPUT); //PUL+(+5v)
pinMode (13,OUTPUT);
// NE: GND   digitalWrite (X_ENgnd,  LOW); //ENA-(ENA)
digitalWrite (X_EN_5v, HIGH); //ENA+(+5V) low=enabled
// NE: GND   digitalWrite (X_DIRgnd, LOW); //DIR-(DIR)
digitalWrite (X_DIR_5v, LOW); //DIR+(+5v)
// NE: GND   digitalWrite (X_STPgnd, LOW); //PUL-(PUL)
digitalWrite (X_STP_5v, LOW); //PUL+(+5v)

Serial.begin(115200);
}

void serialEvent()// ********************************************************      Serial in
{ while (Serial.available()) 
  {
    char inChar = (char)Serial.read();            // get the new byte:
    if (inChar > 0)     {inputString += inChar;}  // add it to the inputString:
    if (inChar == '\n') { stringComplete = true;} // if the incoming character is a newline, set a flag so the main loop can do something about it: 
  }
}
void Help(){ // **************************************************************   Help
 Serial.println("Commands step by step guide");
 Serial.println("Type hello -sends TB6600 Tester Ready ");
 Serial.println("Type xon  -turns TB6600 on");
 Serial.println("Type x+Number(0-60000) eg x1904 -to set next move steps");
 Serial.println("Type mx -to make motor move to next postion");
 Serial.println("Type cdon -turns on postion data when moving will increase time of step");
 Serial.println("Type x0");
 Serial.println("Type mx");
 Serial.println("Type s+Number(0-2000) eg s500 -to set Microseconds betwean steps");
 Serial.println("Type s2000");
 Serial.println("Type x300");
 Serial.println("Type mx");
 Serial.println("Type xoff -turns TB6600 off");
 Serial.println("Type cdoff -turns off postion data when moving");
 
 

 inputString="";
}
void Hello(){ // **************************************************************   Hello
 Serial.println("TB6600 Tester Ready");
 inputString="";
}
void ENAXON(){ // *************************************************************   ENAXON
 Serial.println("ENAXON");
 digitalWrite (X_EN_5v, LOW);//ENA+(+5V) low=enabled
 inputString="";
}
void ENAXOFF(){  // ***********************************************************   ENAXOFF
 Serial.println("ENAXOFF");
 digitalWrite (X_EN_5v, HIGH);//ENA+(+5V) low=enabled
 inputString="";
}
void MSpeed(){  // ************************************************************   MoveSpeed
 inputString.setCharAt(0,' ');
 MoveSpeed=inputString.toInt();
 Serial.print("Speed=");
 Serial.println(MoveSpeed);
 inputString="";
}
void ComDataON(){  // *********************************************************   ComDataON
 ComData=true;
 Serial.println("ComDataOn");
 inputString="";
}
void ComDataOFF(){  // ********************************************************   ComDataOFF
 ComData=false;
 Serial.println("ComDataOFF");
 inputString="";
}
void NextX(){ // **************************************************************    NextX
 inputString.setCharAt(0,' ');
 NX=inputString.toInt();
 Serial.print("NX=");
 Serial.println(NX);
 inputString="";
}
void MoveX(){ // **************************************************************    Move
int xt;
if (NX>X)
{xt=NX-X; digitalWrite (X_DIR_5v,LOW);xt=1;}
else
{xt=X-NX; digitalWrite (X_DIR_5v,HIGH);xt=-1;}
if (ComData==true)
{for (; X !=NX; X=X+xt)
{    digitalWrite (X_STP_5v, HIGH);
     Serial.print("X=");
     delayMicroseconds (MoveSpeed);
     digitalWrite (X_STP_5v, LOW);
     delayMicroseconds (MoveSpeed);
     Serial.println(X+100000);
}}
else
{for (; X !=NX; X=X+xt)
{    digitalWrite (X_STP_5v, HIGH);
     delayMicroseconds (MoveSpeed);
     digitalWrite (X_STP_5v, LOW);
     delayMicroseconds (MoveSpeed);
}}
Serial.print("X=");
Serial.println(X);
//X=NX;

inputString="";
}
void loop()  // **************************************************************     loop
{
 serialEvent(); 
 if (stringComplete) 
 {
  if (inputString=="help\n")      {Help();}
  if (inputString=="hello\n")     {Hello();}  
  if (inputString=="xon\n")       {ENAXON();}   
  if (inputString=="xoff\n")      {ENAXOFF();}
  if (inputString=="cdon\n")      {ComDataON();}
  if (inputString=="cdoff\n")     {ComDataOFF();}
  if (inputString=="mx\n")        {MoveX();}
  if (inputString.charAt(0)=='s')   {MSpeed();}
  if (inputString.charAt(0)=='x')   {NextX();} 
  
  if (inputString !="") {Serial.println("BAD COMMAND="+inputString);}// Serial.print("\n"); }// "\t" tab      
  inputString = ""; stringComplete = false; // clear the string:
 }

}


