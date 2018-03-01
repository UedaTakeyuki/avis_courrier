# coding:utf-8 Copy Right Atelier Grenouille © 2018 -
#
import os
import shutil
import subprocess
import logging
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

# logging
logging.basicConfig(format='%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s',filename='/var/log/SCRIPT/avis_courrie.log',level=logging.DEBUG)

# config
configfile = "/boot/avis_courrier.ini"
ini = ConfigParser.SafeConfigParser()
ini.read(configfile)

# RPi 3 は LED1(赤LED)を操作できない
pi3 = True if getrpimodel.model() == "3 Model B" else False

# GPIO の設定
GPIO.setmode(GPIO.BOARD)

# 基盤LED の設定
l = led.LED()
l.use(0) # green
pi3 or l.use(1) # red

# ライトの設定
GPIO.setup(36, GPIO.OUT)
GPIO.output(36, GPIO.LOW) # 撮影時以外は消灯

def wait():
  GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.add_event_detect(37, GPIO.FALLING)
  GPIO.add_event_detect(35, GPIO.FALLING)
  GPIO.add_event_detect(33, GPIO.FALLING)
  GPIO.add_event_detect(31, GPIO.FALLING)

  GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.add_event_detect(12, GPIO.FALLING)
  GPIO.add_event_detect(10, GPIO.FALLING)
  GPIO.add_event_detect(8, GPIO.FALLING)

#  GPIO.setup(28, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  '''  GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)'''
#  GPIO.add_event_detect(28, GPIO.FALLING)
  '''  GPIO.add_event_detect(26, GPIO.FALLING)
  GPIO.add_event_detect(24, GPIO.FALLING)
  GPIO.add_event_detect(22, GPIO.FALLING)'''
  while True:
    try:
      if GPIO.event_detected(37):
        logging.info("detect 37")
        detect_37()
      elif GPIO.event_detected(35):
        logging.info("detect 35")
        detect_35()
      elif GPIO.event_detected(33):
        logging.info("detect 33")
        detect_33()
      elif GPIO.event_detected(31):
        logging.info("detect 31")
        detect_31()
      elif GPIO.event_detected(12):
        logging.info("detect 12")
        detect_12()
      elif GPIO.event_detected(10):
        logging.info("detect 10")
        detect_10()
      elif GPIO.event_detected(8):
        logging.info("detect 8")
        print("8")

#      elif GPIO.event_detected(28):
#        print("28")
      '''      elif GPIO.event_detected(26):
        logging.info("detect 26")
        print("26")
      elif GPIO.event_detected(24):
        logging.info("detect 24")
        print("24")
      elif GPIO.event_detected(22):
        logging.info("detect 22")
        print("22")'''
    except:
      info=sys.exc_info()
      print "Unexpected error:"+ traceback.format_exc(info[0])
      print traceback.format_exc(info[1])
      print traceback.format_exc(info[2])
    time.sleep(2)

def detect_37():
  blink()
  print("37")
  avis('zenin', 'send.php')
  pass
def detect_35():
  blink()
  print("35")
  avis('koike', 'send.php')
  pass
def detect_33():
  blink()
  print("33")
  avis('iwasaki', 'send.php')
  pass
def detect_31():
  blink()
  print("31")
  avis('sekine', 'send.php')
  pass
def detect_12():
  blink()
  print("12")
  avis('tomari', 'send.php')
  pass
def detect_10():
  print("10")
  blink()
  avis('ueda', 'send.test.php')
#  avis('yamazaki', 'send.php')

def blink():
  l.off(0)
  time.sleep(1)
  l.on(0)

def take_photo(filename, device, size):
  global ini
  command_str = os.path.dirname(os.path.abspath(__file__))+'/photographier.sh '+filename+'.tmp'+' '+device+' '+size
  GPIO.output(36, GPIO.HIGH) # 撮影のために点灯
  p = subprocess.check_call(command_str, shell=True)
  GPIO.output(36, GPIO.LOW)  # 撮影後は消灯
  perspective.transform(filename+'.tmp', 
                        filename, 
                        int(ini.get("perspective", "left")), 
                        int(ini.get("perspective", "right")), 
                        int(ini.get("perspective", "depth"))
                        )
  os.remove(filename+'.tmp')

def avis(to, script):
  global ini
  proxies = {}
  if "http_proxy" in ini.options("proxy"):
    proxies['http'] = ini.get("proxy", "http_proxy")
  if "https_proxy" in ini.options("proxy"):
    proxies['https'] = ini.get("proxy", "https_proxy")
  print (proxies)
  server_url = "http://titurel.uedasoft.com/biff/index.test.php"
  now = datetime.datetime.now() # 時刻の取得
  now_string = now.strftime("%Y/%m/%d %H:%M:%S")
  filename = now.strftime("%Y.%m.%d.%H%M%S")+".jpg"
#  take_photo(filename, "video0", "640x480")
  take_photo(filename, "video0", ini.get("photo", "size"))
  print "take photo end"
  files = {'upfile': open(filename, 'rb')}
  payload = {'usename': 'yes'}
  r = requests.post(server_url, data=payload, files=files, timeout=10, cert=os.path.dirname(os.path.abspath(__file__))+'/slider.pem', verify=False, proxies=proxies)
#  command_str = 'curl -F "data=@/home/pi/SCRIPT/avis_courrier/'+filename+'"' + ' -F "usename=yes" http://titurel.uedasoft.com/biff/index.test.php'
#  p = subprocess.check_call(command_str, shell=True)
  print "photo sent"
  if not os.path.exists("/boot/DATA/biff"):
    os.makedirs("/boot/DATA/biff")
  shutil.move(filename,"/boot/DATA/biff/"+filename)
  print "photo moved"

  server_url = "http://titurel.uedasoft.com/biff/"+script
  payload2 = {'to': to, 'filename': filename, 'now': now_string}
  r = requests.post(server_url, data=payload2, timeout=10, cert=os.path.dirname(os.path.abspath(__file__))+'/slider.pem', verify=False)
  print "avis end"

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
#  print fork()
  wait()
