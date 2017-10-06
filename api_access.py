import socket
import network
import urequests

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Columbia University', '')              #typing the wifi and password there
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def get_location():     #the return value of this function is float type, some type casting is needed in next usage
    googleurl = r'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAUlck47UwLhNZDEZfaPnHg0w3Oo2zg_gs'
    f = open('googlemap.json')    #googlemap.json is a file we have put to the board before
    requestdata = f.read()   
    f.close()
    response = urequests.post(googleurl,data = requestdata)
    loc_josn = response.json()
    loc_josn = loc_josn['location']
    return [loc_josn['lat'],loc_josn['lng']]

def get_weather(location):
    weatherurl = "http://api.openweathermap.org/data/2.5/weather?lat={0:d}&lon={1:d}&APPID=c9854c1788404511ef45ac54c8a21def".format(location[0],location[1])
    response = urequests.post(weatherurl)
    response_str = response.json()
    weather_str = response_str['weather']
    weather_str = weather_str[0]
    return weather_str['main']

def send_twitter(tweet):
    """ thingspeak API is used there"""
    twitterurl = "https://api.thingspeak.com/apps/thingtweet/1/statuses/update"
    twitterkey =  "key=QIC7VZVRGLELTU71&status="
    data_to_send = twitterkey+tweet  #combine api key and status togather to send
    response = urequests.post(twitterurl,data = data_to_send)

#connect to wifi
do_connect()

location = get_location()
#the return value of this function is float type, some type casting is needed in next usage
location_int = [int(var) for var in location]
print(get_weather(location_int))
send_twitter("to many fucking dues~")
