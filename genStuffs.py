import datetime
import time
from faker import Faker

faker = Faker()
'''
data type testing
'''
dt = datetime.datetime(2019, 1, 22, 17, 8, 19)
print(dt)
print(type(dt))

timestamp = time.mktime(dt.timetuple())
print(timestamp)
print(type(timestamp))

print(faker.name())