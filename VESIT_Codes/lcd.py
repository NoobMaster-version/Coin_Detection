import smbus
import time

# I2C address of the LCD (use `i2cdetect -y 1` to find it, typically 0x27)
LCD_I2C_ADDR = 0x27

# Define commands
LCD_BACKLIGHT = 0x08  # Backlight on
ENABLE = 0b00000100   # Enable bit

# LCD Initialization
def lcd_write(value, mode):
    """Send byte to data pins, mode = 1 for data, 0 for command."""
    bus.write_byte(LCD_I2C_ADDR, value | LCD_BACKLIGHT | mode)
    time.sleep(0.0005)
    lcd_toggle_enable(value | LCD_BACKLIGHT | mode)

def lcd_toggle_enable(value):
    """Toggle the enable pin to send command."""
    time.sleep(0.0005)
    bus.write_byte(LCD_I2C_ADDR, value | ENABLE)
    time.sleep(0.0005)
    bus.write_byte(LCD_I2C_ADDR, value & ~ENABLE)
    time.sleep(0.0005)

def lcd_send_command(cmd):
    """Send command to the LCD."""
    lcd_write(cmd & 0xF0, 0)
    lcd_write((cmd << 4) & 0xF0, 0)

def lcd_send_data(data):
    """Send data (character) to the LCD."""
    lcd_write(data & 0xF0, 1)
    lcd_write((data << 4) & 0xF0, 1)

def lcd_init():
    """Initialize LCD display."""
    lcd_send_command(0x33)  # Initialize
    lcd_send_command(0x32)  # Set to 4-bit mode
    lcd_send_command(0x28)  # 2-line, 5x8 dots
    lcd_send_command(0x0C)  # Display ON, Cursor OFF
    lcd_send_command(0x06)  # Entry mode
    lcd_send_command(0x01)  # Clear display
    time.sleep(0.005)

def lcd_clear():
    """Clear LCD screen."""
    lcd_send_command(0x01)
    time.sleep(0.005)

def lcd_set_cursor(line, position):
    """Set cursor position."""
    offsets = [0x80, 0xC0, 0x94, 0xD4]
    lcd_send_command(offsets[line] + position)

def lcd_print(text):
    """Display text on LCD."""
    for char in text:
        lcd_send_data(ord(char))

# Initialize I2C bus
bus = smbus.SMBus(1)

# Initialize LCD
lcd_init()

# Example Usage
lcd_clear()
lcd_set_cursor(0, 0)  # Line 1, Position 0
lcd_print("Number Of 2 Rupee Coins")

lcd_set_cursor(1, 0)  # Line 2
lcd_print("Number: " + str(20))

lcd_set_cursor(2, 0)  # Line 3
lcd_print("I2C 20x4 LCD")

lcd_set_cursor(3, 0)  # Line 4
lcd_print("Enjoy Coding!")

