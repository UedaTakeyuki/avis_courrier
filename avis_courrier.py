# coding:utf-8 Copy Right Atelier Grenouille © 2018 -
#
import os
import shutil
import subprocess
import importlib
import led

import traceback
import sys
import RPi.GPIO as GPIO
import time
import datetime 

import ConfigParser
import requests
import piserialnumber as ps
import getrpimodel
import requests

import perspective

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
#  GPIO.setup(29, GPIO.OUT)
#  GPIO.output(29, GPIO.HIGH)
#  GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#  GPIO.add_event_detect(27, GPIO.RISING)
  # 23(out, 1),21(in, 0)
#  GPIO.setup(23, GPIO.OUT)
#  GPIO.output(23, GPIO.HIGH)
#  GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#  GPIO.add_event_detect(21, GPIO.RISING)
  # 15(out, 1),13(in, 0)
  GPIO.setup(15, GPIO.OUT)
  GPIO.output(15, GPIO.HIGH)
  GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.add_event_detect(13, GPIO.RISING)
  #  5(out, 1), 3(in, 0)
  GPIO.setup(5, GPIO.OUT)
  GPIO.output(5, GPIO.HIGH)
  GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.add_event_detect(3, GPIO.RISING)

  # 40(out, 1),38(in, 0)
  GPIO.setup(40, GPIO.OUT)
  GPIO.output(40, GPIO.HIGH)
  GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.add_event_detect(38, GPIO.RISING)
  # 18(out, 1),16(in, 0)
  GPIO.setup(18, GPIO.OUT)
  GPIO.output(18, GPIO.HIGH)
  GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.add_event_detect(16, GPIO.RISING)

  while True:
    try:
      if GPIO.event_detected(35):
        detect_35()
      elif GPIO.event_detected(31):
        detect_31()
    except:
      info=sys.exc_info()
      print "Unexpected error:"+ traceback.format_exc(info[0])
      print traceback.format_exc(info[1])
      print traceback.format_exc(info[2])
    time.sleep(1)

def detect_35():
  l.off(0)
  time.sleep(1)
  l.on(0)

def detect_31():
  l.off(0)
  time.sleep(1)
  l.on(0)
  time.sleep(1)
  l.off(0)
  time.sleep(1)
  l.on(0)

def take_photo(filename, device, size):
#  command_str = os.path.dirname(os.path.abspath(__file__))+'/photographier.sh '+'v1.tmp.jpg'+' '+'video1'+' 640x480'
  command_str = os.path.dirname(os.path.abspath(__file__))+'/photographier.sh '+filename+'.tmp'+' '+device+' '+size
  p = subprocess.check_call(command_str, shell=True)
  perspective.transform(filename+'.tmp', filename, 400, 200, 90)
  os.remove(filename+'.tmp')

def avis():
  server_url = "http://titurel.uedasoft.com/biff/index.test.php"
  now = datetime.datetime.now() # 時刻の取得
  now_string = now.strftime("%Y/%m/%d %H:%M:%S")
  filename = now.strftime("%Y.%m.%d.%H%M%S")+".jpg"
#  print filename
  take_photo(filename, "video0", "640x480")
  files = {'upfile': open(filename, 'rb')}
#  payload = {'serial_id': serialid, 'device': device, 'datetime': now_string}
  payload = {'usename': 'yes'}
  r = requests.post(server_url, data=payload, files=files, timeout=10, cert=os.path.dirname(os.path.abspath(__file__))+'/slider.pem', verify=False)
  if not os.path.exists("/boot/DATA/biff"):
    os.makedirs("/boot/DATA/biff")
  shutil.move(filename,"/boot/DATA/biff/"+filename)

  server_url = "http://titurel.uedasoft.com/biff/send.test.php"
  payload = {'to': 'ueda', 'filename': filename, 'now': now_string}
  r = requests.post(server_url, data=payload, files=files, timeout=10, cert=os.path.dirname(os.path.abspath(__file__))+'/slider.pem', verify=False)
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