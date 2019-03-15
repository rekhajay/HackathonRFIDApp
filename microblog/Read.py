

#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import time
import os
from sqlalchemy  import *
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

connstring = 'sqlite:///' + os.path.join(basedir, 'app.db')
engine = create_engine(connstring)

engine.echo = False
metadata = MetaData (bind=engine)

swipe = Table ('swipe', metadata,
	      Column('id', Integer, primary_key=True),
              Column ('rfid', Integer),
              Column ('time', DateTime),
)
if not engine.dialect.has_table(engine, 'swipe'):
 swipe.create()
  


#print ('Id:' ,row[0])
#print ('Rfid:', row['rfid'])



reader = SimpleMFRC522.SimpleMFRC522()
#Looks like the base library has set it for Pin number mode, So we are going to use it that way

try:
 time.sleep (1)
 LED =12
        #GPIO.setmode (GPIO.BCM)
	#for x in range (2,25):
 GPIO.setup(LED, GPIO.OUT)
 while True:
  id, text = reader.read()	
  GPIO.output(LED, GPIO.HIGH)	
  time.sleep(1)
  GPIO.output(LED, GPIO.LOW)
  print(id)
  print(text)
  with engine.connect() as connection:
   tim = datetime.datetime.now()
   connection.execute(swipe.insert().values(rfid=text, time=tim))
   sel = select([swipe])
   res = connection.execute(sel)
#   print(row['rfid'])
finally:
  GPIO.cleanup()


