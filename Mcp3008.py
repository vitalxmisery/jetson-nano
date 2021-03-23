class Mcp3008:

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

        print("Raw ADC Value: ", chan.value)
        print("ADC Voltage: " + str(chan.voltage) + "V")

        time.sleep(.05)