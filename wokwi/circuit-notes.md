# Wokwi Circuit Notes - SCEMS

## Project Link

- https://wokwi.com/projects/448685686274316289

## Microcontroller

- Arduino UNO (5V, 16 MHz)

## Sensor & Actuator Connections

| Logical Name      | Component           | Arduino Pin | Extra Notes                          |
|-------------------|--------------------|------------|--------------------------------------|
| SOIL_PIN          | Potentiometer      | A0         | Soil moisture (simulated)           |
| AQI_PIN           | Potentiometer      | A1         | AQI sensor (mock value)             |
| SOUND_PIN         | Potentiometer      | A2         | Ambient sound level (mock)          |
| LDR_PIN           | LDR + 10k resistor | A3         | 5V — LDR — A3 node — 10k — GND      |
| DHTPIN            | DHT22              | D2         | Temperature + humidity              |
| TRIG_PIN          | HC-SR04 TRIG       | D3         | Ultrasonic trigger                  |
| ECHO_PIN          | HC-SR04 ECHO       | D4         | Ultrasonic echo                     |
| PIR_PIN           | PIR OUT            | D5         | Motion detection                    |
| LIGHT_PIN         | LED (via 220Ω)     | D6         | Street light / adaptive lighting    |

## Power Connections

- All sensor VCC pins → 5V
- All sensor GND pins → GND
- LDR voltage divider:
  - 5V — LDR — node(A3) — 10k resistor — GND
