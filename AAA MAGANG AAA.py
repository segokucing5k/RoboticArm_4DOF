import serial
import time
import math
import array as pretheta

t1 = 3000
pi = math.pi
l1 = 12
l2 = 10
l3 = 10
l4 = 14.5
l5 = 5

passed = 0
placed_deg = None
open = False
tumpuk = 0

ser = serial.Serial('COM13', 9600)
angle = 0

def kirim(theta):
    global jarak
    command = theta[0], theta[1], theta[2], theta[3], theta[4]
    commandString = str(round(command[0])) + ";" + str(round(command[1])) + ";" + str(round(command[2])) + ";" + str(round(command[3])) + ";" + str(round(command[4])) + "\n"

    ser.write(commandString.encode())

    dataRaw = ser.readline()
    data = dataRaw.split(b'-')
    print('{0}-{1}-{2}-{3}-{4}-{5}'.format(int(data[0]), int(data[1]), int(data[2]), int(data[3]),int(data[4]), int(data[5])))

    jarak = int (data[5].decode().split('\n')[0])
    print ('jarak = ', jarak, 'cm')

    time.sleep(1)

def degtorad(deg):
    rad = (deg * pi / 180)
    return rad

def radtodeg(rad):
    deg = rad * 180 / pi
    return deg

def duty_cycle(deg):
    value = deg/180*4000 + 1000
    return value
    
def pick_object(distance):
    global l1, l2, l3, l4, t1, t2, t3, t4, t5, a, b, c, base
    x = distance - 4
    print ("x :", x)
    c = math.sqrt(l1 * l1 + x * x)
    print ("c :", c)
    c2 = radtodeg(math.acos((c * c - (l2 * l2 + l3 * l3 )) / (2 * l2 * l3)))
    a2 = (180 - c2) / 2
    b2 = a2
    b1 = radtodeg(math.asin((l1 * math.sin(0.5)) / c)) 
    a1 = 180 - 90 - b1
    a = 5000 - duty_cycle(a1 + a2)
    b = duty_cycle(c2)
    c = duty_cycle(180 - b1 - b2)
    jumlah = t2+t3+t4
    sum2 = a2 + b2 + c2
    sum1 = a1 + b1 + 90

    print("setelah invers dengan jarak 3 ||  x 17,5 :", t1, a, b, c, t5, jumlah)
    print("sudut sudut :", a1, b1, a2, b2, c2, sum1, sum2)

    theta = [base, a, b, c, t5]
    kirim(theta)
    t5 -= 2000
    theta = [base, a, b, c, t5]
    kirim(theta)
    move()

def search_object():
    global placed_deg, t1, t2, t3, t4, t5, theta, base
    clockwise = True
    Distance = jarak 
    base = t1
    print(base, " base")
    while Distance > 18:
        if clockwise == False and base < 5000:
            print("passed 2")
            base += 50
            theta = [base, t2, t3, t4, t5]
            kirim(theta)
            Distance = jarak
        elif clockwise == True and base > 1000:
            print(base, " base")
            base -= 50
            print("passed 3")
            theta = [base, t2, t3, t4, t5]
            kirim(theta)
            Distance = jarak
        if base == 5000 or base == 1000:
            clockwise = not clockwise
#    placed_deg = base
    t1 = base
#    gripper(True)
    pick_object(Distance)

def robot_start():
    global t1, t2, t3, t4, t5, jarak
    t1 = duty_cycle(90) #awalnya 90
    t2 = duty_cycle(20)
    t3 = duty_cycle(100)
    t4 = duty_cycle(120)
    t5 = duty_cycle(90)
    print("robot start degree :", t1, t2, t3, t4, t5)
    theta = [t1, t2, t3, t4, t5]
    kirim(theta)
    search_object()

def move():
    global t1, t2, t3, t4, passed, base, a, b, c, t5, tumpuk, base0, a0, b0, c0, Distance
    a += duty_cycle(10) 
    print("a : ", a)
    theta = [base, a, b, c, t5]
    kirim(theta) 
    print("base : ", base)
    if tumpuk > 0 :
        base = base0
        theta = [base, a, b, c, t5]
        kirim(theta)
        a = a0
        b = b0
        c = c0
        while a >  duty_cycle(10) + 300 + passed: 
            a -= 100
            theta = [base, a, b, c, t5]
            kirim(theta) 
    else:
        if base > 2000:
            base -= 1200
        else:
            base += 1200
            theta = [base, a, b, c, t5]
            kirim(theta) 
        a0 = a 
        b0 = b
        c0 = c
        while a >  duty_cycle(10) + 300 + passed: 
            a -= 100
            theta = [base, a, b, c, t5]
            kirim(theta)     
    t5 += 3000 
    theta = [base, a, b, c, t5]
    kirim(theta) 
    passed += 250
    tumpuk += 1
    base0 = base
    theta = [duty_cycle(90), duty_cycle(20), duty_cycle(100), duty_cycle(120), duty_cycle(90)]
    kirim(theta) 
    time.sleep(2)
    
while True:
    robot_start()
