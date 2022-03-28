# https://www.thegeekpub.com/236867/using-the-dht11-temperature-sensor-with-the-raspberry-pi/

# Kode ini efektif namun bersifat sementara.
# 1. masih menggunakan objek LED lalu dibalik untuk relay active low
# 2. belum menggunakan hysteresis agar respon tidak terlalu cepat
# 3. terkait perangkat keras, masih ditemukan gagal baca sensor

import Adafruit_DHT
from gpiozero import LED
from time import sleep

sensor = Adafruit_DHT.DHT11
pin = 27
not_relay = LED(17)

def relay_on():
  not_relay.off()
def relay_off():
  not_relay.on()

relay_rest = True
relay_off()
while True:
  hum, tem = Adafruit_DHT.read(sensor, pin)
  if hum is not None and tem is not None:
    print(f'Humidity = {hum}%, Temperature = {tem}C')
    if hum < 70 and relay_rest:
      relay_on()
      relay_rest = False
      print('Sprayer activated.')
    elif hum > 70 and not relay_rest:
      relay_off()
      relay_rest = True
      print('Sprayer deactivated.')
  else:
    print('Sensor failure. Check wiring.')
  sleep(3)
