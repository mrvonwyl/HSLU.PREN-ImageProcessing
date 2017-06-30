import time
from DigitDetection import DigitDetection

dd = DigitDetection()
dd.start()
time.sleep(15)
number = dd.getNumber()
dd.cancel()
print('number: ' + repr(number))
