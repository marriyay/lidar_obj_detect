#!/usr/bin/env python3
'''Records measurements to a given file. Usage example:

$ ./record_measurements.py out.txt'''
import sys
import time
from rplidar import RPLidar

PORT_NAME = '/COM5'

'Main function'
lidar = RPLidar(PORT_NAME)
outfile = open("C:/Users/User/PycharmProjects/rpLidar/out.txt", 'w')
time.sleep(5)
print('Recording measurements...')
for i, measurement in enumerate(lidar.iter_measurments()):
    if (i > 1500) & (i < 5000):
        print('%d: Got %d measurements' % (i, len(measurement)))
        line = '\t'.join(str(v) for v in measurement)
        outfile.write(line + '\n')
    if (i > 4500):
        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
outfile.close()
