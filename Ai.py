import pyaudio
import wave
import numpy as np
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt  
import librosa
import librosa.display
import os
import time
import board
import busio
import adafruit_bme280
import adafruit_gps
import serial
import threading 

import tensorflow as tf
import tensorflow.keras as keras


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# will load the model and return it. One time setup only
# The directory must point to the variables AND the model file like so
# Saved Model Data\\MarkusModel\\
def audio():


    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 1.5

    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    output = True,
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
    wf.writeframes(b''.join(frames))
    wf.close()

def load(modelPath):
    global model
    #filePath = "/home/allen/Desktop/pyPro/Master/Saved_Model_Data//MarkusModel"
    model = keras.models.load_model(modelPath)
    return model


##
# Will predict the outcome of a target image in the directory.
# directory must be like: C:\\Markus\\melSpecFiles\\ZOOM0011204.png
##
def predictOutcome(model, imageDirectory):
    # filePath = "Saved Model Data\\MarkusModel\\"
    # model = keras.models.load_model(filePath)
    # model = load("Saved Model Data\\MarkusModel\\")
    img = keras.preprocessing.image.load_img(
        imageDirectory, target_size=(64, 48)
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    print(score)
    return score

#model = load("/home/allen/Desktop/pyPro/Master/Saved_Model_Data/MarkusModel")



def makeMelSpec(ai, filename):
    test = "/" + filename + ".png"
    my_file = Path(test)
    if my_file.is_file():
        os.remove(test)
    y, sr = librosa.load("/" + filename + ".wav")
    print("C:\\Markus\\audioFiles" + filename + ".wav______________")
    # trim silent edges
    whale_song, _ = librosa.effects.trim(y)
    n_fft = 2048
    hop_length = 100
    D = np.abs(librosa.stft(whale_song, n_fft=n_fft, hop_length=hop_length + 1))
    DB = librosa.amplitude_to_db(D, ref=np.max)
    librosa.display.specshow(DB, sr=sr, hop_length=hop_length)
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    # plt.show()
    plt.savefig(test, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(filename)
    variable = predictOutcome(ai, "/home/allen/Desktop/pyPro/output.png")
  #audio data location goes here      

#makeMelSpec("/home/allen/Desktop/pyPro/output") 


#while true
#record audio data 1.5 sec
#save recording
#make melspec (audio file location, png file)
#v /outputdata/ png file location

#print(variable)

def setup():
    model = load("/home/allen/Desktop/pyPro/Master/Saved_Model_Data/MarkusModel")
    return model
def startAi(ai):
    audio()
    start= time.time()
    makeMelSpec(ai,"/home/allen/Desktop/pyPro/output") 
    stop = time.time()    
    print(str(start - stop)+" seconds")

def model():
    model = setup()
    while True:
        #start thread
        startAi(model)



def temp():
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

    while True:
        print("\nTemperature: %0.1f C" % bme280.temperature)
        print("Humidity: %0.1f %%" % bme280.relative_humidity)
        print("Altitude = %0.2f meters" % bme280.altitude)
        print("Pressure: %0.1f hPa" % bme280.pressure)
        time.sleep(1)


def gps():

    uart = serial.Serial("/dev/ttyTHS1", baudrate=9600, timeout=10)

    gps = adafruit_gps.GPS(uart, debug=False)

    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

    gps.send_command(b"PMTK220,1000")

    last_print = time.monotonic()
    count = 1

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

#global data for sensors ie temp= t gps = g, ...
#t4 for jetsondata for sending off
#every x secs... 10 secs


t1 = threading.Thread(target= model, args=())
t2 = threading.Thread(target= temp, args=())
t3 = threading.Thread(target= gps, args=())


t1.start()
t2.start()
t3.start()

t2 = time.sleep(10)
t3 = time.sleep(10)

t1.join()
t2.join()
t3.join()
