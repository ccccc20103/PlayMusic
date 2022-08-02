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
    sea = ['如果找不到想要的，要不要試試看多加其他關鍵字？','有找到想要的嗎？','不要浪費時間了，趕快選一個']
    bye = ['再見','Bye','Goodbye','拜噗']
    hello = ['你還在嗎？','哈囉？','Hello？','有人在嗎?？']
    wtf = ['我聽不懂','不好意思，我聽不懂','what are you talking about？','請問你在講什麼呢？']
    #wtf = ['りしれ供さ小','不好意思，我聽不懂','此人話否？','你在講什麼瘋狗話？']
    if ( string.find('搜尋',0) >= 0 ):
        string = string.replace("搜尋","")
        search(string)
        result = show()
        print(sea[random.randint(0,len(sea)-1)])
    elif (string.find("下三個") >= 0):
        print("顯示下三筆")
        result = show()
        print(sea[random.randint(0,len(sea)-1)])
    elif ( (string.find("拜拜") >= 0) | (string.find("再見") >= 0)):
        print(bye[random.randint(0,len(bye)-1)])
        break
    elif ( string.find('第') >= 0 ):
        if( string[(string.find('第') +1)] == '一' ):
            pick = int(1)
        elif ( string[(string.find('第') +1)] == '二' ):
            pick = int(2)
        elif ( string[(string.find('第') +1)] == '三' ):
            pick = int(3)
        else:
            pick = int (string[(string.find('第') +1)])
        print("好的，播放第",pick,"首歌")
        play = resultUrl + result[pick-1]
        webbrowser.open(play)
    elif (string.find(' ') == 0):
        if( random.random() > 0.5 ):
            print(hello[random.randint(0,len(hello)-1)])
        continue
    else:
        print(wtf[random.randint(0,len(wtf)-1)])
        print("")