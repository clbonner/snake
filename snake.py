from machine import Pin,PWM
from picolcd144 import *
import time, random

class Snake():
    def __init__(self, level, LCD):
        self.LCD = LCD
        self.LCD.fill(self.LCD.BLACK)
        self.LCD.show()

        # the screen size is divided up into 8x8 pixel squares
        self.height = int(self.LCD.height / 8)
        self.width = int(self.LCD.width / 8)

        # key0 = down / key1 = left / key2 = right / key3 = up
        self.up = Pin(3 ,Pin.IN,Pin.PULL_UP)
        self.left = Pin(17,Pin.IN,Pin.PULL_UP) 
        self.right = Pin(2 ,Pin.IN,Pin.PULL_UP)
        self.down = Pin(15,Pin.IN,Pin.PULL_UP)

        # snake coordinates - minus 4 pixels to centre 8x8 pixel snake head
        self.coordinates = [{'x': int(self.width / 2), 'y': int(self.height / 2)}]
        self.direction = 'N'

        # game attributes
        self.fruit_left = 10
        self.fruit_eaten = False
        self.game_over = False

        # levels are defined by speed (ms)
        self.CURRENT_LEVEL = level
        if level == 1: self.SPEED = 500
        if level == 2: self.SPEED = 400
        if level == 3: self.SPEED = 300
        if level == 4: self.SPEED = 250
        if level == 5: self.SPEED = 200
    
    def setFruitLocation(self):
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
        self.LCD.show()

    def isFruitEaten(self):
        if (self.coordinates[0] == self.fruit_coordinates):
            self.fruit_left -= 1
            if self.fruit_left == 0:
                self.gameWon()
            else:
                self.setFruitLocation()
                self.drawFruit()
                self.growSnake()
            return True
        return False

    def drawSnake(self):
        for location in self.coordinates:
            self.LCD.fill_rect(location['x'] * 8, location['y'] * 8, 8, 8, self.LCD.GREEN)
            if self.coordinates.index(location) == 0:
                self.LCD.fill_rect(location['x'] * 8 + 5, location['y'] * 8 + 2, 2, 2, self.LCD.BLACK)
                self.LCD.fill_rect(location['x'] * 8 + 1, location['y'] * 8 + 2, 2, 2, self.LCD.BLACK)
        self.LCD.show()

    def clearSnake(self, location):
        self.LCD.fill_rect(location['x'] * 8, location['y'] * 8, 8, 8, self.LCD.BLACK)

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

        self.clearSnake(self.coordinates.pop(len(self.coordinates) - 1))
        self.checkOutOfBounds()

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
        self.LCD.fill(self.LCD.GREEN)
        self.LCD.text("GAME OVER", int(self.LCD.width / 4.5), int(self.LCD.height / 2), self.LCD.RED)
        self.LCD.show()

        self.game_over = True
        self.waitForKeyPress()
    
    def gameWon(self):
        self.LCD.fill(self.LCD.GREEN)
        width = self.LCD.width / 100
        height = self.LCD.height / 100
        if (self.CURRENT_LEVEL < 5):
            self.LCD.text("LEVEL", int(width * 37), int(height * 35), self.LCD.RED)
            self.LCD.text("COMPLETE!", int(width * 25), int(height * 50), self.LCD.RED)
            self.CURRENT_LEVEL += 1
        else:
            self.LCD.text("YOU WIN!", int(width * 27), int(height * 45), self.LCD.RED)
            self.CURRENT_LEVEL = 1

        self.LCD.show()
        self.game_over = True
        self.waitForKeyPress()
        
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
        self.setBorder()
        self.growSnake()
        self.setFruitLocation()
        self.drawFruit()

        while (not self.game_over):
            self.drawSnake()
            for x in range(self.SPEED):
                self.checkForDirectionChange()
                time.sleep_ms(1)
            if (not self.isFruitEaten()):
                self.moveSnake()
            
    def setBorder(self):
        for n in range(1, 8):
            self.LCD.hline(n, n, self.LCD.width, self.LCD.GBLUE)
            self.LCD.hline(n, self.LCD.height - n, self.LCD.width, self.LCD.GBLUE)
            self.LCD.vline(n, n, self.LCD.height, self.LCD.GBLUE)
            self.LCD.vline(self.LCD.width - n, n, self.LCD.height, self.LCD.GBLUE)

    def welcomeScreen(self):
        self.LCD.fill(self.LCD.BLACK)
        width = self.LCD.width / 100
        height = self.LCD.height / 100
        level_text = "LEVEL " + str(self.CURRENT_LEVEL)

        self.LCD.text("SNAKE", int(width * 37), int(height * 20), self.LCD.GREEN)
        self.LCD.text(level_text, int(width * 32), int(height * 40), self.LCD.GREEN)
        self.LCD.text("Press any key", int(width * 10), int(height * 60), self.LCD.WHITE)
        self.LCD.text("to start", int(width * 27), int(height * 70), self.LCD.WHITE)
        self.LCD.show()

        self.waitForKeyPress()
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

    level = 1
    while level <= 5:
        game = Snake(level, LCD)
        level = game.play()