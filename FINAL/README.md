# Heart Rate Simulation Device with ProtoPie Integration

## Introduction

This project simulates a heart rate monitoring device that integrates with ProtoPie for visual feedback. Initially intended to use a real heart rate monitor, the device now uses an angle sensor to mimic heart rate variations. The final prototype includes real-time communication with ProtoPie to indicate normal and alarm states, accompanied by LED strip visualizations.

---

## Research
![image](https://github.com/user-attachments/assets/b8a00632-fb2e-496f-b792-90da3a9ee7e1)



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

4. **Key Features**
- **Alarm Trigger:** 
Triggers alarm ("b") if heart rate is below the threshold or if the device remains stationary beyond a specified duration.
- **Normal State:** 
Resets to normal state ("a") if no alarm condition persists for 5 seconds.


**Mechanism Summary**
The "b" drowning signal is triggered under the following three conditions:
- Heart rate drops below 50 BPM (heart_rate < heart_rate_threshold).
- The device remains stationary for more than 10 seconds (acceleration below the threshold and stationary time exceeding stationary_time_limit).
- The user manually presses the button (BtnA.wasPressed()). 

When any of these conditions are met, the code will:
- Send the "b" signal to ProtoPie.
- Turn on the red LED light.
- Update the UI to reflect the drowning state.


---

## Software
**ProtoPie Integration**
ProtoPie was used to visualize the device states based on signals sent from the firmware:

**- Alarm State ("b"):**
- Displays a drowning alarm when the device detects low simulated heart rate or prolonged stationary behavior.
**- Normal State ("a"):**
- Resets the interface to the normal condition.

**Key Snippets**
Firmware sends the following signals:
```python
if heart_rate < heart_rate_threshold:
    send_to_protopie("b")
elif time.ticks_ms() - last_b_trigger_time > 5000:
    send_to_protopie("a")
```


---

## Integrations
**ProtoPie Connect:**
- Receives JSON-formatted signals ("a" for normal, "b" for alarm) from the firmware.
- Debugging ProtoPie integration involved significant time due to configuration errors in signal handling.

---

## Enclosure / Mechanical Design
**Enclosure**
**- Material:**
- The enclosure was 3D-printed using a transparent elastic material for light transmission.
**- Challenges:**
- The pipe housing the LED strip was initially filled with support material during printing. A precise incision at the bottom allowed manual removal of this material before inserting the LED strip.


---

## Project Outcome
**Results**
The final prototype successfully demonstrates:
- Simulated heart rate monitoring using an angle sensor.
- Visual alarm state indication via an RGB LED strip.
- Real-time communication with ProtoPie for state visualization.


---

## Conclusion
**Reflections**
**Challenges:**
- Hardware: The pulse sensor’s environmental sensitivity required a shift to a more stable input device (angle sensor).
- Software: Debugging the ProtoPie connection consumed significant time due to incorrect settings.
- Enclosure: Manual removal of 3D-printed support material was labor-intensive but necessary for the final assembly.

**Lessons Learned:**
- Simple and reliable hardware components significantly improve overall system stability.
- Thorough testing and debugging at each development stage are critical to avoid misdirected efforts.

**Future Improvements:**
- Replace the angle sensor with a robust heart rate monitor immune to environmental fluctuations.
- Optimize the enclosure design to eliminate manual post-processing.
- Enhance software functionality with more detailed visual feedback or additional UI states.




