/* Simple Obstacle Avoidance Module with Buzzer */

class ObstacleAvoidance {
  
  private:
    // Thresholds
    const float SAFETY_DISTANCE = 20.0;  // 20 cm
    const unsigned long CHECK_INTERVAL = 500;  // 500 ms
    const unsigned long TIMEOUT = 30000;  // 30 seconds
    
    // State
    bool blocked;
    unsigned long block_start;
    unsigned long last_check;
    bool alert_on;
    
    // Pins
    int ultrasonic_trig_pin;
    int ultrasonic_echo_pin;
    int buzzer_pin;
    
  public:
    
    ObstacleAvoidance(int trig_pin, int echo_pin, int buzz_pin) {
      // Initialize pins
      ultrasonic_trig_pin = trig_pin;
      ultrasonic_echo_pin = echo_pin;
      buzzer_pin = buzz_pin;
      
      pinMode(ultrasonic_trig_pin, OUTPUT);
      pinMode(ultrasonic_echo_pin, INPUT);
      pinMode(buzzer_pin, OUTPUT);
      
      // Initialize state
      blocked = false;
      block_start = 0;
      last_check = 0;
      alert_on = false;
      
      Serial.println("Obstacle Avoidance Initialized");
      Serial.println("Safety Distance: 20cm");
      Serial.println("Check Interval: 500ms");
      Serial.println("Timeout: 30s\n");
    }
    
    float getDistance() {
      // Send ultrasonic pulse
      digitalWrite(ultrasonic_trig_pin, LOW);
      delayMicroseconds(2);
      digitalWrite(ultrasonic_trig_pin, HIGH);
      delayMicroseconds(10);
      digitalWrite(ultrasonic_trig_pin, LOW);
      
      // Read echo pulse duration
      long duration = pulseIn(ultrasonic_echo_pin, HIGH);
      
      // Calculate distance in cm (speed of sound = 343 m/s)
      float distance = duration * 0.034 / 2;
      
      return distance;
    }
    
    bool check() {
      /* Check for obstacles. Returns true if path is clear, false if blocked. */
      
      unsigned long now = millis();
      float distance = getDistance();
      
      // Obstacle detected (distance < 20cm)
      if (distance < SAFETY_DISTANCE) {
        
        // First detection
        if (!blocked) {
          Serial.println("\n!!! OBSTACLE DETECTED - EMERGENCY STOP !!!");
          Serial.print("Distance: ");
          Serial.print(distance);
          Serial.println(" cm\n");
          
          blocked = true;
          block_start = now;
          last_check = now;
          alert_on = false;
        }
        
        // Check every 500ms
        if (now - last_check >= CHECK_INTERVAL) {
          float elapsed = (now - block_start) / 1000.0;
          
          Serial.print("Obstacle still present (");
          Serial.print(distance);
          Serial.print("cm) - Waiting ");
          Serial.print(elapsed, 1);
          Serial.println("s");
          
          last_check = now;
          
          // Timeout after 30 seconds
          if (elapsed >= 30.0 && !alert_on) {
            Serial.println("\n*** ALERT: Obstacle >30s - Manual intervention needed ***\n");
            alert_on = true;
            digitalWrite(buzzer_pin, HIGH);  // Turn on buzzer
          }
        }
        
        return false;  // Path blocked
      }
      
      // Path clear
      else {
        
        // Obstacle was cleared
        if (blocked) {
          float elapsed = (now - block_start) / 1000.0;
          
          Serial.print("\n*** Obstacle cleared after ");
          Serial.print(elapsed, 1);
          Serial.println("s - Resuming ***\n");
          
          blocked = false;
          alert_on = false;
          digitalWrite(buzzer_pin, LOW);  // Turn off buzzer
        }
        
        return true;  // Path clear
      }
    }
    
    bool isBlocked() {
      return blocked;
    }
    
    void reset() {
      blocked = false;
      alert_on = false;
      digitalWrite(buzzer_pin, LOW);
      Serial.println("Obstacle avoidance reset\n");
    }
};