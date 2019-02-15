from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD

# instantiate lcd and specify pins
#def lcd_setup():
def display_lcd(data):
    lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=5, d6=6, d7=17,
                       cols=16, lines=2)
    lcd.clear()
# display text on LCD display \n = new line
#def display(data):
    lcd.message(data)
    sleep(0.5)
# scroll text off display
    for x in range(0, 16):
        lcd.move_right()
    sleep(0.1)
    # scroll text on display
    for x in range(0, 16):
        lcd.move_left()
    sleep(0.1)
    #sleep(2)
    #lcd.clear()
    
display_lcd("hello");