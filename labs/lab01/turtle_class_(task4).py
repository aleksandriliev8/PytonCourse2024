class Turtle:
    #initializator method
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.count = 0
        self.moves = []

    def get_current_position(self):
        return (self.x, self.y)

    def move(self, *args):
        for command in args:
            if command == 'up':
                self.y += 1
                self.count += 1
                self.moves.append(command)

            elif command == 'down':
                self.y -= 1
                self.count += 1
                self.moves.append(command)

            elif command == 'left':
                self.x -= 1
                self.count += 1
                self.moves.append(command)

            elif command == 'right':
                self.x += 1
                self.count += 1
                self.moves.append(command)

            else:
                print(f"Invalid command: {command}")

    def configure_turtle(self, **kwargs):
        print_msg = "Current configuration:"

        for parameter, value in kwargs.items():
            print_msg += f" {parameter}:{value} |"

        return print_msg

    def check_for_drawing(self, commands):
        isDrawing = True
        prev_command = ''

        for i in range(len(commands)):
            if i == 0:
                prev_command = commands[i]
            elif (commands[i] == 'up' and prev_command == 'down') or (
                  commands[i] == 'down' and prev_command == 'up') or (
                  commands[i] == 'left' and prev_command == 'right') or (
                  commands[i] == 'right' and prev_command == 'left'):
                  isDrawing = False
                  break
            else:
                prev_command = commands[i]
        
        return isDrawing

    def __str__(self):
        return f"Turtle is at position ({self.x},{self.y}) and has moved {self.count} times since start"


# Test Case 1: Test Turtle Initialization with default coordinates (0, 0)
t1 = Turtle()
assert t1.x == 0 and t1.y == 0, "Initial position should be (0,0)"
assert str(t1) == "Turtle is at position (0,0) and has moved 0 times since start", "String representation is incorrect"

# Test Case 2: Test move method with valid moves
t1.move('up', 'right', 'down', 'left')
assert t1.x == 0 and t1.y == 0, "Turtle should return to (0,0) after up, right, down, left"
assert len(t1.moves) == 4, "Turtle should have 4 moves recorded"
assert str(t1) == "Turtle is at position (0,0) and has moved 4 times since start", "String representation after 4 moves is incorrect"

# Test Case 3: Test move method with invalid move
t1.move('right', 'testing', 'right', 'left')
assert len(t1.moves) == 7, "Invalid move should not be added to the move list"
assert str(t1) == "Turtle is at position (1,0) and has moved 7 times since start", "Invalid move should not affect the position or count of moves"

# Test Case 4: Test Turtle Initialization with custom coordinates
t2 = Turtle(3, 4)
assert t2.x == 3 and t2.y == 4, "Initial position should be (3,4)"
assert str(t2) == "Turtle is at position (3,4) and has moved 0 times since start", "String representation with custom initial coordinates is incorrect"

# Test Case 5: Test move method with different valid moves
t2.move('up', 'up', 'right')
assert t2.x == 4 and t2.y == 6, "Turtle should be at (4,6) after moving up twice and right"
assert len(t2.moves) == 3, "Turtle should have 3 moves recorded"
assert str(t2) == "Turtle is at position (4,6) and has moved 3 times since start", "String representation after custom moves is incorrect"

# Test Case 6: Test configure_turtle method
config_message = t2.configure_turtle(color="green", thickness=2, size=10)
assert config_message == "Current configuration: color:green | thickness:2 | size:10 |", "Configuration message is incorrect"

# Test Case 7: Test check_for_drawing method with existing drawing
t2.move('down', 'down', 'left')
assert t2.check_for_drawing(['up', 'right', 'down']) is True, "Drawing sequence should match recorded moves"
assert t2.check_for_drawing(['up', 'up', 'right', 'left']) is False, "Invalid drawing sequence should not match recorded moves"

# Test Case 8: Test get_current_position method 
assert t2.get_current_position() == (3, 4), "Current position should be (3,4) after initial moves"