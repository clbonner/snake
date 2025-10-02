from machine import Pin,PWM
from picolcd144 import *
import time, random

class Snake():
    def __init__(self, level, LCD):
        self.LCD = LCD
        
        # the screen size is divided up into 8x8 pixel squares where the snake or fruit is placed
        self.height = int(self.LCD.height / 8)
        self.width = int(self.LCD.width / 8)

        # key0 = down / key1 = left / key2 = right / key3 = up
        self.up = Pin(3 ,Pin.IN,Pin.PULL_UP)
        self.left = Pin(17,Pin.IN,Pin.PULL_UP) 
        self.right = Pin(2 ,Pin.IN,Pin.PULL_UP)
        self.down = Pin(15,Pin.IN,Pin.PULL_UP)

        # snake coordinates - direction is compass positions N,E,S,W
        self.coordinates = [{'x': int(self.width / 2), 'y': int(self.height / 2)}]
        self.direction = 'N'

        # game attributes
        self.fruit_left = 15
        self.fruit_eaten = False
        self.game_over = False

        # levels are defined by the speed (ms) that the snake moves
        self.CURRENT_LEVEL = level
        if level == 1: self.SPEED = 350
        if level == 2: self.SPEED = 300
        if level == 3: self.SPEED = 250
        if level == 4: self.SPEED = 225
        if level == 5: self.SPEED = 200
    
    # these two functions return relative screen width or height given a percentage
    def pWidth(self, percent):
        return int((self.LCD.width / 100) * percent)
    
    def pHeight(self, percent):
        return int((self.LCD.height / 100) * percent)
    
    def setFruitLocation(self):
        # location minus 2 to account for border
        self.fruit_coordinates = {
            'x': random.randint(1, int(self.width) - 2), 
            'y': random.randint(1, int(self.height) - 2)
        }
        for location in self.coordinates:
            if (location == self.fruit_coordinates):
                self.setFruitLocation()

    def drawFruit(self):
        self.LCD.fill_rect(
            self.fruit_coordinates['x'] * 8, 
            self.fruit_coordinates['y'] * 8, 8, 8, 
            self.LCD.BLUE
        )

    def isFruitEaten(self):
        if (self.coordinates[0] == self.fruit_coordinates):
            self.fruit_left -= 1
            if self.fruit_left == 0:
                self.gameWon()
            else:
                self.setFruitLocation()
                self.drawFruit()
                self.growSnake()
                self.checkOutOfBounds()
            return True
        return False

    def drawSnake(self):
        for location in self.coordinates:
            self.LCD.fill_rect(location['x'] * 8, location['y'] * 8, 8, 8, self.LCD.GREEN)
            # draw eyes on the head of the snake
            if self.coordinates.index(location) == 0:
                self.LCD.fill_rect(location['x'] * 8 + 5, location['y'] * 8 + 2, 2, 2, self.LCD.BLACK)
                self.LCD.fill_rect(location['x'] * 8 + 1, location['y'] * 8 + 2, 2, 2, self.LCD.BLACK)
        self.LCD.show()

    # removes end snake position from screen
    def clearSnake(self, location):
        self.LCD.fill_rect(location['x'] * 8, location['y'] * 8, 8, 8, self.LCD.BLACK)

    # advances snake by one position and removes last list item
    def moveSnake(self):
        head = self.coordinates[0]
        if (self.direction == 'N'):
            self.coordinates.insert(0, {'x': head['x'], 'y': head['y'] - 1})
        if (self.direction == 'E'):
            self.coordinates.insert(0, {'x': head['x'] + 1, 'y': head['y']})
        if (self.direction == 'S'):
            self.coordinates.insert(0, {'x': head['x'], 'y': head['y'] + 1})
        if (self.direction == 'W'):
            self.coordinates.insert(0, {'x': head['x'] - 1, 'y': head['y']})

        self.checkOutOfBounds()
        self.clearSnake(self.coordinates.pop(len(self.coordinates) - 1))

    # inserts a new head at the start of the list
    def growSnake(self):
        head = self.coordinates[0]
        if (self.direction == 'N'):
            self.coordinates.insert(0, {'x': head['x'], 'y': head['y'] - 1})
        if (self.direction == 'E'):
            self.coordinates.insert(0, {'x': head['x'] + 1, 'y': head['y']})
        if (self.direction == 'S'):
            self.coordinates.insert(0, {'x': head['x'], 'y': head['y'] + 1})
        if (self.direction == 'W'):
            self.coordinates.insert(0, {'x': head['x'] - 1, 'y': head['y']})

    def checkForDirectionChange(self):
        if (self.up.value() == 0 and self.direction != 'S'):
            self.direction = 'N'
        if (self.right.value() == 0 and self.direction != 'W'):
            self.direction = 'E'
        if (self.down.value() == 0 and self.direction != 'N'):
            self.direction = 'S'
        if (self.left.value() == 0 and self.direction != 'E'):
            self.direction = 'W'

    def checkOutOfBounds(self):
        # check if snake head hits the border
        if (self.coordinates[0]['y'] <  1 or
            self.coordinates[0]['x'] > self.width - 2 or
            self.coordinates[0]['y'] > self.height - 2 or
            self.coordinates[0]['x'] < 1):
                self.gameOver()

        # check if head hits another part of the snake
        head = self.coordinates[0]
        for index in range(1, len(self.coordinates) - 1):
            if (self.coordinates[index] == head):
                self.gameOver()

    def gameOver(self):
        self.setBorder(self.LCD.RED)
        self.endGameEffect()
        self.LCD.text("GAME OVER", self.pWidth(22), self.pHeight(45), self.LCD.RED)
        self.LCD.show()

        self.game_over = True
        self.waitForKeyPress()
    
    def gameWon(self):
        self.endGameEffect()
        if (self.CURRENT_LEVEL < 5):
            self.LCD.text("LEVEL", self.pWidth(37), self.pHeight(40), self.LCD.RED)
            self.LCD.text("COMPLETE!", self.pWidth(25), self.pHeight(50), self.LCD.RED)
            self.CURRENT_LEVEL += 1
        else:
            self.LCD.text("YOU WIN!", self.pWidth(28), self.pHeight(45), self.LCD.RED)
            self.CURRENT_LEVEL = 1

        self.LCD.show()
        self.game_over = True
        self.waitForKeyPress()

    def endGameEffect(self):
        for n in range(8, self.pHeight(50)):
            self.LCD.rect(n, n, self.LCD.width - n * 2, self.LCD.height - n * 2, self.LCD.GREEN)
            self.LCD.show()
    
    def setBorder(self, color):
            for n in range(0, 8):
                self.LCD.hline(n, n, self.LCD.width, color)
                self.LCD.hline(n, (self.LCD.height - 1) - n, self.LCD.width, color)
                self.LCD.vline(n, n, self.LCD.height, color)
                self.LCD.vline((self.LCD.width - 1) - n, n, self.LCD.height, color)

    def instructions(self):
        self.LCD.fill(self.LCD.BLACK)
        self.LCD.text("Move UP", self.pWidth(10), self.pHeight(5), self.LCD.WHITE)
        self.LCD.text("Move RIGHT", self.pWidth(10), self.pHeight(32), self.LCD.WHITE)
        self.LCD.text("Move LEFT", self.pWidth(10), self.pHeight(59), self.LCD.WHITE)
        self.LCD.text("Move DOWN", self.pWidth(10), self.pHeight(86), self.LCD.WHITE)
        # arrow 1
        self.LCD.hline(self.pWidth(80), self.pHeight(8), 20, self.LCD.WHITE)
        self.LCD.line(self.pWidth(98), self.pHeight(8), self.pWidth(95), self.pHeight(5), self.LCD.WHITE)
        self.LCD.line(self.pWidth(98), self.pHeight(8), self.pWidth(95), self.pHeight(11), self.LCD.WHITE)
        # arrow 2
        self.LCD.hline(self.pWidth(80), self.pHeight(35), 20, self.LCD.WHITE)
        self.LCD.line(self.pWidth(98), self.pHeight(35), self.pWidth(95), self.pHeight(32), self.LCD.WHITE)
        self.LCD.line(self.pWidth(98), self.pHeight(35), self.pWidth(95), self.pHeight(38), self.LCD.WHITE)
        # arrow 3
        self.LCD.hline(self.pWidth(80), self.pHeight(62), 20, self.LCD.WHITE)
        self.LCD.line(self.pWidth(98), self.pHeight(62), self.pWidth(95), self.pHeight(59), self.LCD.WHITE)
        self.LCD.line(self.pWidth(98), self.pHeight(62), self.pWidth(95), self.pHeight(65), self.LCD.WHITE)
        # arrow 4
        self.LCD.hline(self.pWidth(80), self.pHeight(89), 20, self.LCD.WHITE)
        self.LCD.line(self.pWidth(98), self.pHeight(89), self.pWidth(95), self.pHeight(85.5), self.LCD.WHITE)
        self.LCD.line(self.pWidth(98), self.pHeight(89), self.pWidth(95), self.pHeight(92), self.LCD.WHITE)
        self.LCD.show()

        self.waitForKeyPress()

    # waits for any key to be pressed before continuing
    def waitForKeyPress(self):
        while (True):
            time.sleep_ms(100)
            if (self.left.value() == 0 or
                self.right.value() == 0 or
                self.up.value() == 0 or
                self.down.value() == 0):
                    return

    def startGame(self):
        self.LCD.fill(self.LCD.BLACK)
        self.setBorder(self.LCD.WHITE)
        self.growSnake()
        self.setFruitLocation()
        self.drawFruit()

        while (not self.game_over):
            self.drawSnake()
            for n in range(self.SPEED):
                self.checkForDirectionChange()
                time.sleep_ms(1)
            if (not self.isFruitEaten()):
                self.moveSnake()

    def welcomeScreen(self):
        level_text = "LEVEL " + str(self.CURRENT_LEVEL)

        self.LCD.fill(self.LCD.BLACK)
        self.LCD.text("SNAKE", self.pWidth(35), self.pHeight(20), self.LCD.GREEN)
        self.LCD.text(level_text, self.pWidth(29), self.pHeight(40), self.LCD.GREEN)
        self.LCD.text("Press any key", self.pWidth(8), self.pHeight(60), self.LCD.WHITE)
        self.LCD.text("to start", self.pWidth(25), self.pHeight(70), self.LCD.WHITE)
        self.LCD.show()

        self.waitForKeyPress()
        self.instructions()
        self.startGame()
    
    def play(self):
        self.welcomeScreen()
        return self.CURRENT_LEVEL

if __name__=='__main__':

    # init display
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32000)#max 65535
    LCD = LCD_1inch44()

    # init game
    level = 1
    while level <= 5:
        game = Snake(level, LCD)
        level = game.play()