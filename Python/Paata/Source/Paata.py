from tkinter import *
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import os
import time
import threading
import math


def add():
    global file
    file = filedialog.askopenfilename()
    if file:
        add_to_playlist(file)


def add_to_playlist(file):
    global playList, index
    extension = os.path.splitext(file)[1]
    if extension != ".mp3":
        statusbar['text'] = 'Unsupported file format'
        return
    playList.insert(index, file)
    filename = os.path.basename(file)
    playListBox.insert(index, filename)
    index += 1
    statusbar['text'] = 'Ready'


def delete():
    if playListBox and playList:
        selectedIndex = (int)((playListBox.curselection())[0])
        playListBox.delete(selectedIndex)
        playList.pop(selectedIndex)


def play_pause():
    global paused, totalLength, timeThread
    if paused:
        playPauseButton.configure(image=pausePhoto)
        paused = False
        statusbar['text'] = 'Playing'
        mixer.music.unpause()
    elif mixer.music.get_busy():
        playPauseButton.configure(image=playPhoto)
        paused = True
        statusbar['text'] = 'Paused'
        mixer.music.pause()
    else:
        if playListBox.curselection():
            playPauseButton.configure(image=pausePhoto)
            selectedIndex = (int)((playListBox.curselection())[0])
            mixer.music.load(playList[selectedIndex])
            statusbar['text'] = 'Playing'
            showDetails()
            mixer.music.play()
            timeThread = threading.Thread(target=start_counter, args=(totalLength,))
            timeThread.start()
        else:
            statusbar['text'] = 'Select from playlist'


def start_counter(length):
    global totalLength, repeated

    while length and mixer.music.get_busy():
        if paused:
            continue

        if repeated:
            length = totalLength
            repeated = False

        hours = (length / 60) / 60
        minutes = length / 60
        seconds = length % 60
        hours = int(hours)
        minutes = int(minutes)
        seconds = round(seconds)
        timeFormat = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        currentTimeLabel['text'] = 'Current time - ' + format(timeFormat)
        time.sleep(1)
        length -= 1

    if(length == 0):
        totalTimeLabel['text'] = 'Total time - 00:00:00'
        currentTimeLabel['text'] = 'Current time - 00:00:00'


def repeat():
    global paused, timeThread, repeated
    paused = False
    if mixer.music.get_busy():
        repeated = True
        playPauseButton.configure(image=pausePhoto)
        statusbar['text'] = 'Playing'
        mixer.music.play()


def stop():
    global paused, timeThread
    paused = False
    if mixer.music.get_busy():
        statusbar['text'] = 'Ready'
        playPauseButton.configure(image=playPhoto)
    totalTimeLabel['text'] = 'Total time - 00:00:00'
    currentTimeLabel['text'] = 'Current time - 00:00:00'
    mixer.music.stop()


def setVol(value):
    volume = int(value) / 100  # mixer.music.set_volume accepts volume only from 0 to 1
    mixer.music.set_volume(volume)  # Pass volume from 0 to 1. Example: 0.50 is 50% volume


def mute():
    global muted, currentVolume
    if muted:
        muteButton.configure(image=volumePhoto)
        muted = False
        statusbar['text'] = 'Ready'
        if mixer.music.get_busy():
            statusbar['text'] = 'Playing'
        volumeScale.set(currentVolume)
    else:
        muteButton.configure(image=mutePhoto)
        currentVolume = math.ceil(mixer.music.get_volume() * 100)
        muted = True
        statusbar['text'] = 'Muted'
        volumeScale.set(0)


def showDetails():
    global file, totalLength
    audio = MP3(file)
    totalLength = audio.info.length
    totalLength = round(totalLength)
    hours = (totalLength / 60) / 60
    minutes = totalLength / 60
    seconds = totalLength % 60
    hours = int(hours)
    minutes = int(minutes)
    seconds = round(seconds)
    timeFormat = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    totalTimeLabel['text'] = 'Total time - ' + format(timeFormat)


def exit():
    stop()
    mainWindow.destroy()


# **************************************************************************************************


mainWindow = Tk()
mixer.init()
paused = False
muted = False
repeated = False
totalLength = 0
timeThread = 0
playList = []
index = 0

mainWindow.geometry('320x300')
mainWindow.title('Paata')
titleIcon = PhotoImage(file=r'..\Icons\paata.png')
mainWindow.iconphoto(False, titleIcon)

statusbar = Label(mainWindow, text='Ready', relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

leftFrame = Frame(mainWindow)
leftFrame.pack(side=LEFT, padx=5, pady=10)

rightFrame = Frame(mainWindow)
rightFrame.pack(side=RIGHT, padx=5, pady=10)

topLeftFrame1 = Frame(leftFrame)
topLeftFrame1.pack(side=TOP, padx=5, pady=10)
topLeftFrame2 = Frame(leftFrame)
topLeftFrame2.pack(side=TOP, padx=5, pady=10)

topRightFrame1 = Frame(rightFrame)
topRightFrame1.pack(side=TOP, padx= 5, pady=10)
topRightFrame2 = Frame(rightFrame)
topRightFrame2.pack(side=TOP, padx=5, pady=10)

playPhoto = PhotoImage(file=r'..\Icons\play.png')
pausePhoto = PhotoImage(file=r'..\Icons\pause.png')
playPauseButton = Button(topRightFrame1, image=playPhoto, command=play_pause)
playPauseButton.grid(row=0, column=0, padx=5, pady=10)

repeatPhoto = PhotoImage(file=r'..\Icons\repeat.png')
repeatButton = Button(topRightFrame1, image=repeatPhoto, command=repeat)
repeatButton.grid(row=0, column=1, padx=5, pady=10)

stopPhoto = PhotoImage(file=r'..\Icons\stop.png')
stopButton = Button(topRightFrame1, image=stopPhoto, command=stop)
stopButton.grid(row=0, column=2, padx=5, pady=10)

playListBox = Listbox(topLeftFrame1)
playListBox.grid(row=0, column=0, padx=5, pady=10)

addButton = Button(topLeftFrame2, text="   +   ", command=add)
addButton.grid(row=0, column=0, padx=5)
deleteButton = Button(topLeftFrame2, text="   -   ", command=delete)
deleteButton.grid(row=0, column=1, padx=5)

totalTimeLabel = Label(topRightFrame2, text='Total time - 00:00:00', relief=GROOVE)
totalTimeLabel.grid(row=0, column=0, padx=5, pady=10)
currentTimeLabel = Label(topRightFrame2, text='Current time - 00:00:00', relief=GROOVE)
currentTimeLabel.grid(row=1, column=0, padx=5, pady=10)

bottomRightFrame = Frame(rightFrame)
bottomRightFrame.pack(side=BOTTOM, pady=10)

volumePhoto = PhotoImage(file=r'..\Icons\volume.png')
mutePhoto = PhotoImage(file=r'..\Icons\mute.png')
muteButton = Button(bottomRightFrame, image=volumePhoto, command=mute)
muteButton.grid(row=0, column=0, padx=5, pady=10)

volumeScale = Scale(bottomRightFrame, from_=0, to=100, orient=HORIZONTAL, command=setVol)
volumeScale.grid(row=0, column=1, padx=5, pady=10)
volumeScale.set(100)

# this removes the maximize button
mainWindow.resizable(0, 0)
mainWindow.protocol('WM_DELETE_WINDOW', exit)
mainWindow.mainloop()