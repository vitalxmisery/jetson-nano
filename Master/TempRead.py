class TempRead:

    import time
 
    import board
    import busio
    import adafruit_bme280

    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

    bme280.sea_level_pressure = 1013.25
    bme280.mode = adafruit_bme280.MODE_NORMAL
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
    bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    time.sleep(1)

    f = open("/home/allen/Desktop/pyPro/Master /OutputData/TempData.txt", "a")
    while True:
        f.write("\n%0.1f" % bme280.temperature + ","
            "%0.1f %%" % bme280.relative_humidity + ","
            "%0.2f" % bme280.altitude + ","
            "%0.1f" % bme280.pressure)
        time.sleep(1)
    f.close()
## make an if not statement for when it disconnects
'''
    while True:
        print("\nTemperature: %0.1f C" % bme280.temperature)
        print("Humidity: %0.1f %%" % bme280.relative_humidity)
        print("Altitude = %0.2f meters" % bme280.altitude)
        print("Pressure: %0.1f hPa" % bme280.pressure)
        time.sleep(1)

    Fahrenheit = ((bme280.temperature * (9/5)) + 32)
    while True:
    
        print("\nTemperature: %0.1f" % Fahrenheit)
'''