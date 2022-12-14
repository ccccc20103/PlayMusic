import speech_recognition as sr
import re
import requests
from bs4 import BeautifulSoup
import urllib3
import wave
import pyaudio
import matplotlib.pyplot as plt
import time
import webbrowser
import random
from gtts import gTTS
#from wavefile import WaveReader

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5





def record(filename='output.wav'):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK)
    print("* recording")
    frames = []
    sound = False
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def read():
    print('.')
    r = sr.Recognizer()
    r.energy_threshold = 10000
    r.dynamic_energy_threshold = False
    r.pause_threshold = 0.8
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        audio = r.listen(source)
    print('.')
    try:
        #if !(r.recognize_google(audio,language="zh-TW")) is None:
        print("Transcription: " + r.recognize_google(audio,language="zh-TW"))
    except LookupError:
        print("Could not understand audio")
    return r.recognize_google(audio,language="zh-TW")
cont = 0
entry = 0
end = 0
def search(string):
    global cont,entry,txt
    string = string.replace(" ","+")
    print(string)
    url = "https://www.youtube.com/results?search_query=" + string
    print(url)
    res = requests.get(url)
    cont = res.content
    cont = cont.decode()
    soup = BeautifulSoup(cont,'html.parser')
    last = None
    tit_last = None
    entry = cont.find('videoRenderer')
    txt = cont.find('"title":{"runs":[{"text":"')
    end = 0
    txt_end = 0

def show():
    global cont,entry,txt
    result = []
    n=3
    end = 0
    txt_end = 0
    last = -1
    tit_last = -1
    while ((entry>=0) & (n>0)):
        while (end < entry+27):
            end = cont.find('"',end+1)
        m = cont[(entry+27) : end]
        if m:
            target = m
            if target == last:
                continue
            last = target
            result.append(target)
            n -= 1
        entry = cont.find('videoRenderer',entry+1)
    n=3
    while ((txt>=0) & (n>0)):
        while (txt_end < txt+26):
            txt_end = cont.find('"',txt_end+1)
        tit = cont[(txt+26) : txt_end]
        if tit:
            tit_targ = tit
            if (tit_targ == tit_last):
                continue
            tit_last = tit_targ
            print(tit_last)
            n-=1
        txt = cont.find('"title":{"runs":[{"text":"',txt+1)
    return result

while (True):
    resultUrl = "https://www.youtube.com/watch?v="
    filename = 'test3.wav'
    #record(filename)
    ans = read()
    urllib3.disable_warnings()
    string = ans
    sea = ['?????????????????????????????????????????????????????????????????????','????????????????????????','???????????????????????????????????????']
    bye = ['??????','Bye','Goodbye','??????']
    hello = ['???????????????','?????????','Hello???','????????????????']
    wtf = ['????????????','???????????????????????????','what are you talking about???','???????????????????????????']
    #wtf = ['??????????????????','???????????????????????????','???????????????','???????????????????????????']
    if ( string.find('??????',0) >= 0 ):
        string = string.replace("??????","")
        search(string)
        result = show()
        print(sea[random.randint(0,len(sea)-1)])
    elif (string.find("?????????") >= 0):
        print("???????????????")
        result = show()
        print(sea[random.randint(0,len(sea)-1)])
    elif ( (string.find("??????") >= 0) | (string.find("??????") >= 0)):
        print(bye[random.randint(0,len(bye)-1)])
        break
    elif ( string.find('???') >= 0 ):
        if( string[(string.find('???') +1)] == '???' ):
            pick = int(1)
        elif ( string[(string.find('???') +1)] == '???' ):
            pick = int(2)
        elif ( string[(string.find('???') +1)] == '???' ):
            pick = int(3)
        else:
            pick = int (string[(string.find('???') +1)])
        print("??????????????????",pick,"??????")
        play = resultUrl + result[pick-1]
        webbrowser.open(play)
    elif (string.find(' ') == 0):
        if( random.random() > 0.5 ):
            print(hello[random.randint(0,len(hello)-1)])
        continue
    else:
        print(wtf[random.randint(0,len(wtf)-1)])
        print("")