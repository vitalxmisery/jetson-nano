class Temp:

    import time

    import board
    import busio
    import adafruit_bme280

    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

    bme280.sea_level_pressure = 1013.25

    while True:
        choice = input('Enter a command ')
        if choice == 'temperature':
                while True:
                    print("\nTemperature: %0.1f C" % bme280.temperature)
                    time.sleep(1)
                    ext = input('To leave ')
                    if ext == 'q':
                        break
                    
        elif choice =='humitidty': 
            try:
                while True:          
                    print("\nHumidity: %0.1f %%" % bme280.relative_humidity)
                    time.sleep(2)
            except KeyboardInterrupt:
                print('Enter a command') 

        elif choice =='pressure':
            try: 
                while True:       
                    print("\nPressure: %0.1f hPa" % bme280.pressure)
                    time.sleep(2)
            except KeyboardInterrupt:
                print('Enter a command')

        elif choice =='altitude':        
            try:
                while True:
                    print("\nAltitude = %0.2f meters" % bme280.altitude)
                    time.sleep(2)
            except KeyboardInterrupt:
                print('Enter a command')