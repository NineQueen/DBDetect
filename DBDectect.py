import time
import Adafruit_ADS1x15
import math
from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
LIGHT = [18,23,24,25,8]
lcd = CharLCD("PCF8574",0x27)
BUTTON = 20
adc = Adafruit_ADS1x15.ADS1115()
ADC_value_Base = 20
peak_value = -80
PIN_NUMBER = 2
level_test = 0
level = 0
grade =(
    0x1F,
    0x1F,
    0x1F,
    0x1F,
    0x1F,
    0x1F,
    0x1F,
    0x1F
)
def button_press_callback(channel):
    global peak_value
    peak_value = -80
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LIGHT,GPIO.OUT)
    GPIO.setup(BUTTON,GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON,GPIO.FALLING,callback = button_press_callback,bouncetime = 200)
    lcd.create_char(0,grade)
    while True:
        lcd.clear()
        ADC_value_measured = max(adc.read_adc(PIN_NUMBER),1)
        value_in_DB = int(20*math.log(ADC_value_measured/ADC_value_Base))
        peak_value = max(peak_value,value_in_DB)
        value_string = "CUR:{}".format(value_in_DB)
        lcd.cursor_pos = (0,0)
        lcd.write_string(value_string)
        peak_string = "PEAK:{}".format(peak_value)
        lcd.cursor_pos = (0,8)
        lcd.write_string(peak_string)
        level_test = value_in_DB
        if level_test >=0:
            level = 5
            lcd.cursor_pos = (1,0)
            lcd.write_string("Level:"+"\x00"*5)
        elif -5 <= level_test < 0:
            level = 4
            lcd.cursor_pos = (1,0)
            lcd.write_string("Level:"+"\x00"*4)
        elif -10 <= level_test < -5:
            level = 3
            lcd.cursor_pos = (1,0)
            lcd.write_string("Level:"+"\x00"*3)
        elif -15 <= level_test < -10:
            level = 2
            lcd.cursor_pos = (1,0)
            lcd.write_string("Level:"+"\x00"*2)
        elif -20 <= level_test <-15:
            level = 1
            lcd.cursor_pos = (1,0)
            lcd.write_string("Level:"+"\x00")
        else:
            level = 0
            lcd.cursor_pos = (1,0)
            lcd.write_string("Level:")
        time.sleep(0.5)
except Exception as e:
    print(e)