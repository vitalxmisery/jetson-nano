import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')


import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time

while True:
    spi = busio.SPI(clock=board.SCK_1, MISO=board.MISO_1, MOSI=board.MOSI_1)

    cs = digitalio.DigitalInOut(board.D5)

    mcp = MCP.MCP3008(spi, cs)

    chan = AnalogIn(mcp, MCP.P0)

x_values = []
y_values = []

index = count()
def animate(i):
    x_values.append(next(index))
    y_values.append(print(str(chan.voltage)))
    plt.cla()
    plt.plot(x_values, y_values)


ani = FuncAnimation(plt.gcf(), animate, 1000)


plt.tight_layout()
plt.show()