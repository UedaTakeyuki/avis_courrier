# coding:utf-8 Copy Right Atelier Grenouille © 2018 -
#
import os
import subprocess
import importlib
import led

import traceback
import sys
import RPi.GPIO as GPIO
import time

import ConfigParser
import requests
import piserialnumber as ps
import getrpimodel

# RPi 3 は LED1(赤LED)を操作できない
pi3 = True if getrpimodel.model() == "3 Model B" else False


# GPIO の設定
GPIO.setmode(GPIO.BOARD)

# 基盤LED の設定
l = led.LED()
l.use(0) # green
pi3 or l.use(1) # red

def wait():
  # 37(out, 1),35(in, 0)
  GPIO.setup(37, GPIO.OUT)
  GPIO.output(37, GPIO.HIGH)
  GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.add_event_detect(35, GPIO.RISING)
  # 33(out, 1),31(in, 0)
  GPIO.setup(33, GPIO.OUT)
  GPIO.output(33, GPIO.HIGH)
  GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.add_event_detect(31, GPIO.RISING)
  # 29(out, 1),27(in, 0)
  # 23(out, 1),21(in, 0)
  # 15(out, 1),13(in, 0)
  #  5(out, 1), 3(in, 0)
  # 37(out, 1),35(in, 0)
  while True:
    try:
      if GPIO.event_detected(35):
        l.off(0)
        time.sleep(1)
        l.on(0)
      elif GPIO.event_detected(31):
        l.off(0)
        time.sleep(1)
        l.on(0)
        time.sleep(1)
        l.off(0)
        time.sleep(1)
        l.on(0)
    except:
      info=sys.exc_info()
      print "Unexpected error:"+ traceback.format_exc(info[0])
      print traceback.format_exc(info[1])
      print traceback.format_exc(info[2])
    time.sleep(1)

def fork():
  pid = os.fork()
  if pid > 0:
    f = open('/var/run/avis_courrier.pid','w')
    f.write(str(pid)+"\n")
    f.close()
    sys.exit()

  if pid == 0:
    wait()

if __name__ == '__main__':
  print fork()