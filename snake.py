from machine import Pin,PWM
from picolcd144 import *
import time

class Snake():
    def __init__(self, level):
        # init display
        pwm = PWM(Pin(BL))
        pwm.freq(1000)
        pwm.duty_u16(32000)#max 65535
        self.LCD = LCD_1inch44()
        self.LCD.fill(self.LCD.BLACK)
        self.LCD.show()

        self.height = self.getMaxDisplayLength(self.LCD.height)
        self.width = self.getMaxDisplayLength(self.LCD.width)

        # key0 = down / key1 = left / key2 = right / key3 = up
        self.up = Pin(3 ,Pin.IN,Pin.PULL_UP)
        self.left = Pin(17,Pin.IN,Pin.PULL_UP) 
        self.right = Pin(2 ,Pin.IN,Pin.PULL_UP)
        self.down = Pin(15,Pin.IN,Pin.PULL_UP)

        # snake coordinates
        self.coordinates = [{'x': int(self.LCD.width / 2) - 4, 'y': int(self.LCD.height / 2) - 4}]
        self.direction = 'N'

        # game attributes
        self.MAX_LEVEL = 5
        self.fruit = 5
        self.game_over = False
        self.border_height = self.height - 1
        self.border_width = self.width - 1

        # levels are defined by speed (ms)
        self.CURRENT_LEVEL = level
        if level == 1: self.SPEED = 250
        if level == 2: self.SPEED = 200
        if level == 3: self.SPEED = 150
        if level == 4: self.SPEED = 100
        if level == 5: self.SPEED = 50

    def getMaxDisplayLength(self, n):
        count = 1
        length = 8
        while (length < n):
            count += 1
            length += 8
        return count * 8

    def drawSnake(self):
        for block in self.coordinates:
            self.LCD.fill_rect(block['x'], block['y'], 8, 8, self.LCD.GREEN)
            if self.coordinates.index(block) == 0:
                self.LCD.fill_rect(block['x'] + 5, block['y'] + 2, 2, 2, self.LCD.BLACK)
                self.LCD.fill_rect(block['x'] + 1, block['y'] + 2, 2, 2, self.LCD.BLACK)

    def clearSnake(self, block):
        self.LCD.fill_rect(block['x'], block['y'], 8, 8, self.LCD.BLACK)

    def moveSnake(self):
        head = self.coordinates[0]
        if (self.direction == 'N'):
            self.coordinates.insert(0, {'x': head['x'], 'y': head['y'] - 8})
        if (self.direction == 'E'):
            self.coordinates.insert(0, {'x': head['x'] + 8, 'y': head['y']})
        if (self.direction == 'S'):
            self.coordinates.insert(0, {'x': head['x'], 'y': head['y'] + 8})
        if (self.direction == 'W'):
            self.coordinates.insert(0, {'x': head['x'] - 8, 'y': head['y']})

        self.clearSnake(self.coordinates.pop(len(self.coordinates) - 1))
        self.checkOutOfBounds()
        self.checkHeadIntoTail()

    def growSnake(self):
        head = self.coordinates[0]
        if (self.direction == 'N'):
            self.coordinates.insert(0, {'x': head['x'], 'y': head['y'] - 8})
        if (self.direction == 'E'):
            self.coordinates.insert(0, {'x': head['x'] + 8, 'y': head['y']})
        if (self.direction == 'S'):
            self.coordinates.insert(0, {'x': head['x'], 'y': head['y'] + 8})
        if (self.direction == 'W'):
            self.coordinates.insert(0, {'x': head['x'] - 8, 'y': head['y']})


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
        if (self.coordinates[0]['y'] <  1 or
            self.coordinates[0]['x'] > self.border_width or
            self.coordinates[0]['y'] > self.border_height or
            self.coordinates[0]['x'] < 1):
                self.gameOver()

    def checkHeadIntoTail(self):
        head = self.coordinates[0]
        for block in self.coordinates:
            if (block['x'] == head['x'] and
                block['y'] == head['y'] and
                self.coordinates.index(block) != 0):
                    self.gameOver()

    def gameOver(self):
        self.LCD.fill(self.LCD.GREEN)
        self.LCD.text("GAME OVER", int(self.LCD.width / 4.5), int(self.LCD.height / 2), self.LCD.RED)
        self.LCD.show()

        # reset snake position
        self.coordinates = [{'x': int(self.LCD.width / 2), 'y': int(self.LCD.height / 2)}]
        self.direction = 'N'

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

        while (not self.game_over):
            self.drawSnake()
            self.LCD.show()
            for x in range(self.SPEED):
                self.checkForDirectionChange()
                time.sleep_ms(1)
            self.moveSnake()
            
    def setBorder(self):
        self.LCD.hline(0, 0, self.border_width, self.LCD.GBLUE)
        self.LCD.hline(0, self.border_height, self.border_width, self.LCD.GBLUE)
        self.LCD.vline(0, 0, self.border_height, self.LCD.GBLUE)
        self.LCD.vline(self.border_width, 0, self.border_height, self.LCD.GBLUE)

    def welcomeScreen(self):
        self.LCD.fill(self.LCD.BLACK)
        self.setBorder()
        self.LCD.text("SNAKE", 45, 25, self.LCD.GREEN)
        self.LCD.text("Press any key", 10, 50, self.LCD.WHITE)
        self.LCD.text("to start...", 20, 70, self.LCD.WHITE)
        self.LCD.show()

        self.waitForKeyPress()
        self.startGame()
    
    def play(self):
        self.welcomeScreen()
        return self.CURRENT_LEVEL

if __name__=='__main__':
    level = 1
    while level <= 5:
        game = Snake(level)
        level = game.play()