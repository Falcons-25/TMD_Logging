#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 4;
const int LOADCELL_SCK_PIN = 5;

HX711 scale;

// RC Receiver variables
#define THROTTLE_SIGNAL_IN 0 // INTERRUPT 0 = DIGITAL PIN 2
#define THROTTLE_SIGNAL_IN_PIN 2 // Digital Pin 2

float actualThrottle;
#define NEUTRAL_THROTTLE 1500
volatile int nThrottleIn = NEUTRAL_THROTTLE;
volatile unsigned long ulStartPeriod = 0;
volatile boolean bNewThrottleSignal = false;

void setup() {
  // Setup for HX711
  Serial.begin(57600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);

  // Setup for RC Receiver
  attachInterrupt(THROTTLE_SIGNAL_IN, calcInput, CHANGE);
}

void loop() {
  if (scale.is_ready()) {
    // HX711 config
    scale.set_scale();
    Serial.println("Tare... remove any weights from the scale (5sec).");
    delay(5000);
    scale.tare();
    Serial.println("Tare done.");
    
    int known_weight = 828;
    double calibration_factor = 20.821256038647342;
    scale.set_scale(calibration_factor);
    scale.tare();
    delay(1000);

    while (scale.is_ready()) {
      // Serial.print("Weight: ");
      Serial.println(known_weight * (1 - scale.get_units(10) / known_weight) / 1000, 5);
      
      // RC Receiver code
      if (bNewThrottleSignal) {
        actualThrottle = map(nThrottleIn, 905, 2090, 0, 100);
        // Serial.print("Throttle: ");
        Serial.print(",");
        Serial.println(actualThrottle);
        bNewThrottleSignal = false;
      }
      else {
        Serial.println(",0");
      }

      delay(250); // Adjust the delay as needed
    }
  } else {
    Serial.println("HX711 not found.");
  }
  
  delay(250); // Adjust the delay as needed
}

void calcInput() {
  if (digitalRead(THROTTLE_SIGNAL_IN_PIN) == HIGH) {
    ulStartPeriod = micros();
  } else {
    if (ulStartPeriod && (bNewThrottleSignal == false)) {
      nThrottleIn = (int)(micros() - ulStartPeriod);
      ulStartPeriod = 0;
      bNewThrottleSignal = true;
    }
  }
}
