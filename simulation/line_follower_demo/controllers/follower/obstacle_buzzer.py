""" Simple Obstacle Avoidance Module with Buzzer """

class ObstacleAvoidance:
    
    def __init__(self, robot, time_step):
        # Thresholds
        self.SAFETY_DISTANCE = 0.20  # 20 cm
        self.CHECK_INTERVAL = 500    # 500 ms
        self.TIMEOUT = 30000         # 30 seconds
        
        # State
        self.blocked = False
        self.block_start = 0
        self.last_check = 0
        self.alert_on = False
        
        # Devices
        self.ultrasonic = robot.getDevice('ultrasonic')
        self.ultrasonic.enable(time_step)
        self.buzzer = robot.getDevice('buzzer')
        self.robot = robot
    
    def check(self):
        """Check for obstacles. Returns True if path is clear, False if blocked."""
        
        now = self.robot.getTime() * 1000  # Get time in milliseconds
        distance = self.ultrasonic.getValue()
        
        # Obstacle detected (distance < 20cm)
        if distance < self.SAFETY_DISTANCE:
            
            # First detection
            if not self.blocked:
                print(f"\n!!! OBSTACLE DETECTED at {distance:.2f}m - EMERGENCY STOP !!!\n")
                self.blocked = True
                self.block_start = now
                self.last_check = now
                self.alert_on = False
            
            # Check every 500ms
            if now - self.last_check >= self.CHECK_INTERVAL:
                elapsed = (now - self.block_start) / 1000
                print(f"Obstacle still present ({distance:.2f}m) - Waiting {elapsed:.1f}s")
                self.last_check = now
                
                # Timeout after 30 seconds
                if elapsed >= 30 and not self.alert_on:
                    print("\n*** ALERT: Obstacle >30s - Manual intervention needed ***\n")
                    self.alert_on = True
                    self.buzzer.set(1)  # Turn on buzzer
            
            return False  # Path blocked
        
        # Path clear
        else:
            
            # Obstacle was cleared
            if self.blocked:
                elapsed = (now - self.block_start) / 1000
                print(f"\n*** Obstacle cleared after {elapsed:.1f}s - Resuming ***\n")
                self.blocked = False
                self.alert_on = False
                self.buzzer.set(0)  # Turn off buzzer
            
            return True  # Path clear