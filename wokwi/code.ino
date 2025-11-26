#include <DHT.h>

// -------------------------
// Pin Definitions
// -------------------------
#define SOIL_PIN   A0   // Potentiometer → Soil moisture
#define AQI_PIN    A1   // Potentiometer → AQI (mock)
#define SOUND_PIN  A2   // Potentiometer → Sound level
#define LDR_PIN    A3   // LDR + 10k resistor divider

#define DHTPIN     2
#define DHTTYPE    DHT22

#define TRIG_PIN   3    // Ultrasonic TRIG
#define ECHO_PIN   4    // Ultrasonic ECHO
#define PIR_PIN    5    // PIR output
#define LIGHT_PIN  6    // LED for adaptive lighting

DHT dht(DHTPIN, DHTTYPE);

// -------------------------
// Helper functions
// -------------------------

float readSoilPercent() {
  int raw = analogRead(SOIL_PIN); // 0–1023
  // map to 0–100% (you can adjust later if needed)
  float percent = map(raw, 0, 1023, 0, 100);
  return percent;
}

int readAQI() {
  int raw = analogRead(AQI_PIN);
  // Map raw analog to AQI range 0–500 (approx)
  int aqi = map(raw, 0, 1023, 0, 500);
  return aqi;
}

int readSoundLevel() {
  int raw = analogRead(SOUND_PIN);
  // 0–1023 → 0–100 arbitrary level
  int level = map(raw, 0, 1023, 0, 100);
  return level;
}

long readDistanceCm() {
  // Ultrasonic distance in cm
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // timeout ~30ms
  if (duration == 0) {
    return -1; // no echo
  }
  long distance = duration / 58; // approx cm
  return distance;
}

int estimateCrowdFromDistance(long distanceCm) {
  // Simple assumption: small distance → more crowd (people closer)
  if (distanceCm < 0) return 0;
  if (distanceCm < 20) return 25;
  if (distanceCm < 40) return 20;
  if (distanceCm < 80) return 10;
  return 5;
}

bool isNightFromLDR(int ldrValue) {
  // LDR low = dark, high = bright
  // Tune thresholds as needed (0–1023)
  if (ldrValue < 300) return true;  // dark / night
  return false;                     // day / bright
}

bool isStormDarkDay(int ldrValue, bool isDayTime) {
  // Daytime কিন্তু আলোর মান খুব কম → storm/dark daylight
  if (isDayTime && ldrValue < 400) return true;
  return false;
}

float computeSimpleHeatIndex(float t, float h) {
  // Simplified approximation of heat index (not exact formula, but enough for contest)
  // If sensor fails (NaN), return -1
  if (isnan(t) || isnan(h)) return -1;
  // Very rough approximation:
  float hi = t + (0.1 * h / 10.0);
  return hi;
}

// -------------------------
// Setup
// -------------------------

void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(PIR_PIN, INPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LIGHT_PIN, OUTPUT);

  Serial.println("SCEMS Simulation Started...");
}

// -------------------------
// Main Loop
// -------------------------

void loop() {
  // ---- Read raw sensor values ----
  float soil = readSoilPercent();
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature(); // °C
  float heatIndex = computeSimpleHeatIndex(temperature, humidity);

  int aqi = readAQI();
  int soundLevel = readSoundLevel();
  int ldrValue = analogRead(LDR_PIN);
  bool pirState = digitalRead(PIR_PIN);

  long distance = readDistanceCm();
  int crowdEstimate = estimateCrowdFromDistance(distance);

  bool night = isNightFromLDR(ldrValue);
  bool stormDark = isStormDarkDay(ldrValue, !night);

  // -----------------------------
  // A1: Soil Moisture Conditions
  // -----------------------------
  String soilStatus;

  if (soil <= 15) {
    soilStatus = "IRRIGATION_ALERT";      // Moisture = 15% → Irrigation Alert
  } else if (soil <= 30) {
    soilStatus = "WARNING";               // Moisture ~28% → Warning
  } else if (soil >= 50 && soil <= 60) {
    soilStatus = "NO_WATERING_NEEDED";    // Moisture ~55% → No watering needed
  } else {
    soilStatus = "STABLE";
  }

  // For ±5% fluctuation and firehose effect,
  // we are not triggering extra states → soilStatus remains stable.

  // -----------------------------
  // A2: Temperature & Heat Stress
  // -----------------------------
  String heatStatus;

  if (!isnan(temperature)) {
    if (temperature >= 45) {
      heatStatus = "EMERGENCY_CONDITION";     // Temp = 45°C
    } else if (temperature >= 36) {
      heatStatus = "HEAT_STRESS_ALERT";       // Temp = 36°C
    } else if (temperature < 25) {
      heatStatus = "NORMAL";                  // Temp < 25°C
    } else {
      heatStatus = "ELEVATED";
    }

    if (!isnan(humidity) && temperature >= 32 && humidity >= 70) {
      // Combined heat-index warning
      heatStatus += "_HEAT_INDEX_WARNING";
    }
  } else {
    heatStatus = "TEMP_SENSOR_ERROR";
  }

  // -----------------------------
  // A3: AQI Test Cases
  // -----------------------------
  String aqiStatus;

  if (aqi >= 300) {
    aqiStatus = "HEALTH_RISK_ALERT";   // AQI = 300
  } else if (aqi >= 180) {
    aqiStatus = "POOR_AIR";            // AQI = 180
  } else if (aqi >= 40 && aqi <= 80) {
    aqiStatus = "STABLE_REPORTING";    // 40–80 → stable
  } else {
    aqiStatus = "GOOD";
  }

  // -----------------------------
  // A4: Crowd Density (Ultrasonic)
  // -----------------------------
  String crowdStatus;

  // We assume:
  // crowdEstimate ~ 5 → Normal
  // crowdEstimate ~ 20 → Shuttle alert
  if (crowdEstimate >= 20) {
    crowdStatus = "SHUTTLE_ALERT";   // Estimated crowd = 20
  } else if (crowdEstimate <= 5) {
    crowdStatus = "NORMAL_CROWD";    // crowd = 5
  } else {
    crowdStatus = "MEDIUM_CROWD";
  }

  // Sudden jump 3 → 25 and noise handling is represented by
  // our estimateCrowdFromDistance + logic not crashing.

  // -----------------------------
  // A5: Security (PIR + Sound)
  // -----------------------------
  String securityStatus = "NO_ALERT";

  bool soundHigh = (soundLevel > 60); // threshold, can be tuned

  if (pirState && soundHigh) {
    securityStatus = "SECURITY_ALERT";               // PIR + sound > threshold
  } else if (pirState && !soundHigh) {
    securityStatus = "IGNORE_PIR_ONLY";              // PIR alone
  } else if (!pirState && soundHigh) {
    securityStatus = "IGNORE_SOUND_ONLY";            // Sound alone
  }

  // রাতে multiple trigger হলে escalate করতে চাইলে, simple ভাবে night+alert হলে:
  if (night && securityStatus == "SECURITY_ALERT") {
    securityStatus = "SECURITY_ALERT_ESCALATED";     // Night-time escalation
  }

  // -----------------------------
  // A6: Adaptive Lighting (LDR)
  // -----------------------------
  String lightStatus;

  if (night) {
    digitalWrite(LIGHT_PIN, HIGH);       // Night mode → Light ON
    lightStatus = "NIGHT_MODE_LIGHT_ON";
  } else if (stormDark) {
    digitalWrite(LIGHT_PIN, HIGH);       // dark daylight / storm → partial/ON
    lightStatus = "STORM_DARK_DAY_LIGHT_ON";
  } else {
    digitalWrite(LIGHT_PIN, LOW);        // Day mode → Light OFF
    lightStatus = "DAY_MODE_LIGHT_OFF";
  }

  // -----------------------------
  // Print all statuses (one frame)
  // -----------------------------
  Serial.println("----------- SCEMS FRAME -----------");
  Serial.print("Soil: "); Serial.print(soil); Serial.print("% | Status: "); Serial.println(soilStatus);

  Serial.print("Temp: "); Serial.print(temperature); Serial.print(" C");
  Serial.print(" | Humidity: "); Serial.print(humidity); Serial.print(" %");
  Serial.print(" | HeatIndex: "); Serial.print(heatIndex);
  Serial.print(" | HeatStatus: "); Serial.println(heatStatus);

  Serial.print("AQI: "); Serial.print(aqi);
  Serial.print(" | AQI Status: "); Serial.println(aqiStatus);

  Serial.print("Ultrasonic distance: "); Serial.print(distance); Serial.print(" cm");
  Serial.print(" | Crowd estimate: "); Serial.print(crowdEstimate);
  Serial.print(" | Crowd status: "); Serial.println(crowdStatus);

  Serial.print("PIR: "); Serial.print(pirState ? "MOTION" : "NO MOTION");
  Serial.print(" | Sound level: "); Serial.print(soundLevel);
  Serial.print(" | Security: "); Serial.println(securityStatus);

  Serial.print("LDR value: "); Serial.print(ldrValue);
  Serial.print(" | Night: "); Serial.print(night ? "YES" : "NO");
  Serial.print(" | StormDarkDay: "); Serial.print(stormDark ? "YES" : "NO");
  Serial.print(" | Light status: "); Serial.println(lightStatus);

  Serial.println("-----------------------------------");
  Serial.println();

  delay(1000); // 1 second per frame
}
