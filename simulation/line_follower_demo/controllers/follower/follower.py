""" Controller to drive epuck to follow a line with runtime room switching and automatic return. """

from controller import Robot, Keyboard

def run_robot(robot):
    
    time_step = 32
    max_speed = 6.28
    
    # Initialize keyboard
    keyboard = Keyboard()
    keyboard.enable(time_step)
    
    # State variables
    return_mode = False
    turning_180 = False
    turn_counter = 0
    TURN_DURATION = 50  # Adjust this value based on your robot's turn speed
    at_destination = False
    at_start = True  # START AS TRUE - robot begins at start
    robot_active = False  # Robot is OFF until command is pressed
    junction_count = 0
    return_initiated = False
    forward_count_target = 0  # Store the count value when reaching destination
    turn_at_start = False  # Flag to turn at starting point
    
    print("\n*** ROBOT IS OFF - Press 1, 2, or 3 to start ***\n")

    # Motors
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    # Enable ir sensors
    left_ir = robot.getDevice('ir_left')
    left_ir.enable(time_step)
    right_ir = robot.getDevice('ir_right')
    right_ir.enable(time_step)
    centre_ir = robot.getDevice('ir_centre')
    centre_ir.enable(time_step)
    left_most_ir = robot.getDevice('left_most')
    left_most_ir.enable(time_step)
    right_most_ir = robot.getDevice('right_most')
    right_most_ir.enable(time_step)

    count = 0
    
    while robot.step(time_step) != -1:
        
        # Initialize speeds at the beginning of each loop
        left_speed = 0
        right_speed = 0
        
        # Check for keyboard input
        key = keyboard.getKey()
        
        # Forward path (going to rooms)
        if key == ord('1'):
            room = 1
            return_mode = False
            turning_180 = False
            at_destination = False
            at_start = False  # Start moving
            robot_active = True  # Activate robot
            return_initiated = False
            turn_at_start = False
            count = 0
            junction_count = 0
            forward_count_target = 0
            print("\n=== ROBOT ACTIVATED - Going to Room 1 (Turn Left) ===\n")
        elif key == ord('2'):
            room = 2
            return_mode = False
            turning_180 = False
            at_destination = False
            at_start = False  # Start moving
            robot_active = True  # Activate robot
            return_initiated = False
            turn_at_start = False
            count = 0
            junction_count = 0
            forward_count_target = 0
            print("\n=== ROBOT ACTIVATED - Going to Room 2 (Go Straight) ===\n")
        elif key == ord('3'):
            room = 3
            return_mode = False
            turning_180 = False
            at_destination = False
            at_start = False  # Start moving
            robot_active = True  # Activate robot
            return_initiated = False
            turn_at_start = False
            count = 0
            junction_count = 0
            forward_count_target = 0
            print("\n=== ROBOT ACTIVATED - Going to Room 3 (Turn Right) ===\n")
        
        # Return command - initiate return journey
        elif (key == ord('R') or key == ord('r')) and at_destination and not return_initiated:
            print(f"\n=== ROBOT ACTIVATED - Initiating 180° turn for return journey ===\n")
            print(f"Forward count was: {forward_count_target}, will return using same count\n")
            return_mode = True
            return_initiated = True
            robot_active = True  # Activate robot
            turning_180 = True
            turn_counter = 0
            count = 0
            junction_count = 0

        # ROBOT IS OFF - Do nothing, just wait for commands
        if not robot_active:
            left_speed = 0
            right_speed = 0
            left_motor.setVelocity(left_speed)
            right_motor.setVelocity(right_speed)
            continue  # Skip all other logic
        
        # ROBOT IS ACTIVE - Normal operation
        # Handle 180° turn
        if turning_180:
            turn_counter += 1
            
            if turn_at_start:
                print(f"Turning 180° at START... {turn_counter}/{TURN_DURATION}")
            else:
                print(f"Turning 180° at DESTINATION... {turn_counter}/{TURN_DURATION}")
            
            # Perform the turn (rotate in place)
            left_speed = -max_speed * 0.5
            right_speed = max_speed * 0.5
            
            # Check if turn is complete
            if turn_counter >= TURN_DURATION:
                turning_180 = False
                turn_counter = 0
                count = 0
                
                if turn_at_start:
                    print("Turn at start complete! Ready for next journey.\n")
                    print("\n*** ROBOT IS OFF - Press 1, 2, or 3 to start ***\n")
                    turn_at_start = False
                    at_start = True
                    robot_active = False  # Deactivate robot
                else:
                    print("Turn complete! Following line back to start.\n")
        
        else:
            # Normal operation (not turning 180°)
            
            # read ir sensors
            left_ir_value = left_ir.getValue()
            right_ir_value = right_ir.getValue()
            centre_ir_value = centre_ir.getValue()
            left_most_ir_value = left_most_ir.getValue()
            right_most_ir_value = right_most_ir.getValue()

            if round(left_ir_value) == round(right_ir_value) == round(centre_ir_value):
                count = count + 1

            print("-\n  {}\n  {}\n  {}\n  {}\n  {}\n".format(
                left_most_ir_value, left_ir_value, centre_ir_value, 
                right_ir_value, right_most_ir_value))
            
            mode_text = "RETURN" if return_mode else "FORWARD"
            status = "AT START" if at_start else ("AT DESTINATION" if at_destination else "TRAVELING")
            print(f"Count: {count}/{forward_count_target}, Room: {room}, Mode: {mode_text}, Status: {status}, Junctions: {junction_count}")

            # Robot is stopped at start - waiting for command
            if at_start:
                left_speed = 0
                right_speed = 0
                
            # Check if reached destination (room) - FORWARD MODE
            elif not return_mode and not at_destination:
                if (room == 2 and count > 200) or (room != 2 and count > 400):
                    print(f'\n*** REACHED ROOM {room} DESTINATION ***')
                    print(f'*** Forward count: {count} ***')
                    print('*** ROBOT IS OFF - Press R to return to start ***\n')
                    at_destination = True
                    forward_count_target = count  # Save the count value
                    robot_active = False  # Deactivate robot
                    left_speed = 0
                    right_speed = 0
                else:
                    # Continue moving forward
                    # Default speed
                    left_speed = max_speed * .1
                    right_speed = max_speed * .1

                    # Junction detection
                    if (50 > centre_ir_value > 10) and (50 > left_ir_value > 10) and (50 > right_ir_value > 10):
                        print('--------------------------------------------------')
                        junction_count += 1
                        
                        if room == 1:
                            print(f'Junction {junction_count} - Turn left (to Room 1)')
                            left_speed = -max_speed * .4
                            right_speed = +max_speed * .4
                        elif room == 2:
                            print(f'Junction {junction_count} - Go straight (to Room 2)')
                            left_speed = max_speed * .6
                            right_speed = max_speed * .6
                        elif room == 3:
                            print(f'Junction {junction_count} - Turn right (to Room 3)')
                            left_speed = max_speed * .4
                            right_speed = -max_speed * .4
                            
                    # Line following logic
                    elif (left_ir_value > right_ir_value) and (6 < left_ir_value < 15):
                        print("Go left")
                        left_speed = -max_speed * .4
                    elif (right_ir_value > left_ir_value) and (6 < right_ir_value < 15):
                        print("Go right")
                        right_speed = -max_speed * .4
                    
            # Robot is stopped at destination - waiting for R
            elif at_destination and not return_mode:
                left_speed = 0
                right_speed = 0
                
            # RETURN MODE - robot is traveling back
            elif return_mode:
                
                # Check if reached starting point - use same count as forward path
                if count >= forward_count_target:
                    print('\n*** REACHED STARTING POINT ***')
                    print(f'*** Return count: {count} (matched forward count: {forward_count_target}) ***')
                    print('*** Initiating 180° turn at starting point ***\n')
                    return_mode = False
                    at_destination = False
                    return_initiated = False
                    junction_count = 0
                    forward_count_target = 0
                    
                    # Initiate turn at starting point
                    turning_180 = True
                    turn_at_start = True
                    turn_counter = 0
                    
                    left_speed = 0
                    right_speed = 0
                else:
                    # Default speed
                    left_speed = max_speed * .1
                    right_speed = max_speed * .1

                    # Junction detection - RETURN PATH (OPPOSITE DIRECTION)
                    if (50 > centre_ir_value > 10) and (50 > left_ir_value > 10) and (50 > right_ir_value > 10):
                        print('--------------------------------------------------')
                        junction_count += 1
                        
                        if room == 1:
                            print(f'Junction {junction_count} - Turn RIGHT (returning from Room 1)')
                            left_speed = max_speed * .4
                            right_speed = -max_speed * .4
                        elif room == 2:
                            print(f'Junction {junction_count} - Go STRAIGHT (returning from Room 2)')
                            left_speed = max_speed * .6
                            right_speed = max_speed * .6
                        elif room == 3:
                            print(f'Junction {junction_count} - Turn LEFT (returning from Room 3)')
                            left_speed = -max_speed * .4
                            right_speed = +max_speed * .4
                            
                    # Line following logic
                    elif (left_ir_value > right_ir_value) and (6 < left_ir_value < 15):
                        print("Go left")
                        left_speed = -max_speed * .4
                    elif (right_ir_value > left_ir_value) and (6 < right_ir_value < 15):
                        print("Go right")
                        right_speed = -max_speed * .4

        # Set velocities
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)


if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)