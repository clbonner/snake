from machine import Pin,PWM
from picolcd144 import *
import time

class Snake():
    def __init__(self):
        pwm = PWM(Pin(BL))
        pwm.freq(1000)
        pwm.duty_u16(32000)#max 65535

        self.LCD = LCD_1inch44()
        self.LCD.fill(self.LCD.BLACK)
        self.LCD.show()

        self.left = Pin(15,Pin.IN,Pin.PULL_UP) 
        self.down = Pin(17,Pin.IN,Pin.PULL_UP)
        self.up = Pin(2 ,Pin.IN,Pin.PULL_UP)
        self.right = Pin(3 ,Pin.IN,Pin.PULL_UP)

        # snake attributes
        # direction can be N, E, S, W
        self.posX = int(self.LCD.width / 2)
        self.posY = int(self.LCD.height / 2)
        self.size = 1
        self.direction = 'E'

        # games attributes
        self.level = 1
        self.MAX_LEVEL = 5
        self.fruit = 5
        self.gameOver = False

        self.welcomeScreen()

    def drawSnake(self):
        self.LCD.fill_rect(self.posX, self.posY, 10, 10, self.LCD.GREEN)

    def clearSnake(self):
        self.LCD.fill_rect(self.posX, self.posY, 10, 10, self.LCD.BLACK)

    def moveSnake(self):
        if (self.direction == 'N'):
            self.posY -= 5
        if (self.direction == 'E'):
            self.posX += 5
        if (self.direction == 'S'):
            self.posY += 5
        if (self.direction == 'W'):
            self.posX -= 5

    def checkForKeypress(self):
        if (self.up.value() == 0):
            self.direction = 'N'
        if (self.down.value() == 0):
            self.direction = 'S'
        if (self.left.value() == 0):
            self.direction = 'W'
        if (self.right.value() == 0):
            self.direction = 'E'

    def start(self):
        self.LCD.fill(self.LCD.BLACK)
        self.setBorder()
        self.drawSnake()
        self.LCD.show()

        while(not self.gameOver):
            self.checkForKeypress()
            self.clearSnake()
            self.moveSnake()
            self.drawSnake()
            self.LCD.show()
            time.sleep_ms(250)
            
    def setBorder(self):
        self.LCD.hline(0,0,128,self.LCD.GBLUE)
        self.LCD.hline(0,127,128,self.LCD.GBLUE)
        self.LCD.vline(0,0,128,self.LCD.GBLUE)
        self.LCD.vline(127,0,128,self.LCD.GBLUE)

    def welcomeScreen(self):
        self.setBorder()
        self.LCD.text("SNAKE", 45, 25, self.LCD.GREEN)
        self.LCD.text("Press any key", 10, 50, self.LCD.BLUE)
        self.LCD.text("to start...", 20, 70, self.LCD.BLUE)

        self.LCD.show()

        while (True):
            if (self.left.value() == 0 or
                self.right.value() == 0 or
                self.up.value() == 0 or
                self.down.value() == 0):
                    self.start()



if __name__=='__main__':
    game = Snake()