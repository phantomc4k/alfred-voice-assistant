import os
import searchlite
import RPi.GPIO as GPIO
import time
import requests
import speech_recognition as sr
from datetime import date
import datetime
import random
import sys
import Adafruit_DHT



GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
r = sr.Recognizer()

x=False
more=True
cityLoc = {'inside': 'n/a','here':'n/a', 'city': ["lat", "long"]}
key = "key"
url = "https://api.climacell.co/v3/weather/realtime"
keywords = ["open", "pc", "computer", "login", ]
errorMessage = ['sorry sir, i didnt get that', 'could you please repeat that, sir?', 'what was that sir?']
searchwords = ['what', 'who', "how", "where", "when", "why", 'search', 'look',"when's","where's","what's","whos's"]
urls = {'now': "https://api.climacell.co/v3/weather/realtime",
        'minutes': "https://api.climacell.co/v3/weather/nowcast",
        'hours': "https://api.climacell.co/v3/weather/forecast/hourly",
        'days': "https://api.climacell.co/v3/weather/forecast/daily",
        'day': {'n/a': 'days'},
        'hour': {'n/a': 'hours'},
        'minute': {'n/a': 'minutes'}}
uni = {'humidity': ' percent ', 'temperature': " degrees "}
dayinfo = {'monday': 1, 'tuseday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7}
comstr = ""
word = ""
result = ""
timerTime = []
check = False
timerVal = []
alarms = []
timecheck=0
city = ""
greet = ['here i am', 'what can i do for you?', 'yes sir?', 'at your service']
hourWords = ['oclock', 'at']
gpiodict = {"light": {'desk': 33, 'workshop': 13}, "dht-11": 7, 'computer': 40, 'pc': 40}
weatherPhrase = {"temp": ["the temperature ", " degrees in ", " right now"],
                 "humidity": ["the humidity percentage ", "in", "right now"],
                 "wind_speed": ["the wind speed ", " miles per hour in ", " right now"],
                 "precipitation": ["there is a ", "precent chance precipitation of in ", " right now"],
                 "rain": {"n/a": "precipitation"},
                 "rainy": {"n/a": "precipitation"},
                 "wind": {"n/a": "wind_speed"},
                 "windy": {"n/a": "wind_speed"},
                 "raining": {"n/a": "precipitation"},
                 'temperature': {"n/a": "temp"},
                 'weather': "afsdgnjoikp"}



    

def say(a):
    os.system('flite -voice awb -t "' + str(a) + '"')
    time.sleep(.15)

def read(a): # add DHT-11
    print('here')
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    num=8
    if humidity is not None and temperature is not None:
        c="{0:0.1f} {1:0.1f}".format(temperature, humidity)
        h=c.split()
        if (a=='temp' or a=='temperature'):
            num=(float(h[0])*1.8+32)
            time.sleep(.1)
        elif (a=='humidity'):
            num=h[1]
            time.sleep(.1)
        return str(num)
    else:
        say("Sensor failure. Check wiring.")

def listen():
    said = "HKg6dN3"

    with sr.Microphone (device_index = 0) as source:
        r.adjust_for_ambient_noise(source)
        print ("Say something!")
        audio = r.listen(source)
        r.adjust_for_ambient_noise(source)

    try:
        said = r.recognize_google(audio)
        # print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print ("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print ("Could not request results from Google Speech Recognition service; {0}".format(e))

    return str(said.lower())

def gpioset(item, state, sec):
    global gpiodict
    if (sec != "n/a"):
        pin = gpiodict[item][sec]
        item = sec + ' ' + item
    else:
        pin = gpiodict[item]
    if state == True:
        say('turning on the ' + item)
    else:
        say('turning off the ' + item)
    GPIO.output(pin, state)

def addsir(str):
    x=random.randint(0,1)
    if(x==1):
        return str+', sir'
    else:
        return str

def randphrase(list,sir):
    if(sir==True):
        x = random.randint(0, len(list) - 1)
        say(addsir(list[x]))
    else:
        x = random.randint(0, len(list) - 1)
        say(list[x])

def personality(word):
    global comand
    global more
    global x
    hi=False
    counter=0
    count = 0
    disphr=[['nevermind'],['ignore','that'],["don't",'worry','about','that'],['disregard','that']]
    greetings = ['hello', 'greetings']
    goodwords=['morning','afternoon','night','day']
    goodpt2=['goodnight','goodmorring','goodday']
    counterhru=["what about you","how are you",'how has your day been']
    thankrsp=["you're welcome","of course"]
    poswords=['good', 'great','fantastic','amazing','fabulous','best','greatest']
    negwords=['not','bad','sad','terrible','awful','mad','frustrated','angry']
    posrsp=['very good to here that','thats very good',"i'm glad to here that",'wonderful']
    negrsp=['very sorry to here that','i hope your day gets better','thats very unfortunate']
    otherrsp=['interesting','very good']
    thankyou=['thank you','i appreciate it',' it means a lot']
    personalqsword = ['how',"how's","hows",'life', 'you', 'going', 'hanging']
    pqwresponses = ['great, sir', 'never better!', 'fantasic,sir','amazing, sir']  # eventually add in abliity to ask how you are
   
    if(word=='good'):
        if (len(comand)<=3):
                more=False
        for i in goodwords:
            if i in comand:
                say(addsir('good '+i))
                return
            
    elif(word in goodpt2):
        if (len(comand)<=3):
            more=False
        say(addsir(word))
        return
    
    if(word=='hi' or word=='hello'):
        randphrase(greetings,True)
        hi=True
        if(len(comand)<3):
            more=False            

    elif(word=="thanks" or word=='thank'):
        randphrase(thankrsp,True)
        more=False
        return
    for i in range(len(personalqsword)):
        word1=personalqsword[i]
        if(word1 in comand):
            count+=1
    if (count>=2 and x==False):
        if (('spell' in comand) or ('spelled' in comand)):
            return
        print('herek')
        x=True
        if(len(comand)<=4):
            more=False
        elif(len(comand)<=5 and hi==True):
            more=False
        randphrase(pqwresponses,False)
        randphrase(counterhru,True)
        rsp=listen().split()
        for i in range(len(rsp)):
            word=rsp[i]
            if(word in negwords or ('could'in rsp and 'better' in rsp)):
                randphrase(negrsp,True)
                return
            elif (word in poswords or ('never'in rsp and 'better'in rsp)):
                randphrase(posrsp,True)
                #print('here')
                return
            else:
                continue
        return
    
    for i in range(len(disphr)):
        for j in disphr[i]:
            if j in comand:
                counter+=1
        if counter==len(disphr[i]):
            more=False
            return
    
            
    if (word in poswords and ('you' or 'your' or "you're")):
        randphrase(thankyou,True)
        more=False
    return

# if more==False:
#return

def getWeatherinfo(info, city, timeframe, timenum):  # add time frame
    global weatherPhrase
    global result
    global urls
    global errorMessage
    global cityLoc
    global uni
    global key
    print(timenum)
    
    #print(timenum)
    check = ["temp", "humidity", 'wind_speed']
    timenum -= 1
    url = "now"
    result = "hfasdhjgf"
    req = {}
    infostr = timeframe

    if (city == 'inside' or city=='here'):
        print(info)
        val=read(info)
        unit = uni[info]
        say('the '+info+' is '+val+unit+'inside')
        #say("the humidity is 15 percent")
        return

    if ("n/a" in urls[timeframe]):
        timeframe = urls[timeframe]['n/a']
    if ("n/a" in weatherPhrase[info]):
        info = weatherPhrase[info]['n/a']
    if (info == 'weather'):
        info = 'weather_code'
    elif (info == 'precipitation_probability' and timeframe == "now"):
        timeframe = 'minutes'

    if (city in cityLoc):
        lat = cityLoc[city][0]
        lon = cityLoc[city][1]
    else:
        city = cityLoc[2]
        lat = cityLoc[city][0]
        lon = cityLoc[city][1]

    if (timenum == 0 or timeframe == "now"):
        req = {"lat": lat, "lon": lon, "unit_system": "us", "fields": info, "apikey": key}
    elif (timeframe == 'minutes'):
        req = {"lat": lat, "lon": lon, "unit_system": "us", "timestep": "1", "start_time": "now", "fields": info,
               "apikey": key}
    else:
        req = {"lat": lat, "lon": lon, "unit_system": "us", "start_time": "now", "fields": info, "apikey": key}
    if (info == 'weather_code'):
        url = urls[timeframe]
        response = requests.request("GET", url, params=req)
        if (timeframe == "now"):
            result = response.json()[info]['value']
        else:
            result = response.json()[timenum][info]['value']

        weather = str(result)
        if (weather == "freezing_rain_heavy or weather" or weather == "freezing_rain" or weather == "freezing_rain_light" or weather == "freezing_drizzle"):
            weather = "freezing raining"
        elif (weather == "ice_pellets_heavy" or weather == "ice_pellets_light"):
            weather = "hailing"
        elif (weather == "snow_heavy" or weather == "ice_pellets" or weather == "snow_light" or weather == "flurries"):
            weather = "snowing"
        elif (weather == "tstorm"):
            weather = "thunder storming"
        elif (weather == "rain" or weather == "rain_heavy" or weather == "drizzle"):
            weather = "Raining"
        elif (weather == "fog_light" or weather == "fog"):
            weather = "foggy"
        elif (weather == "mostly_cloudy"):
            weather = "mostly cloudy"
        elif (weather == "cloudy"):
            weather = "cloudy"
        elif (weather == "partly_cloudy"):
            weather = "partly cloudy"
        elif (weather == "mostly clear"):
            weather = "mostly clear"
        else:
            weather = "clear"
        print(timeframe)
        if (timeframe == 'now'):
            say("in " + city + " it is " + str(weather) + ' right now')
        else:
            say("in " + city + " it will be " + str(weather) + ' in ' + str(timenum + 1) + ' ' + infostr)
        return

    elif (info != "hfasdhjgf"):
        url = urls[timeframe]

        response = requests.request("GET", url, params=req)
        if (timeframe == "now"):
            result = response.json()[info]['value']
            try:
                result=str(round(int(result),1))
            except TypeError:
                n=1
            say(weatherPhrase[info][0] + 'is ' + str(result) + weatherPhrase[info][1] + city + weatherPhrase[info][2])
            #print(result)
        elif (timeframe == 'days' and info in check):
            result1 = response.json()[timenum][info][0]['min']['value']
            result2 = response.json()[timenum][info][1]['max']['value']
            result = round((result1 + result2) / 2,1)
            say(weatherPhrase[info][0] + 'will be ' + str(result) + weatherPhrase[info][1] + city + ' in ' + str(
                timenum + 1) + ' ' + infostr)

        else:
            result = response.json()[timenum][info]['value']
            try:
                result=str(round(int(result),1))
            except TypeError:
                n=1
            say(weatherPhrase[info][0] + 'will be ' + str(result) + weatherPhrase[info][1] + city + ' in ' + str(
                timenum + 1) + ' ' + infostr)
            print(timenum)
    else:
        r = random.randint(1, len(errorMessage)) - 1
        say(errorMessage[r])
        return


def comands(comand):  # check in list thing!!!!!!!!!
    global gpiodict
    global weatherPhrase
    global word
    global searchwords
    global dayinfo
    global timerVal
    global timerTime
    global alarms
    alarm = False
    timer = False
    search = False
    login = False
    hours = False
    hours2=False
    city = cityLoc[2]
    code = 'hello'
    item = "n"
    maths={'+':"plus"}
    state = 'n'
    letstr = ''
    numk = []
    num = 0
    h = 0
    unit = "now"
    seco = "n/a"
    print(comand)

    for i in range(len(comand)):
        word = comand[i]
        pos=i
        
        personality(word)
        
        if(more==False):
            return
        if (word in weatherPhrase):
            code = word
        elif (word in gpiodict and 'computer' not in comand and 'pc' not in comand):
            item = word
            if (type(gpiodict[word]) != str):
                for i in range(len(comand)):
                    thing = comand[i]
                    if thing in gpiodict[word]:
                        seco = thing


        elif word in searchwords:
            search = True

        if (word in cityLoc):
            city = word
        elif ((word=='on' or word=='login') and ('computer' in comand or 'pc' in comand)):
            login=True
        elif ((word == 'on')):
            state = True
        elif (word == 'off'):
            state = False
        elif (word == 'spell' or word=='spelled'):
            if (word=='spell'):
                print('here')
                word2=comand[pos+1]
                letlist = [char for char in word2]
                print(word2)
            else:
                word2=comand[pos-1]
                letlist = [char for char in word2]
            say('the word ' + word2 + "is spelled,")
            for j in range(len(letlist)):
                say(letlist[j])
            return

        if (word == "alarm"):
            alarm = True
        elif (word == "timer"):
            timer = True
        numy = word.split(':')
        try:
            if (len(numy) == 2):
                try:
                    numk.append(int(numy[0]))
                    numk.append(int(numy[1]))
                except ValueError:
                    n = 1
                except IndexError:
                    n = 1

        except TypeError:
            n = 1
        try:
            numk.append(int(word))
        except ValueError:
            numk = numk

        if (word in dayinfo or word == "tomorrow"):
            if (word == "tomorrow"):
                num = 1
                unit = "day"
            else:
                num1 = dayinfo[word]
                num2 = date.today().weekday()
                num = num1 - num2personality(word) 
                print(num, num1, num2)
                if (num < 1):
                    num = abs(num) + 7
                if (num == 1):
                    unit = "day"
                else:
                    unit = "days"
        elif (word == 'at'):
            hours = True
        elif(word=='hour'or word=='hours'):
            hours2=True
        elif (word in urls):
            unit = word
        else:
            h += 1

    if (hours == True):
        print(num)
        if ("p.m." in comand or "afternoon" in comand or "night" in comand):
            numk[0] += 12
            num=numk[0]
        num2 = datetime.datetime.now().hour
        print(num2)
        num -= num2
        print(num)
        if (num == 1):
            unit = "hour"
        else:
            unit = "hours"
    if (hours2==True):
        try:
            num=numk[0]
        except IndexError:
            num=1
            
        if (num == 1):
            unit = "hour"
        else:
            unit = "hours"
        
    if (alarm == True):
        say("ok setting the alarm")
        if ("p.m." in comand or "afternoon" in comand or "night" in comand):
            numk[0] += 12
        try:
            alarms.append(numk[0] * 3600 + numk[1] * 60)
        except IndexError:
            alarms.append(numk[0] * 3600)
        return
    elif (timer == True):
        say("ok setting a timer")
        l1 = [datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second]
        timerTime.append(l1)
        if ("half" in comand):
            timerVal.append((numk[0] * 60 + 30) * 60)

        elif (unit == "hour" or unit == "hours"):
            timerVal.append(numk[0] * 3600)
        else:
            try:
                if (len(numk) == 1):
                    timerVal.append(numk[0] * 60)
                else:
                    timerVal.append((numk[0] * 60 + numk[1]) * 60)
            except TypeError:
                timerVal.append(numk[0] * 60)
        return

    if (item != 'n' and state != 'n'):
        gpioset(item, state, seco)
        return
    elif (code != 'hello'):
        getWeatherinfo(code, city, unit, num)
        return
    elif (login==True):
        GPIO.output(40, True)
        time.sleep(.1)
        GPIO.output(40, False)
        time.sleep(.1)
        say('activating your computer, sir')
    elif (search == True):
        
        num=0
        search_term = ""
        if('look' in comand and 'up' in comand):
            num=2
        elif('search'in comand):
            num=1
        if ('alfred' in comand):
            num+=1
            
        for i in range(num,len(comand)):
            if (comand[i] in maths):
                search_term=search_term +' '+maths[comand[i]]
            else:    
                search_term = search_term + " " + str(comand[i])
        print(search_term)
        x=searchlite.search(search_term)
        print(x)
        say(f'Here is what I found for {search_term} on google')
        say(x)
        return

    else:
        if(comand[0]=='hkg6dn3'):
            return
        else:
            r = random.randint(1, len(errorMessage)) - 1
            say(errorMessage[r])
            return


while (True):
    x=False
    more=True
    comstr = listen()
    com=comstr.split()
    print(comstr)
    if (datetime.datetime.now().minute * 60 + datetime.datetime.now().second - timecheck > 10):
        check = False


    if ('alfred' in comstr.split() and len(comstr.split())>=2):  # work on this to decrese latency
        print(1)
        timecheck = datetime.datetime.now().minute * 60 + datetime.datetime.now().second
        check = True
        comand = comstr.split()
        
        comands(comand)
        print('good to go')

    elif(check == True and comstr != 'hg'):
        timecheck = datetime.datetime.now().minute * 60 + datetime.datetime.now().second
        check=True
        print(comstr)
        comand = comstr.split()
        comands(comand)

    elif (comstr == 'alfred' or comstr=='hey alfred'):
        print(2)
        check = True
        timecheck = datetime.datetime.now().minute * 60 + datetime.datetime.now().second
        rp = random.randint(1, len(greet)) - 1
        say(greet[rp])  

    else:
        comtime = [datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second]
        print(3)
        for i in range(len(alarms)):
            mintotal1 = comtime[0] * 3600 + comtime[1] * 60 + comtime[2]
            if (mintotal1 >= alarms[i]):
                os.system('omxplayer -o local lmao.mp3')
                alarms.pop(i)
                break

        for i in range(len(timerTime)):
            mintotal1 = comtime[0] * 3600 + comtime[1] * 60 + comtime[2]
            mintotal2 = timerTime[i][0] * 3600 + timerTime[i][1] * 60 + timerTime[i][2]
            timel = mintotal1 - mintotal2

            if (timel >= timerVal[i]):
                print(timel)
                print(timerVal)
                os.system('omxplayer -o local lmao.mp3')
                timerVal.pop(i)
                timerTime.pop(i)
                break

    comand = []
    comstr = ""
