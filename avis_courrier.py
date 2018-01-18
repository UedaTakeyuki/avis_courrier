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

# 37(out, 1),35(in, 0)
GPIO.setup(37, GPIO.OUT)
GPIO.output(37, GPIO.HIGH)
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# 33(out, 1),31(in, 0)
# 29(out, 1),27(in, 0)
# 23(out, 1),21(in, 0)
# 15(out, 1),13(in, 0)
#  5(out, 1), 3(in, 0)

# 基盤LED の設定
l = led.LED()
l.use(0) # green
pi3 or l.use(1) # red

if GPIO.input(35):
  l.off(0)  # green off
  pi3 or l.on(1) # red on
else:
  l.on(0)  # green on
  pi3 or l.off(1) # red off

def wait():
  pass

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