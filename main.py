# Portions of this code are derived from code copyrighted by Dieter Vansteenwegen
# and licensed under the GNU General Public License, version 3.
# Original code: src/novastar_mctrl300/mctrl300.py (available at https://github.com/dietervansteenwegen/Novastar_MCTRL300_basic_controller/blob/feature-simplified_mctrl300/src/novastar_mctrl300/mctrl300.py).

import serial
import argparse
from datetime import datetime
from typing import Union, List

BAUDRATE = 115200
TIMEOUT = 4
PATTERN_NORMAL = 1
PATTERN_RED = 2
PATTERN_GREEN = 3
PATTERN_BLUE = 4
PATTERN_WHITE = 5
PATTERN_HORIZONTAL = 6
PATTERN_VERTICAL = 7
PATTERN_SLASH = 8
PATTERN_GRAYSCALE = 9

parser = argparse.ArgumentParser(
    prog='Novastar Control',
    description='This tool helps to configure the brightness and test Novastar devices (MCTRL300)')

parser.add_argument('--brightness', type=int, choices=range(256), metavar="[0-255]",
                    help='set to brightness (range: 0 - 255)')
parser.add_argument('--output', type=int, choices=range(256), default=1, metavar="",
                    help='output port (default=1)')
parser.add_argument('--port', default="/dev/ttyUSB0",
                    help='serial port device (default=/dev/ttyUSB0)')
parser.add_argument('--test', choices=['normal', 'red', 'green', 'blue', 'white', 'slash', 'vertical', 'horizontal', 'grayscale'],
                    help='show test pattern')
args = parser.parse_args()

class DeviceMsg:

    def __init__(self):
        self.msg = bytearray()

    def generate(
            self,
            serno: int,
            reg_addr: int,
            data_len: int,
            data: Union[int, List[int], None],
            port: int,
            is_cmd: bool = True,
            is_write: bool = True,
            ack=0,
    ) -> bytearray:
        self.msg = bytearray()
        self._append_header(is_cmd)
        self._append_ack(ack)
        self.msg.append(serno)
        self._append_src()
        self._append_dest()
        self._append_card_type()
        self._append_port_addr(port)
        self._append_board_addr(is_cmd)
        self._append_cmd_type(is_write)
        self._append_reserved()
        self._append_reg_addr(reg_addr)
        self._append_data_len(data_len)
        self._append_data(data)
        self._append_checksum()
        return self.msg

    def _append_ack(self, ack) -> None:
        self.msg.append(ack)

    def _append_checksum(self) -> None:
        c = sum(self.msg[3:])
        c += 0x5555
        self.msg.append(c & 0xFF)
        self.msg.append(c >> 8)

    def _append_data(self, data: Union[int, list, None]) -> None:
        if data and type(data) == list:
            self.msg.append(*data)
        elif data is not None:
            self.msg.append(data)

    def _append_data_len(self, data_len) -> None:
        self.msg.append(data_len & 0xFF)
        self.msg.append((data_len & 0xFF) >> 8)

    def _append_reg_addr(self, reg_addr) -> None:
        self.msg.append(reg_addr & 0xFF)
        self.msg.append((reg_addr & 0x0000FF00) >> 8)
        self.msg.append((reg_addr & 0x00FF0000) >> 16)
        self.msg.append((reg_addr & 0xFF000000) >> 24)

    def _append_header(self, is_cmd) -> None:
        header = [0x55, 0xAA] if is_cmd else [0xAA, 0x55]
        for i in header:
            self.msg.append(i)  # header

    def _append_src(self) -> None:
        self.msg.append(0xFE)

    def _append_dest(self) -> None:
        self.msg.append(0x00)

    def _append_card_type(self) -> None:
        # 00 for sender, 01 for receiver, 02 for function
        self.msg.append(0x01)

    def _append_port_addr(self, port) -> None:
        self.msg.append(port - 1)

    def _append_board_addr(self, is_cmd: bool) -> None:
        for i in ([0xFF, 0xFF] if is_cmd else [0x0, 0x0]):
            self.msg.append(i)

    def _append_cmd_type(self, is_write) -> None:
        self.msg.append(0x01 if is_write else 0x00)

    def _append_reserved(self) -> None:
        self.msg.append(0x00)


class Device:

    message = DeviceMsg()

    REG_TEST_PATTERN = 0x02000101
    REG_BRIGHTNESS_OVERALL = 0x02000001

    def __init__(self, serport: serial.Serial, port: int):
        self.serport = serport
        self.port = port
        self.msg_no = 0

    def send_msg(self, msg) -> None:
        self.serport.write(msg)

    def show_pattern(self, pattern: int):
        self.serport.write(self.message.generate(
            serno=self.msg_no,
            port=self.port,
            reg_addr=self.REG_TEST_PATTERN,
            data_len=1,
            data=pattern,
        ))

    def set_brightness(self, value: int):
        self.serport.write(self.message.generate(
            serno=self.msg_no,
            port=self.port,
            reg_addr=self.REG_BRIGHTNESS_OVERALL,
            data_len=1,
            data=value
        ))

def main():
    ser = serial.Serial(args.port,
                    baudrate=BAUDRATE,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=TIMEOUT)

    led_screen = Device(ser, args.output)

    if args.brightness is not None:
        log("Set brightness to " + str(args.brightness))
        led_screen.set_brightness(args.brightness)

    if args.test is not None:

        if args.test == 'normal':
            log("Hide test pattern")
        else:
            log("Show test pattern " + args.test)

        if args.test == 'normal':
            led_screen.show_pattern(PATTERN_NORMAL)
        elif args.test == 'red':
            led_screen.show_pattern(PATTERN_RED)
        elif args.test == 'green':
            led_screen.show_pattern(PATTERN_GREEN)
        elif args.test == 'blue':
            led_screen.show_pattern(PATTERN_BLUE)
        elif args.test == 'white':
            led_screen.show_pattern(PATTERN_WHITE)
        elif args.test == 'slash':
            led_screen.show_pattern(PATTERN_SLASH)
        elif args.test == 'vertical':
            led_screen.show_pattern(PATTERN_VERTICAL)
        elif args.test == 'horizontal':
            led_screen.show_pattern(PATTERN_HORIZONTAL)
        elif args.test == 'grayscale':
            led_screen.show_pattern(PATTERN_GRAYSCALE)

def log(message):
    print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ': ' + message)

if __name__ == '__main__':
    main()
