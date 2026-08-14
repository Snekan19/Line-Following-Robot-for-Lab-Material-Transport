void followLine() {
    // Read IR sensor values
    float left_ir_value = analogRead(LEFT_IR_PIN);
    float right_ir_value = analogRead(RIGHT_IR_PIN);
    float centre_ir_value = analogRead(CENTRE_IR_PIN);
    
    // Default speed
    float left_speed = max_speed * 0.1;
    float right_speed = max_speed * 0.1;

    // Junction detection - all three middle sensors detect line
    if ((centre_ir_value > 10 && centre_ir_value < 50) && 
        (left_ir_value > 10 && left_ir_value < 50) && 
        (right_ir_value > 10 && right_ir_value < 50)) {
        
        Serial.println("--------------------------------------------------");
        junction_count++;
        
        if (room == 1) {
            Serial.print("Junction ");
            Serial.print(junction_count);
            Serial.println(" - Turn left (to Room 1)");
            left_speed = -max_speed * 0.4;
            right_speed = max_speed * 0.4;
        }
        else if (room == 2) {
            Serial.print("Junction ");
            Serial.print(junction_count);
            Serial.println(" - Go straight (to Room 2)");
            left_speed = max_speed * 0.6;
            right_speed = max_speed * 0.6;
        }
        else if (room == 3) {
            Serial.print("Junction ");
            Serial.print(junction_count);
            Serial.println(" - Turn right (to Room 3)");
            left_speed = max_speed * 0.4;
            right_speed = -max_speed * 0.4;
        }
    }
    // Line following logic
    else if ((left_ir_value > right_ir_value) && (left_ir_value > 6 && left_ir_value < 15)) {
        Serial.println("Go left");
        left_speed = -max_speed * 0.4;
        right_speed = right_speed; // Keep right at default
    }
    else if ((right_ir_value > left_ir_value) && (right_ir_value > 6 && right_ir_value < 15)) {
        Serial.println("Go right");
        left_speed = left_speed; // Keep left at default
        right_speed = -max_speed * 0.4;
    }

    // Apply motor speeds
    setMotorSpeed(LEFT_MOTOR, left_speed);
    setMotorSpeed(RIGHT_MOTOR, right_speed);
}