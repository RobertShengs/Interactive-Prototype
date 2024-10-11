## Assignment #1 Documentation  
  

### Introduction

The initial concept of this project was to create a prototype nightlight using the materials outlined above. This light can mimic the natural phenomenon of lightning with its irregular flashing or maintain a steady and softly bright state when needed. The main goal is to craft a soothing, nature-inspired light pattern that helps induce sleep and provides a stable, gentle light source when necessary. Below are initial concept sketches.



### State Diagram

Explain the interactive behaviors of the prototype you created and include a 
state diagram (flowchart) to represent it.  For example, below is an example 
state diagram included in the assignment description:  

![State Diagram](Flow_Chart_Final.png)  

### Hardware

The following hardware components were used in this project:

- Atom3 board – A microcontroller used to control the light bulb and process button inputs.
- Button (connected to Pin 7) – Acts as an input device to change the states of the system.
- LED Bulb (connected to Pin 8) – The output device that responds with different lighting effects.
- Wires and Breadboard – Used for setting up the circuit to connect the components.
- Origami Crane made of paper
- Copper Tape – Used to adhere and secure non-critical parts of the circuit.
  
Below is a wiring diagram showing how the components are connected. (Insert your wiring image here – can be hand-drawn or software-generated.)

![Hand_Sketch_Connection](Sketch.png)  

### Firmware   

Upload your MicroPython code and highlight important code snippet(s) that make 
your prototype work.  Most likely you should explain the inputs/outputs used 
in your code and how they affect the behavior of the prototype.

To include code snippets, you can use the code block markdown:

``` Python  
  if input_pin.value():  # read digital input
    led_pin.off()        # turn off LED light
  else:
    led_pin.on()         # turn on LED light
```

### Physical Components   

Explain what products, materials or components you used for the project. 
If you fabricated your own project components, include some details on 
how you made them.

### Project outcome  

Summarize the results of your project implementation and include at least 
1 photo of the finished prototype.  

Finally, include a short video walkthrough of your project showing all of 
its functioning aspects (voice over is optional but could be helpful).  

Note that GitHub has a small size limit for uploading files via browswer (25Mb max), 
so you may choose to use a link to YouTube, Google Drive, or another external site.
