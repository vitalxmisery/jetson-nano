import requests

my_dict = requests.get('http://192.168.43.45:3000/uploadJetsonData?temp=100&hum=2&lat=3&lon=4&pre=69&alt=420').json()
print(my_dict)
print(my_dict['Command'])
print(my_dict['Identifier'])

#(url)?temp=(number)&hum=(number)
#pre (pressure) = (number)
#lat (latiditue) = number
#lon (longitidue) = number
#alt (altitidu)=number

#send joel data for camera, gps, temp, microphone,
#work on threading????
#thread 1 = temp seneors
#th 2 = camera
#th3 = mic
#th4 = gps

#sampling rate for heartbeat, code works but need to config adc to work properly
#