import re
import math
from math import fabs
from operator import itemgetter

infile = open("C:/Users/User/PycharmProjects/rpLidar/out.txt", 'r')

p = []  # points list p[i] = (i.angle, i.direction)
points = [line.strip() for line in infile]
for i in range(points.__len__()):
    abc = re.split(r'\t+', points[i].rstrip('\t'))
    p.append([float(abc[2]), float(abc[3])])
infile.close()

# p.sort(key=itemgetter(0))
#
# distance = []  # distance list distance[i] = (i.distance), where i is angle (i = 0..360)
# cc = 0
# for i in range(360):
#     while p[cc][0] < (i + 1):
#         cc = cc + 1
#         if cc >= p.__len__():
#             break
#         innersum = 0
#         innersummul = 0
#         if p[cc][1] > 0:
#             innersum = innersum + p[cc][0]
#             innersummul = innersummul + p[cc][0] * p[cc][1]
#         else:
#             innersum = -20000000000
#             innersummul = 2
#         if innersum == 0:
#             innersum = -1
#     if cc >= p.__len__():
#         break
#     distance.append(innersummul / innersum)

distance = []  # distance list distance[i] = (i.distance), where i is angle (i = 0..360)
dcounts = []
for i in range(720):
    distance.append(0)
    dcounts.append(0)

for i in range(p.__len__()):
    idx = math.floor(p[i][0]*2)
    distance[idx] = distance[idx]+p[i][1]
    dcounts[idx] = dcounts[idx]+1

for i in range(720):
    if dcounts[i] == 0:
        distance[i] = -1
    else:
        distance[i] = distance[i] / dcounts[i]

edges = []  # edges list
bounds = []  # objects bounds list
beta = 10  # experimental value for bounds!!!!!!!!!!!!!!!!!!!!! 20
neighbor = []  # distance between neighbor points

for i in range(distance.__len__()):
    neighbor.append((2*math.pi/720) * distance[i])
    bounds.append(neighbor[i] * beta)

for i in range(distance.__len__()-1):
    if fabs(distance[i + 1] - distance[i]) > bounds[i]:
        edges.append([i, distance[i]])
       # edges.append([i + 1, distance[i + 1]])
if fabs(distance[0] - distance[distance.__len__()-1]) > bounds[i]:
    edges.append([distance.__len__()-1, distance[distance.__len__()-1]])

bodies = []
for i in range(edges.__len__()-1):
    r1 = edges[i][1]
    r2 = edges[i+1][1]
    alpha1 = edges[i][0]/720*math.pi*2
    alpha2 = edges[i+1][0]/720*math.pi*2

    x1 = r1*math.cos(alpha1)
    y1 = r1*math.sin(alpha1)
    x2 = r2*math.cos(alpha2)
    y2 = r2*math.sin(alpha2)

    dist = math.sqrt((x2-x1)**2+(y2-y1)**2)

    b1 = (alpha1 + alpha2) / 2 / (2 * math.pi) * 360
    b2 = dist

    bodies.append([b1, b2])

r1 = edges[edges.__len__()-1][1]
r2 = edges[0][1]
alpha1 = edges[edges.__len__()-1][0]/720*math.pi*2
alpha2 = edges[0][0]/720*math.pi*2

x1 = r1*math.cos(alpha1)
y1 = r1*math.sin(alpha1)
x2 = r2*math.cos(alpha2)
y2 = r2*math.sin(alpha2)

dist = math.sqrt((x2-x1)**2+(y2-y1)**2)

b1 = (alpha1 + alpha2) / 2 / (2 * math.pi) * 360
b2 = dist

bodies.append([b1, b2])

legsize = 100
delta = 70

for i in range(bodies.__len__()):
    if (((legsize - delta) < bodies[i][1]) and (bodies[i][1] < (legsize + delta))):
        print(bodies[i])
