# TO DO
# Why does it slow down as time goes on? Can I fix this?

# Things to Add

# User interface! So things like:
# Place to put in Picobot instructions

# If there's not a way to add a text input box, use user input and have a add instructions button
# Place that displays errors (like oops I can't go that way)
# Add a menu to choose which map you want
#--------Picobot Interpreter--------

import arcade
import random
import copy

# --- Constants ---
PAUSE = 0
PLAY = 1

# These represent levels/states so the computer knows what screen to display
ZOOM_ZOOM = 1
ALL_DONE = 2

BUTTON_SPACE = 128

# Note: current images of CRATE and BOT are each 64px by 64px
SCALING_BOX = 1 / 2

BOX_SIZE = int(SCALING_BOX * 64)

ROBOT = -1
EMPTY = 0
WALL = 1
VISITED = 2

# Button coordinates
B1X = 7*BOX_SIZE / 2
B1Y = 2*BOX_SIZE

B2X = 7.5 * BOX_SIZE
B2Y = 2*BOX_SIZE

B3X = 11.5 * BOX_SIZE
B3Y = 2*BOX_SIZE

B_BASE = 3 * BOX_SIZE
B_HEIGHT = 2 * BOX_SIZE

B_COLOR = arcade.color.RED
B_HIGHTLIGHT = (239, 146, 146)

MAZE_MAP = [
   [ 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 ],
   [ 1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,0,1 ],
   [ 1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,1 ],
   [ 1,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,0,1 ],
   [ 1,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,1,0,1 ],
   [ 1,0,1,1,1,0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1 ],
   [ 1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,0,0,1,0,0,0,1 ],
   [ 1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,1,0,1,0,1,1,1 ],
   [ 1,1,0,1,0,1,0,0,0,1,0,1,0,1,1,1,0,0,1,0,1,0,0,0,1 ],
   [ 1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1 ],
   [ 1,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,1,1,0,1 ],
   [ 1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,1,0,1,1,1,0,1,0,1 ],
   [ 1,0,1,1,1,1,1,1,0,1,0,0,1,1,1,0,1,0,0,0,1,0,1,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1,1,1,0,1,0,1,0,1 ],
   [ 1,1,1,1,1,1,1,1,1,1,0,1,0,0,1,0,0,0,1,0,1,0,1,0,1 ],
   [ 1,0,0,0,0,1,0,0,0,1,1,1,0,1,1,1,1,0,1,0,1,0,1,0,1 ],
   [ 1,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,0,1 ],
   [ 1,0,0,1,0,1,0,1,1,1,1,1,0,1,1,0,1,0,1,0,1,0,1,0,1 ],
   [ 1,0,1,1,0,1,0,1,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,0,1 ],
   [ 1,0,1,0,0,1,0,1,0,0,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1 ],
   [ 1,0,1,1,1,1,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,1 ],
   [ 1,0,0,0,0,0,0,1,0,1,1,1,0,1,0,0,0,1,1,1,0,0,0,1,1 ],
   [ 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 ] ]

EMPTY_MAP = [
   [ 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
   [ 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 ] ]

EMPTY_RULES = """0 x*** -> N 0
0 N*x* -> W 0
0 N*W* -> E 1
1 *x** -> E 1
1 *E** -> S 2
2 **x* -> W 2
2 **W* -> S 1"""

CRATE = "crate_44.png"
BOT = "crate_30.png"

#---------------------------------------------------------------
class MyGame(arcade.Window):
    """ This class represents the main window of the game. """

    def __init__(self, myMap, myRules):
        """ Initializer """


        self.myMap = copy.deepcopy(myMap)
        self.myRules = myRules
        self.myMapCopy = copy.deepcopy(myMap)

        self.NUM_ROWS = len(self.myMap)
        self.NUM_COLUMNS = len(self.myMap[0])
        
        # Call the parent class initializer
        self.WORLD_WIDTH = BOX_SIZE * (self.NUM_ROWS)
        self.WORLD_HEIGHT = BOX_SIZE * (self.NUM_COLUMNS) + BUTTON_SPACE

        super().__init__(self.WORLD_WIDTH, self.WORLD_HEIGHT, "Picobot!")

        self.background = None

        # Picobot specific!
        self.state = 0
        self.rules = {}

        self.rules = self.convertPicobotToPython()

        # This number is in x,y coordinates
        self.robot_x = None
        self.robot_y = None

        self.b1Color = B_COLOR
        self.b2Color = B_COLOR
        self.b3Color = B_COLOR

        self.pause_or_play = PLAY


    #-----------Coordinate system conversion functions-------------
    def xyToRowCol(self, coordinate):
        """Takes in a (x, y) and returns the equivalent (row, col)"""
        row = int(len(self.myMap) - 1 - coordinate[1])
        col = int(coordinate[0])
        return (row, col)

    def pixelPosToxy(self, coordinate):
        """Takes in (center_x, center_y) and return (x, y)"""
        x = (coordinate[0] - BOX_SIZE / 2)/BOX_SIZE
        y = (coordinate[1] - BOX_SIZE / 2 - BUTTON_SPACE)/BOX_SIZE
        return (x, y)

    def pixelPosToRowCol(self, coordinate):
        """Takes in (center_x, center_y) and returns (row, col)"""
        xy = self.pixelPosToxy(coordinate)
        return self.xyToRowCol(xy)

    def xyToPixelPos(self, coordinate):
        """Takes in (x, y) and returns (center_x, center_y)"""
        pixel_x = BOX_SIZE / 2 + coordinate[0] * BOX_SIZE
        pixel_y = BOX_SIZE / 2 + coordinate[1] * BOX_SIZE + BUTTON_SPACE
        return (pixel_x, pixel_y)

    def rowColToPixelPos(self, coordinate):
        """Takes in a (row, col) and returns (center_x, center_y)"""
        row, col = coordinate
        pixel_x = col * BOX_SIZE + BOX_SIZE // 2
        pixel_y = (len(self.myMap[0]) - 1 - row) * BOX_SIZE + BOX_SIZE / 2 + BUTTON_SPACE
        return (pixel_x, pixel_y)

    def rowColToxy(self, coordinate):
        """Takes in a (row, col) and returns (x, y)"""
        pixel = self.rowColToPixelPos(coordinate)
        return self.pixelPosToxy(pixel)
    
    def setup(self):
        """Used as a reset to Picobot defaults"""
        # Set the background color
        arcade.set_background_color((135, 205, 255))

        # Set opening screen
        self.current_state = ZOOM_ZOOM
        self.state = 0

        # Reset start map
        self.myMap = copy.deepcopy(self.myMapCopy)

        rand_x = random.randint(1,len(self.myMap[0]) - 2)
        rand_y = random.randint(1, len(self.myMap) - 2)
        
        # make sure that it's not starting on a wall
        coord = (rand_x, rand_y)
        while self.isWall(coord):
            rand_x = random.randint(1,len(self.myMap[0]) - 2)
            rand_y = random.randint(1, len(self.myMap) - 2)
            coord = (rand_x, rand_y)
        
        self.robot_x, self.robot_y = coord
        row, col = self.xyToRowCol(coord)
        self.myMap[row][col] = -1

        self.pause_or_play = PLAY

    def on_draw(self):
        """draw the graphics"""
        arcade.start_render()

        self.draw_game()

    def draw_game(self):
        """Draw the main game"""
        # Draw squares where Picobot has visited and the walls
        for row in range(len(self.myMap)):
            for col in range(len(self.myMap[0])):
                if self.myMap[row][col] == VISITED:
                    x, y = self.rowColToPixelPos([row, col])
                    arcade.draw_rectangle_filled(x, y, BOX_SIZE, BOX_SIZE, arcade.color.GREEN)

                elif self.myMap[row][col] == WALL:
                    x, y = self.rowColToPixelPos([row, col])
                    wall_image = arcade.load_texture(CRATE)
                    arcade.draw_texture_rectangle(x, y, SCALING_BOX * wall_image.width, SCALING_BOX * wall_image.height, wall_image)

                elif self.myMap[row][col] == ROBOT:
                    x, y = self.rowColToPixelPos([row, col])
                    bot_image = arcade.load_texture(BOT)
                    arcade.draw_texture_rectangle(x, y, SCALING_BOX * bot_image.width, SCALING_BOX * bot_image.height, bot_image)

                elif self.myMap[row][col] == EMPTY:
                    x, y = self.rowColToPixelPos([row, col])
                    arcade.draw_rectangle_filled(x, y, BOX_SIZE, BOX_SIZE, arcade.color.WHITE)

        # Draw the Grid
        # Draw horizontal lines
        for row in range(0, self.WORLD_HEIGHT + 1, BOX_SIZE):
            arcade.draw_line(0, row, self.WORLD_WIDTH, row, arcade.color.BLACK, 1)

        # Draw horizontal lines
        for col in range(0, self.WORLD_WIDTH + 1, BOX_SIZE):
            arcade.draw_line(col, 0, col, self.WORLD_HEIGHT, arcade.color.BLACK, 1)

        if self.current_state == ALL_DONE:
            self.draw_game_over()

        # Draw the menu buttons
        arcade.draw_rectangle_filled(B1X, B1Y, B_BASE, B_HEIGHT, self.b1Color)
        arcade.draw_text("Restart", 5*BOX_SIZE / 2, 2*BOX_SIZE, arcade.color.WHITE, 12)

        # Buttons to Add: enter new rules
        
        # Pause/Play
        arcade.draw_rectangle_filled(B2X, B2Y, B_BASE, B_HEIGHT, self.b2Color)
        arcade.draw_text("Pause/Play", 12*BOX_SIZE/2, 2*BOX_SIZE, arcade.color.WHITE, 12)

        # switch map
        arcade.draw_rectangle_filled(B3X, B3Y, B_BASE, B_HEIGHT, self.b3Color)
        arcade.draw_text("Change Map", 10*BOX_SIZE, 2*BOX_SIZE, arcade.color.WHITE, 12)


    def draw_game_over(self):
        """Draw the ending screen"""
        arcade.draw_text("Congratulations!", 100, 400, arcade.color.WHITE, 54)

    def update(self, delta_time):
        """updates the position of picobot"""

        if self.current_state == ZOOM_ZOOM:
            self.step()

        if self.allVisited():
            coord = (self.robot_x, self.robot_y)
            self.markVisited(coord)
            self.current_state = ALL_DONE

    def allVisited(self):
        """Takes in a maze and returns True if there are no 2's left,
        so Picobot has visited every cell"""
        for row in self.myMap:
            for col in row:
                if col == 0:
                    return False
        return True


    def getCurrentSurroundings(self):
        """Returns the current surroundings of self.player_sprite in the form of "xxxx" in a String"""
        position = ""

        # convert center_x and center_y to a row/column in the map
        x = self.robot_x
        y = self.robot_y
        
        row, col = self.xyToRowCol([x, y])

        # Look North
        if self.myMap[row - 1][col] == 1:
            position += "N"
        else:
            position += "x"

        # Look East
        if self.myMap[row][col + 1] == 1:
            position += "E"
        else:
            position += "x"

        # Look West
        if self.myMap[row][col - 1] == 1:
            position += "W"
        else:
            position += "x"

        # Look South
        if self.myMap[row + 1][col] == 1:
            position += "S"
        else:
            position += "x"

        return position

    def getMove(self, state, surroundings):
        """Reads self.rules to find next move"""
        return self.rules[(state, surroundings)]
    
    def step(self):
        """moves Picobot one step and updates state, row, col of Picobot"""
        if self.pause_or_play == PLAY:
            coord = [self.robot_x, self.robot_y]
            self.markVisited(coord)
            surroundings = self.getCurrentSurroundings()
            direction, newState = self.getMove(self.state, surroundings)
            self.state = newState

            row, col = self.xyToRowCol(coord)

            # Change self.robot_x and self.robot_y based on direction
            # check if bot can move that direction
            if direction == "N":
                if surroundings[0] == "x":
                    row += -1
                else:
                    print("Cannot move North. Error in instructions.")
            elif direction == "E":
                if surroundings[1] == "x":
                    col += 1
                else:
                    print("Cannot move East. Error in instructions.")
            elif direction == "W":
                if surroundings[2] == "x":
                    col += -1
                else:
                    print("Cannot move West. Error in instructions.")
            elif direction == "S":
                if surroundings[3] == "x":
                    row += 1
                else:
                    print("Cannot move South. Error in instructions.")

            # Move Picobot to the new position
            self.myMap[row][col] = ROBOT
            self.robot_x, self.robot_y = self.rowColToxy([row, col])

    def convertPicobotToPython(self):
        """Takes in instructions as a long string and returns a dictionary of these rules"""
        # This assumes that the formatting of the rules is perfect, and that there's no comments
        ruleDict = {}
        # Each instruction is 14 characters long (including /n)
        instructions = self.myRules
        for c in range(0, len(instructions), 14):
            rule = instructions[c:c+13]
            startState = int(rule[0])
            startCondition = rule[2:6]
            newDirection = rule[10]
            newState = int(rule[12])
            
            ruleDict[(startState, startCondition)] = (newDirection, newState)

        self.fixDictionary(ruleDict)

        return ruleDict

    def deepStarDetection(self, dictionary):
        """Takes in a dictionary, and returns True while some start condition contains a *"""
        keyList = dictionary.keys()
        for key in keyList:
            if "*" in key[1]:
                return True
        return False

    def fixDictionary(self, dictionary):
        """Takes in a dictionary, and edits that dictionary until none of the conditions in
        the keys contain "*". """
        # General logic: only make one change at a time if a key has multiple *'s,
        # starting with *'s on the left
        while self.deepStarDetection(dictionary):
            keyList = list(dictionary.keys())
            for key in keyList:
                initialState = key[0]
                condition = key[1]
                entry = dictionary[key]
                if condition[0] == "*":
                    cond1 = "N" + condition[1:]
                    dictionary[(initialState, cond1)] = entry

                    cond2 = "x" + condition[1:]
                    dictionary[(initialState, cond2)] = entry

                    del dictionary[key]

                elif condition[1] == "*":
                    cond1 = condition[0] + "E" + condition[2:]
                    dictionary[(initialState, cond1)] = entry

                    cond2 = condition[0] + "x" + condition[2:]
                    dictionary[(initialState, cond2)] = entry

                    del dictionary[key]
                
                elif condition[2] == "*":
                    cond1 = condition[:2] + "W" + condition[3]
                    dictionary[(initialState, cond1)] = entry

                    cond2 = condition[:2] + "x" + condition[3]
                    dictionary[(initialState, cond2)] = entry

                    del dictionary[key]

                elif condition[3] == "*":
                    cond1 = condition[:3] + "S"
                    dictionary[(initialState, cond1)] = entry

                    cond2 = condition[:3] + "x"
                    dictionary[(initialState, cond2)] = entry

                    del dictionary[key]

    def isWall(self, coordinate):
        """Takes in (x, y), Returns True if the given coordinate is a wall in the given maze"""
        row, col = self.xyToRowCol(coordinate)
        if self.myMap[row][col] == 1:
            return True
        else:
            return False

    def markVisited(self, coordinate):
        """Takes in (x, y), Returns True if the given coordinate has been visited in the given maze"""
        row, col = self.xyToRowCol(coordinate)
        self.myMap[row][col] = 2

    def on_mouse_press(self, x, y, button, modifiers):
        """handles mouse clicks"""
        if self.onButton(x, y):
            self.buttonPress(x, y)

    def on_mouse_motion(self, x, y, dx, dy):
        """handles mouse motion"""
        if self.onButton(x, y):
            self.buttonHighlight(x, y)
        else:
            self.buttonOff(x, y)

    def onButton(self, x, y):
        """Returns True if inputted coordinates is on a button"""

        # Check button 1
        if (BOX_SIZE * 2 < x < BOX_SIZE * 5) and (BOX_SIZE < y < BOX_SIZE * 3):
            return True
        
        # Check button 2
        elif (BOX_SIZE * 6 < x < BOX_SIZE * 9) and (BOX_SIZE < y < BOX_SIZE * 3):
            return True

        # Check button 3
        elif (BOX_SIZE * 10 < x < BOX_SIZE * 13) and (BOX_SIZE < y < BOX_SIZE * 3):
            return True

        else:
            return False

    def buttonHighlight(self, x, y):
        """Changes the color of the button at the indicated coordinates to be highlighted,
        makes the rest of the buttons unhighlighted"""
        if (BOX_SIZE * 2 < x < BOX_SIZE * 5) and (BOX_SIZE < y < BOX_SIZE * 3):
            self.b1Color = B_HIGHTLIGHT

            self.b2Color = B_COLOR
            self.b3Color = B_COLOR

        elif (BOX_SIZE * 6 < x < BOX_SIZE * 9) and (BOX_SIZE < y < BOX_SIZE * 3):
            self.b2Color = B_HIGHTLIGHT

            self.b1Color = B_COLOR
            self.b3Color = B_COLOR

        elif (BOX_SIZE * 10 < x < BOX_SIZE * 13) and (BOX_SIZE < y < BOX_SIZE * 3):
            self.b3Color = B_HIGHTLIGHT

            self.b1Color = B_COLOR
            self.b2Color = B_COLOR

    def buttonOff(self, x, y):
        """Makes sure all buttons are not highlighted"""
        self.b1Color = B_COLOR
        self.b2Color = B_COLOR
        self.b3Color = B_COLOR

    def buttonPress(self, x, y):
        """Runs the correct function based on the button at (x, y)"""
        if (BOX_SIZE * 2 < x < BOX_SIZE * 5) and (BOX_SIZE < y < BOX_SIZE * 3):
            self.setup()
        
        elif (BOX_SIZE * 6 < x < BOX_SIZE * 9) and (BOX_SIZE < y < BOX_SIZE * 3):
            self.pausePlay()
        
        elif (BOX_SIZE * 10 < x < BOX_SIZE * 13) and (BOX_SIZE < y < BOX_SIZE * 3):
            self.changeMap()

    def pausePlay(self):
        """Pauses or plays the game"""
        if self.pause_or_play == PLAY:
            self.pause_or_play = PAUSE

        elif self.pause_or_play == PAUSE:
            self.pause_or_play = PLAY

    def changeMap(self):
        """Changes the map displayed"""

def main():
    window = MyGame(EMPTY_MAP, EMPTY_RULES)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()