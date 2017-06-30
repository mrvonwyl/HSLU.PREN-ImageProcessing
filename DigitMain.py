import time
from DigitDetection import DigitDetection

dd = DigitDetection()
dd.start()
time.sleep(60)
number = dd.getNumber()
dd.cancel()
print('number: ' + repr(number))
