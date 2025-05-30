# MicroPython SSD1306 OLED driver, I2C and SPI interfaces

from micropython import const
import framebuf

# register definitions
SET_CONTRAST        = const(0x81)
ENTIRE_DISPLAY_ON   = const(0xA4)
NORMAL_DISPLAY      = const(0xA6)
DISPLAY_OFF         = const(0xAE)
DISPLAY_ON          = const(0xAF)
SET_DISPLAY_OFFSET  = const(0xD3)
SET_COM_PINS        = const(0xDA)
SET_VCOM_DETECT     = const(0xDB)
SET_DISPLAY_CLOCK_DIV = const(0xD5)
SET_PRECHARGE       = const(0xD9)
SET_MULTIPLEX       = const(0xA8)
SET_LOW_COLUMN      = const(0x00)
SET_HIGH_COLUMN     = const(0x10)
SET_START_LINE      = const(0x40)
MEMORY_MODE         = const(0x20)
SEG_REMAP           = const(0xA1)
COM_SCAN_DEC        = const(0xC8)
CHARGE_PUMP         = const(0x8D)
EXTERNAL_VCC        = const(0x1)
SWITCH_CAP_VCC      = const(0x2)

# a few patches to support both 128x64 and 128x32 displays
class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.poweron()
        self.init_display()

    def init_display(self):
        for cmd in (
            DISPLAY_OFF,
            SET_DISPLAY_CLOCK_DIV, 0x80,
            SET_MULTIPLEX, self.height - 1,
            SET_DISPLAY_OFFSET, 0x00,
            SET_START_LINE | 0x00,
            CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            MEMORY_MODE, 0x00,
            SEG_REMAP | 0x01,
            COM_SCAN_DEC,
            SET_COM_PINS, 0x02 if self.height == 32 else 0x12,
            SET_CONTRAST, 0x8F,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DETECT, 0x40,
            ENTIRE_DISPLAY_ON,
            NORMAL_DISPLAY,
            DISPLAY_ON,
        ):
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(DISPLAY_OFF)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(0xA7 if invert else 0xA6)

    def show(self):
        for page in range(self.pages):
            self.write_cmd(0xB0 | page)
            self.write_cmd(SET_LOW_COLUMN | 0x0)
            self.write_cmd(SET_HIGH_COLUMN | 0x0)
            self.write_data(self.buffer[page * self.width:(page + 1) * self.width])

    def fill(self, col):
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)

    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)

    def hline(self, x, y, w, col):
        self.framebuf.hline(x, y, w, col)

    def vline(self, x, y, h, col):
        self.framebuf.vline(x, y, h, col)

    def line(self, x1, y1, x2, y2, col):
        self.framebuf.line(x1, y1, x2, y2, col)

    def rect(self, x, y, w, h, col):
        self.framebuf.rect(x, y, w, h, col)

    def fill_rect(self, x, y, w, h, col):
        self.framebuf.fill_rect(x, y, w, h, col)

class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.i2c.writeto(self.addr, b'@' + buf)
