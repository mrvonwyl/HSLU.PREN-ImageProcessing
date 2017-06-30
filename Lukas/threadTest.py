import time
from threadedclass import threadedclass

my_class_instance = threadedclass()

# explicit start is better than implicit start in constructor
my_class_instance.start()
my_class_instance.update(5)
time.sleep(1)
my_class_instance.update(2)
time.sleep(2)
my_class_instance.update(3)
time.sleep(1)
number = my_class_instance.getX()
time.sleep(1)
print("finalnumber: "+str(number))

# you can kill the thread with
my_class_instance.cancel()