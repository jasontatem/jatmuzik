import spidev
import logging


spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000


def build_command(target=0x1, value=0x80):
    # command needs to be 4 bits of target, 8 bits of value, 4 bits of whatever
    byte_1 = target << 4  # shift target left 4 bits to make them highest 4 bits of byte_1
    byte_1 += value >> 4  # move first 4 bits of value to last 4 bits of byte 1

    byte_2 = (1 << 4) - 1 & value  # zero out the first 4 bits, keeping the last 4 bits
    byte_2 = byte_2 << 4  # shift byte_2 keeping the last 4 bits and adding 4 trailing 0s

    return [byte_1, byte_2]


def send_command(target=1, value=128):
    command = build_command(target, value)
    logging.debug(f'DAC::Sending command for target {target} value {value}')
    spi.writebytes(command)


def cleanup():
    send_command(15, 0)
    spi.close()
    logging.debug(f'DAC::Cleanup finished')
