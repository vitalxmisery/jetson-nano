import datetime as dt
import matplotlib.pyplot as plt 
import matplotlib.animation as animation


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
xs = []
ys = []

def Mcp3008():
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

def animate (i,xs,ys):
    
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
    
    volt = print("Raw ADC Value: ", chan.value)

    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append(volt)



    ax.clear()
    ax.plot(xs,ys)

    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('BPM test')
    plt.ylabel('Voltage')

ani = animation.FuncAnimation(fig, animate, fargs=(xs,ys), interval = 100)
plt.show()