# sensor-and-sprayer
As simple as dht11 to raspi to relay to valve

### Device parts
* Raspberry Pi 3B+
* DHT11
* Relay module 8 in 1 with optocoupler
* Electronic valve FCD-180B

### Pin assignment and connection
**Pin name | Assignment | Connection**
---|---|---
Raspberry Pi
GPIO17 | Digital out to relay | IN 1
GPIO27 | Data read from sensor | Pin 2
+3.3V | Powering sensor | Pin 1
+5V | Powering relay | VCC
GND | Common ground | GND, Pin 4
DHT11
Pin 1 | Power in | +3.3V
Pin 2 | Data out | GPIO27
Pin 4 | Common ground | GND
Relay 8 in 1
GND | Common ground | GND, Pin 4
IN 1 | Digital in | GPIO17
VCC | Power in | +5V
Pull-up resistor 5k Ohm
End 1 | | +3.3V, Pin 1
End 2 | | GPIO27, Pin 2

### Usage
`$ python3 spray1.py -d <duration> -i <interval> -l <humidity limit>`

