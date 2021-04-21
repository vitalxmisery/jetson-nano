import threading
import time

def temp():
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
        f.write("\nTemperature: %0.1f C" % bme280.temperature + ","
            "Humidity: %0.1f %%" % bme280.relative_humidity + ","
            "Altitude = %0.2f meters" % bme280.altitude + ","
            "Pressure: %0.1f hPa" % bme280.pressure)
        time.sleep(1)
    f.close()

def cam():
    import cv2
    print(cv2.__version__)
    dispW=640
    dispH=480
    flip=2

    camSet='nvarguscamerasrc ! video/x-raw(memory:NVMM) , width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=' + str(flip)+ ' ! video/x-raw, width='+str(dispW)+',height='+str(dispH)+',formal=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
    cam=cv2.VideoCapture(camSet)
    while True:
        ret, frame=cam.read()



        cv2.imshow('piCam',frame)
        if cv2.waitKey(1)==ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

def audio():
    import pyaudio
    import wave
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7,GPIO.IN)
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("*done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.wrtieframes(b''.join(frames))
    wf.close()

def gps():
    import time
    import board
    import busio

    import adafruit_gps

    import serial
    uart = serial.Serial("/dev/ttyTHS1", baudrate=9600, timeout=10)

    gps = adafruit_gps.GPS(uart, debug=False)

    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

    gps.send_command(b"PMTK220,1000")

    last_print = time.monotonic()

    
    fgps = open("/home/allen/Desktop/pyPro/Master /OutputData/GpsData.txt", "a")

    
    while True:
        gps.update()
        longi = (gps.longitude)
        lati = (gps.latitude)        
        fgps.write(str(lati) +","+str(longi) +"\n")
        time.sleep(1) 

    fgps.close()

''' 
    while True:
        gps.update()

        current = time.monotonic()
        if current - last_print >= 1.0:
            last_print = current
            if not gps.has_fix:

                print("Waiting for fix...")
                continue

            print("=" * 40)  # Print a separator line.
            print(
                "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                    gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                    gps.timestamp_utc.tm_mday,  # struct_time object that holds
                    gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                    gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                    gps.timestamp_utc.tm_min,  # month!
                    gps.timestamp_utc.tm_sec,
                )
            )
            print("Latitude: {0:.6f} degrees".format(gps.latitude))
            print("Longitude: {0:.6f} degrees".format(gps.longitude))
            print("Fix quality: {}".format(gps.fix_quality))

            if gps.satellites is not None:
                print("# satellites: {}".format(gps.satellites))
            if gps.altitude_m is not None:
                print("Altitude: {} meters".format(gps.altitude_m))
            if gps.speed_knots is not None:
                print("Speed: {} knots".format(gps.speed_knots))
            if gps.track_angle_deg is not None:
                print("Track angle: {} degrees".format(gps.track_angle_deg))
            if gps.horizontal_dilution is not None:
                print("Horizontal dilution: {}".format(gps.horizontal_dilution))
            if gps.height_geoid is not None:
                print("Height geo ID: {} meters".format(gps.height_geoid))
'''
def hb():
        import serial
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=10) as ser:  
            while True:
                print(ser.readline())

t1 = threading.Thread(target= temp, args=())
t2 = threading.Thread(target= cam, args=())
t3 = threading.Thread(target= gps, args=())
t4 = threading.Thread(target = audio, args=())
t5 = threading.Thread(target= hb, args=())

t1.start()


t2.start()
t3.start()
#t4.start()
t5.start()


t1.join()
t2.join()
t3.join()
#t4.join()
t5.join()





print("done")