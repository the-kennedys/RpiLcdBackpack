from RpiLcdBackpack import AdafruitLcd
from time import sleep

if __name__ == '__main__':
  lcd = AdafruitLcd()
  lcd.backlight(True)
  lcd.blink(False)
  lcd.cursor(False)
  lcd.clear()
  lcd.message("RpiLcd\nHello World!")
  sleep(2)
  lcd.backlight(False)

