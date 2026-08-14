# Line Following Robot for Lab Material Transport

Autonomous Arduino-based robot that navigates between a central hub and 
three lab rooms using IR line-following and ultrasonic obstacle avoidance, 
built and validated in Webots simulation.

## Features
- 3-sensor IR array for line detection and junction recognition
- HC-SR04 ultrasonic obstacle detection with emergency-stop and timeout alert
- Junction-based routing to 3 destination rooms with automatic path reversal on return
- Differential drive control (L298N motor driver)
- Simulation-first workflow: control logic prototyped in Python/Webots, 
  then ported to Arduino C++

## Tech Stack
Arduino Uno (ATmega328P) · C++ · Webots · Python · IR sensors · HC-SR04 · L298N


## How It Works
1. Operator selects destination room (1/2/3) via push buttons
2. Robot follows line, detects junctions via simultaneous 3-sensor trigger
3. Executes turn based on destination, continues to room
4. Stops, waits for payload, returns via reversed junction logic
