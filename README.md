# Snake Game for Raspberry Pi Pico 

A fun project to code a snake like game on the Raspberry Pi Pico with WaveShare's 1.44" display. The four buttons on the display are used to move the snake around the screen. With each level the speed of the snake increases. 

I have tried to make the code fairly portable to displays of other sizes. For example, when positioning text or shapes on the screen they are relative to the percentage width/height of the display. Likewise, the play area for the snake is divied into an 8x8 pixel grid and the snake and fruit are positioned on the grid.

Requires:\
[Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico-2)\
[MicroPython](https://micropython.org/)\
[WaveShare Pico LCD 1.44 Display](https://www.waveshare.com/wiki/Pico-LCD-1.44)

![Welcome Screen](https://github.com/clbonner/snake/blob/main/WelcomeScreen.jpg)

![Snake game in action](https://github.com/clbonner/snake/blob/main/SnakeGame.jpg)

![Game Over screen](https://github.com/clbonner/snake/blob/main/GameOver.jpg)
