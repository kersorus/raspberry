import RPi.GPIO as GPIO
import time
import math
import numpy as np
import matplotlib.pyplot as plt

NUMBER_OF_LEDS = 8
#bits = [24, 25,  8, 7, 12, 16, 20, 21]
bits  = [10,  9, 11, 5,  6, 13, 19, 26]

def lightUp(ledNumber, period):
    GPIO.output(bits[ledNumber], GPIO.HIGH)
    time.sleep(period)
    GPIO.output(bits[ledNumber], GPIO.LOW)
    time.sleep(period)

def lightDown(ledNumber, period):
    GPIO.output(bits[ledNumber], GPIO.LOW)
    time.sleep(period)
    GPIO.output(bits[ledNumber], GPIO.HIGH)
    time.sleep(period)

def blink(ledNumber, blinkCount, blinkPeriod):
    for i in range(0, blinkCount):
        lightUp(ledNumber, blinkPeriod)

def runningLight(count, period):
    for i in range(0, count):
        for j in range(0, 8):
           lightUp(j, period) 

def runningDark(count, period):
    GPIO.output(bits, GPIO.HIGH)
    for i in range(0, count):
        for j in range(0, 8):
           lightDown(j, period)
    GPIO.output(bits, 0)

def decToBinList(decNumber):
    N = NUMBER_OF_LEDS - 1
    p = 0
    binNumber = []

    while N > 0:
        p = int(decNumber / 2 ** N)
        if p == 1:
            binNumber.append(1)
            decNumber -= 2 ** N
        else:
            binNumber.append(0)
        N -= 1
    binNumber.append(decNumber)
    return binNumber

def lightNumber(number):
    binNumber = decToBinList(number)
    binNumber = binNumber[::-1]
    GPIO.output(bits, binNumber)

def runningPattern(pattern, direction):
    #bitPattern = decToBinList(pattern)
    if(direction):
        while True:
            #print(pattern)
            lightNumber(pattern)
            time.sleep(1)
            #pattern = pattern >> 1
            if(getBit(pattern, 0) == 0):
                pattern = pattern >> 1
            elif(getBit(pattern, 0) == 1):
                pattern = pattern >> 1
                pattern |= 1 << (NUMBER_OF_LEDS - 1)
    elif(direction == 0):
         while True:
            #print(pattern)
            lightNumber(pattern)
            time.sleep(1)
            #pattern = pattern >> 1
            if(getBit(pattern, NUMBER_OF_LEDS - 1) == 0):
                pattern = pattern << 1
            elif(getBit(pattern, NUMBER_OF_LEDS - 1) == 1):
                pattern &= 2 ** (NUMBER_OF_LEDS - 1) - 1
                pattern = pattern << 1
                pattern |= 1

def SHIM(ledNumber, frequency):
    p = GPIO.PWM(bits[ledNumber], frequency)
    p.start(0)
    while True:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
    p.stop()
    GPIO.cleanup()
        
def getBit(number, bit):
    return (number >> bit) & 1


def num2dac (value):
    GPIO.output (bits, 0)
    lightNumber (value)

def firscript (value):
    while (value != -1):
        print ("Vvedite chislo (-1 dlya vixoda):")
        value = int (input ())
        num2dac (value)
    GPIO.output(bits, 0)

def secscript ():
    print ("Vvedite chislo povtorenii:")
    repetitionsNumber = int (input ())
    for i in range (0, repetitionsNumber):
        for j in range (0, 256):
            num2dac (j)
            time.sleep (0.01)
        for k in range (1, 256):
            num2dac (256 - k)
            time.sleep (0.01)
    GPIO.output (bits, 0)

def trdscript (timelen):
    print ("Vvedite frequency:")
    frequency = int ( input())
    print ("Vvedite samplingFrequency:")
    samplingFrequency = int ( input())

    times = np.arange (0, timelen, 1/samplingFrequency)
    amplitude = np.sin (times * frequency * 2 * 3.1416) + 1

    amplitudes = 255 * (np.sin(times * frequency * 2 * 3.1416) + 1) / 2
    plt.plot(times, amplitudes)
    plt.show()

    for k in range (timelen * samplingFrequency):
        num2dac (int (255 * amplitude [k] / 2))
        time.sleep (1/samplingFrequency)

    GPIO.output (bits, 0)



GPIO.setmode(GPIO.BCM)
GPIO.setup  (bits, GPIO.OUT)
GPIO.output (bits, GPIO.LOW)

#lightUp(5, 1)
#GPIO.output(bits, 1)
#blink(1, 4, 1)
#runningLight(2000, 0.1)
#runningDark(5, 0.1)
#print(decToBinList(128))
#lightNumber(16)
#runningPattern(157, 0)
#SHIM(1, 150)

#firscript (1)
secscript ()
#trdscript (3)