#    Copyright Paul Knox-Kennedy, 2012
#    This file is part of RpiLcdBackpack.

#    RpiLcdBackpack is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RpiLcdBackpack is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.#

import smbus,time



class AdafruitLcd:
  # commands
  LCD_CLEARDISPLAY=0x01
  LCD_RETURNHOME=0x02
  LCD_ENTRYMODESET=0x04
  LCD_DISPLAYCONTROL=0x08
  LCD_CURSORSHIFT=0x10
  LCD_FUNCTIONSET=0x20
  LCD_SETCGRAMADDR=0x40
  LCD_SETDDRAMADDR=0x80

  # flags for display entry mode
  LCD_ENTRYRIGHT=0x00
  LCD_ENTRYLEFT=0x02
  LCD_ENTRYSHIFTINCREMENT=0x01
  LCD_ENTRYSHIFTDECREMENT=0x00

  # flags for display on/off control
  LCD_DISPLAYON=0x04
  LCD_DISPLAYOFF=0x00
  LCD_CURSORON=0x02
  LCD_CURSOROFF=0x00
  LCD_BLINKON=0x01
  LCD_BLINKOFF=0x00

  # flags for display/cursor shift
  LCD_DISPLAYMOVE=0x08
  LCD_CURSORMOVE=0x00
  LCD_MOVERIGHT=0x04
  LCD_MOVELEFT=0x00

  # flags for function set
  LCD_8BITMODE=0x10
  LCD_4BITMODE=0x00
  LCD_2LINE=0x08
  LCD_1LINE=0x00
  LCD_5x10DOTS=0x04
  LCD_5x8DOTS=0x00


  _rs=0x02
  _e=0x4
  _dataMask=0x78
  _dataShift=3
  _light=0x80



  def writeFourBits(self,value):
    self.__data &= ~self._dataMask
    self.__data |= value << self._dataShift
    self.__data &= ~self._e 
    self.__bus.write_byte_data(0x20,0x09,self.__data)
    time.sleep(0.000001)
    self.__data |= self._e 
    self.__bus.write_byte_data(0x20,0x09,self.__data)
    time.sleep(0.000001)
    self.__data &= ~self._e 
    self.__bus.write_byte_data(0x20,0x09,self.__data)
    time.sleep(0.000101)

  def writeCommand(self,value):
    self.__data &= ~self._rs
    self.writeFourBits(value>>4)
    self.writeFourBits(value&0xf)

  def writeData(self,value):
    self.__data |= self._rs
    self.writeFourBits(value>>4)
    self.writeFourBits(value&0xf)

  def __init__(self):
    self.__bus=smbus.SMBus(0)
    self.__bus.write_byte_data(0x20,0x00,0x00)
    self.__data=0x80
    self.__displayfunction = self.LCD_4BITMODE | self.LCD_2LINE | self.LCD_5x8DOTS

    self.writeFourBits(0x03)
    time.sleep(0.005)
    self.writeFourBits(0x03)
    time.sleep(0.00015)
    self.writeFourBits(0x03)
    self.writeFourBits(0x02)
    self.writeCommand(self.LCD_FUNCTIONSET | self.__displayfunction)
    self.writeCommand(self.LCD_DISPLAYCONTROL | self.LCD_DISPLAYON | self.LCD_CURSORON | self.LCD_BLINKON)
    self.writeCommand(0x6)
    self.writeCommand(self.LCD_CLEARDISPLAY)
    time.sleep(0.002)


if __name__ == '__main__':
  lcd = AdafruitLcd()
  lcd.writeData(0x48)
  lcd.writeData(0x65)
  lcd.writeData(0x6C)
  lcd.writeData(0x6C)
  lcd.writeData(0x6F)
  lcd.writeData(0x20)
  lcd.writeData(0x52)
  lcd.writeData(0x6F)
