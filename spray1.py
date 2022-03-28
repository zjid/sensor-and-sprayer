import Adafruit_DHT
import gpiozero
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sensor', type=int, help='gpio input pin for sensor', default=27)
parser.add_argument('-r', '--relay', type=int, help='gpio output pin for sprayer relay', default=17)
parser.add_argument('-d', '--duration', type=int, help='duration of the data logging in seconds', default=10)
parser.add_argument('-i', '--interval', type=int, help='Interval between each data logging in seconds', default=5)
parser.add_argument('-l', '--humidity', type=int, help='humidity limit between sprayer relay on and off', default=74)
args = parser.parse_args()

sensor_gpio = args.sensor #27
sprayer_gpio = args.relay #17
durasi = args.duration #7 * 3600 # detik
interval = args.interval #5 # detik
batas_kelembapan = args.humidity #74

class filekita:
  
  # time, sensor_good, humidity, temperature, spraying
  # time, boolean, float, float, boolean
  def buatfile(self):
    '''Required to create self.nama'''

    def duadigit(n):
      '''Returns 2 digits or more as string'''
      if n < 10: return '0' + str(n)
      return str(n)

    tahun_detik = time.localtime()[0:6]
    nama = 'gardenlog' + ''.join(map(duadigit, tahun_detik)) + '.csv'

    with open(nama, 'x') as f:
      f.write('time,sensor_good,humidity,temperature,spraying\n')

    self.nama = nama

  def catat(self, *args):
    '''args: time, sensor_good, humidity, temperature, spraying'''
    catatan = ','.join(map(str, args))
    for i in [1,2,3]:
      try:
        with open(self.nama, 'a') as f:
          f.write(catatan + '\n')
        print('[I] Data:', catatan)
        break
      except:
        print('[W] Gagal catat, percobaan', i)

sensor = Adafruit_DHT.DHT11
sprayer = gpiozero.DigitalOutputDevice(sprayer_gpio)
sprayer.active_high = False
sprayer.off()
spraying = False
gardenlog = filekita()
gardenlog.buatfile()
tidur = max( 0.8 * interval, interval - 1 )
selesai = time.time() + durasi + 0.1

print('Pendataan dimulai:')

while True:
  now = time.time()
  if now >= selesai: break
  hum, tem = Adafruit_DHT.read(sensor, sensor_gpio)
  if hum is not None and tem is not None and hum < 100:
    if hum < batas_kelembapan and not spraying:
      sprayer.on()
      spraying = True
    elif hum > batas_kelembapan and spraying:
      sprayer.off()
      spraying = False
    gardenlog.catat(now, True, hum, tem, spraying)
  else:
    gardenlog.catat(now, False, 0.0, 0.0, spraying)
  time.sleep(tidur)
  next = now + interval
  while True:
    if time.time() >= next: break
  # print(now, time.time())

print('Pendataan selesai.')
