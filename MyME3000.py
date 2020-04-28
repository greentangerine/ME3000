# Highbanks ME3000

SLAVE=0x01
THRESHOLD_FILE="/home/pi/ME3000/pct.txt"
SERIAL_PORT="/dev/ttyUSB0"

# MQTT
ME3000_NAME='me3000'
MQTT_HOST='localhost'
MQTT_USER='emonpi'
MQTT_PWD='emonpimqtt2016'

TOPICS = ((6, 'voltage', 'H'),
          (7, 'current', 'h'),
          (14, 'batt_voltage', 'H'),
          (15, 'batt_current', 'h'),
          (16, 'batt_capacity', 'H'),
          (25, 'sell_grid', 'H'),
          (26, 'buy_grid', 'H'),
          (27, 'load_use', 'H'),
          (36, 'charge_total', 'H'),
          (37, 'discharge_total', 'H')
         )
  
