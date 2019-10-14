const int triggerPort = 9;
const int echoPort = 10;
long duration;
unsigned long time_millis;
char buff[20];
int distance;

void setup() {
 
pinMode(triggerPort, OUTPUT);
pinMode(echoPort, INPUT);
Serial.begin(9600);
}
 
void loop() {
 
//porta bassa l'uscita del trigger
digitalWrite( triggerPort, LOW );
//invia un impulso di 10microsec su trigger
digitalWrite( triggerPort, HIGH );
delayMicroseconds( 10 );
digitalWrite( triggerPort, LOW );
 
duration = pulseIn( echoPort, HIGH );
 
//distance = 0.03461 * duration / 2.;
distance = duration ;
time_millis=millis();


//dopo 38ms è fuori dalla portata del sensore
if( duration > 38000 ){
sprintf(buff, "nan");
}
else{ 
dtostrf(distance, 4, 4, buff);
}
sprintf(buff+strlen(buff), ";%lu", time_millis);
Serial.println(buff);


//Aspetta 1000 microsecondi
//delay(1);
}