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
import pytoml as toml

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
l.on(0)
pi3 or l.use(1) # red

# ライトの設定
GPIO.setup(36, GPIO.OUT)
GPIO.output(36, GPIO.LOW) # 撮影時以外は消灯

## 待受ピンの設定
specs = []
PULL_UP_DOWN    = {"up":GPIO.PUD_UP, "down":GPIO.PUD_DOWN}
RAISING_FALLING = {"rising":GPIO.RISING, "falling":GPIO.FALLING}

tomlfile = '/boot/avis_courrier.toml'
with open(tomlfile) as fin:
  pin_settings = toml.load(fin)
for pin, to, script, pull_up_down, rising_falling in pin_settings["switches"]:
  print pin
  print to
  print script
  print pull_up_down
  print rising_falling
  GPIO.setup(int(pin), GPIO.IN, pull_up_down=PULL_UP_DOWN[pull_up_down])
  GPIO.add_event_detect(int(pin), RAISING_FALLING[rising_falling])
  specs.append({"pin":int(pin), "to":to, "script" :script })


def wait():
  global specs
  while True:
    try:
      for spec in specs:
        if GPIO.event_detected(spec["pin"]):
          logging.info("detect " + str(spec["pin"]))
          blink()
          avis(spec["to"],spec["script"])
    except:
      info=sys.exc_info()
      print "Unexpected error:"+ traceback.format_exc(info[0])
      print traceback.format_exc(info[1])
      print traceback.format_exc(info[2])
    time.sleep(2)

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
#    wait()
    wait()

if __name__ == '__main__':
#  print fork()
  wait()
