# TO DO
# Why does it slow down as time goes on? Can I fix this?

# Things to Add

# User interface! So things like:
# Place to put in Picobot instructions
# Way to restart
# Place that displays errors (like oops I can't go that way)
# Add a menu to choose which map you want
#--------Picobot Interpreter--------

import arcade
import random
import time

# --- Constants ---
POSSIBLE_CONDITIONS = ["xxxx", "Nxxx", "NExx", "NxWx", "xxxS", "xExS", "xxWS", "xExx", "xxWx"]
POSSIBLE_MOVES = ["N", "E", "W", "S"]

# These represent levels/states so the computer knows what screen to display
ZOOM_ZOOM = 1

ALL_DONE = 2

PAUSE = 10

SCREEN_WIDTH = 25 * 33
SCREEN_HEIGHT = 25 * 33

# Note: current images of CRATE and BOT are each 64px by 64px
SPRITE_SCALING_BOX = 1 / 2
SPRITE_SCALING_PLAYER = 1 / 2

BOX_SIZE = 64 // 2

ROBOT = -1
WALL = 1
VISITED = 2

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
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Picobot!")

        self.myMap = myMap
        self.myRules = myRules

        # Sprite lists
        self.player_list = None
        self.wall_list = None

        # Set up player
        self.player_sprite = None

        # physics engine
        self.physics_engine = None

        # Manage the view port
        self.view_left = 0
        self.view_bottom = 0

        self.background = None

        # Picobot specific!
        self.state = 0
        self.rules = {}
        #self.randomize()
        self.rules = self.convertPicobotToPython()

        self.NUM_ROWS = len(self.myMap)
        self.NUM_COLUMNS = len(self.myMap[0])

        self.WORLD_WIDTH = BOX_SIZE * (self.NUM_ROWS)
        self.WORLD_HEIGHT = BOX_SIZE * (self.NUM_COLUMNS)


        # This number is in x,y coordinates
        self.robot_x = None
        self.robot_y = None

        MOVEMENT_SPEED = BOX_SIZE


    #-----------Coordinate system conversion functions-------------
    def xyToRowCol(self, coordinate):
        """Takes in a (x, y) and returns the equivalent (row, col)"""
        row = int(len(self.myMap) - 1 - coordinate[1])
        col = int(coordinate[0])
        return (row, col)

    def pixelPosToxy(self, coordinate):
        """Takes in (center_x, center_y) and return (x, y)"""
        return list(map((lambda S: int((S - (BOX_SIZE / 2)) / BOX_SIZE )), coordinate))

    def pixelPosToRowCol(self, coordinate):
        """Takes in (center_x, center_y) and returns (row, col)"""
        xy = self.pixelPosToxy(coordinate)
        return self.xyToRowCol(xy)

    def xyToPixelPos(self, coordinate):
        """Takes in (x, y) and returns (center_x, center_y)"""
        pixel_x = BOX_SIZE // 2 + coordinate[0] * BOX_SIZE
        pixel_y = BOX_SIZE // 2 + coordinate[1] * BOX_SIZE
        return (pixel_x, pixel_y)

    def rowColToPixelPos(self, coordinate):
        """Takes in a (row, col) and returns (center_x, center_y)"""
        row, col = coordinate
        pixel_x = col * BOX_SIZE + BOX_SIZE // 2
        pixel_y = (len(self.myMap[0]) - 1 - row) * BOX_SIZE + BOX_SIZE // 2
        return (pixel_x, pixel_y)

    def rowColToxy(self, coordinate):
        """Takes in a (row, col) and returns (x, y)"""
        pixel = self.rowColToPixelPos(coordinate)
        return self.pixelPosToxy(pixel)

    def randomize(self):
        """Fill self.rules!"""
        for state in range(5):
            for condition in POSSIBLE_CONDITIONS:
                newState = random.randint(0, 4)
                newMove = random.choice(POSSIBLE_MOVES)
                while newMove in condition:
                    newMove = random.choice(POSSIBLE_MOVES)
                self.rules[(state, condition)] = (newMove, newState)
    
    def setup(self):
        # Set the background color
        arcade.set_background_color((135, 205, 255))

        # Set opening screen
        self.current_state = ZOOM_ZOOM


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

        # Create the maze
        for row in range(len(self.myMap)):
            for col in range(len(self.myMap[0])):
                if self.myMap[row][col] == WALL:
                    x, y = self.rowColToPixelPos([row, col])
                    arcade.draw_rectangle_filled(x, y, BOX_SIZE, BOX_SIZE, arcade.color.BLUE)


    def on_draw(self):
        arcade.start_render()

        if self.current_state == ZOOM_ZOOM:
            self.draw_game()

        elif self.current_state == ALL_DONE:
            self.draw_game_over()

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
                    arcade.draw_rectangle_filled(x, y, BOX_SIZE, BOX_SIZE, arcade.color.BLUE)
                elif self.myMap[row][col] == ROBOT:
                    x, y = self.rowColToPixelPos([row, col])
                    arcade.draw_rectangle_filled(x, y, BOX_SIZE, BOX_SIZE, arcade.color.RED)
        
        # Draw the Grid
        # Draw horizontal lines
        for row in range(0, self.WORLD_HEIGHT + 1, BOX_SIZE):
            arcade.draw_line(0, row, self.WORLD_WIDTH, row, arcade.color.BLACK, 2)

        # Draw horizontal lines
        for col in range(0, self.WORLD_WIDTH + 1, BOX_SIZE):
            arcade.draw_line(col, 0, col, self.WORLD_HEIGHT, arcade.color.BLACK, 2)


    def draw_game_over(self):
        """Draw the ending screen"""
        arcade.draw_text("Congratulations!", 200, 400, arcade.color.WHITE, 54)


    def update(self, delta_time):
        """updates the position of picobot"""

        # convert coord to x,y
        coord = (self.robot_x, self.robot_y)
        self.markVisited(coord)

        self.step()

        if self.allVisited():
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
        surroundings = self.getCurrentSurroundings()
        direction, newState = self.getMove(self.state, surroundings)
        self.state = newState

        row, col = self.xyToRowCol([self.robot_x, self.robot_y])

        # Change self.player_sprite.center_x and self.player_sprite.center_y based on direction
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



def main():
    window = MyGame(EMPTY_MAP, EMPTY_RULES)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()