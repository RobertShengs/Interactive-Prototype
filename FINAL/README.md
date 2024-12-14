# Heart Rate Simulation Device with ProtoPie Integration

## Introduction

This project simulates a heart rate monitoring device that integrates with ProtoPie for visual feedback. Initially intended to use a real heart rate monitor, the device now uses an angle sensor to mimic heart rate variations. The final prototype includes real-time communication with ProtoPie to indicate normal and alarm states, accompanied by LED strip visualizations.

---

## Implementation



### Hardware

The hardware components used in this project are as follows:
- **ATOM S3 Board**:
  - Acts as the main controller, handling input/output operations and communication with sensors and ProtoPie.
- **Angle Sensor (AngleUnit)**:
  - Simulates heart rate variations by providing adjustable analog input. Replaced the pulse sensor for stability and resistance to environmental sensitivity.
- **RGB LED Strip**:
  - Contains 30 LEDs used to visually indicate the device's state (e.g., red for alarm).
- **Pulse Sensor (attempted, replaced)**:
  - Initially used to measure heart rate directly but discarded due to its sensitivity to environmental light fluctuations.
- **3D-Printed Enclosure**:
  - Protects the hardware while allowing LED light to pass through for visibility.

#### Wiring
- The **RGB LED strip** is connected to the ATOM S3 Board via **pin 38**.
- The **angle sensor** is connected to the analog input pin (ADC) on **pin 1**.
- The pulse sensor (when tested) was also connected to pin 1 but was replaced in the final implementation.

*(Include close-up photos of the wiring between these components.)*

---

### Firmware

The firmware was written in MicroPython and serves the following purposes:

1. **Simulating Heart Rate**:
   The angle sensor's analog values are mapped to a range representing heart rate (0–120 BPM):
   ```python
   def get_heart_rate():
       raw_value = pulse_sensor.read()
       heart_rate = int(m5utils.remap(raw_value, 0, 4095, 0, 120))
       return heart_rate
   ```

2. **LED Control**
  The RGB LED strip turns red to indicate an alarm condition:
  ```python
  if heart_rate < heart_rate_threshold:
    rgb_strip.fill_color(0xFF0000)  # Set LEDs to red
  ```

3. **ProtoPie Communication**
JSON-formatted signals are sent to ProtoPie for visualizing device states:
```python
Copy code
def send_to_protopie(signal):
    data = {"signal": signal}
    print(ujson.dumps(data) + "\n")  # Send signal to ProtoPie
```

Key Features:
Alarm Trigger: Triggers alarm ("b") if heart rate is below the threshold or if the device remains stationary beyond a specified duration.
Normal State: Resets to normal state ("a") if no alarm condition persists for 5 seconds.

