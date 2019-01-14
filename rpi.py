import threading
import time
from pyfingerprint.pyfingerprint import PyFingerprint
import pymysql.cursors
from random import randint
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN) #PIR
GPIO.setup(11, GPIO.IN)
GPIO.setup(10, GPIO.IN)

cnx=pymysql.connect(user='phpmyadmin',password='raspberry',host='localhost',database='iotproject')       # connect to MySql database
cur=cnx.cursor()

thread_semaphore = [0,7,0]
time_of_each_thread = [0,0,0]
semaphore_one = [0,0,0]
semaphore_two = [0,0,0]
pir_connected_to_GPIO_mapped = [7,11,10]


def thread_function(thread_number):
    thread_semaphore[thread_number] = 1
    print('Booth Number - ')
    print(thread_number+1)
    while 1:
        if GPIO.input(pir_connected_to_GPIO_mapped[thread_number]) and semaphore_one[thread_number]==0:
            time_of_each_thread[thread_number] = time.time()
            semaphore_one[thread_number] = 1
            semaphore_two[thread_number] = 1
            print("Entered " + str(thread_number+1))
            
        elif (GPIO.input(pir_connected_to_GPIO_mapped[thread_number])==0) and semaphore_two[thread_number]==1:
            semaphore_two[thread_number] = 0
            print("Using " + str(thread_number+1))
            
        elif GPIO.input(pir_connected_to_GPIO_mapped[thread_number]) and semaphore_one[thread_number]==1 and semaphore_two[thread_number]==0:
            semaphore_two[thread_number] = 0
            semaphore_one[thread_number] = 0
            time_consumed = time.time() - time_of_each_thread[thread_number]
            print("left " + str(thread_number+1))
            thread_semaphore[thread_number] = 0
            return
            
            
        #while GPIO.input(pir_connected_to_GPIO_mapped[thread_number]) and semaphore_two[thread_number]==1:
            #print('Infinite')
            #pass
    time.sleep(15)
        
## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    if( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)




while 1:
    
    count_one = 0
    for y in thread_semaphore:
        if y==3:
            if count_one == 0:
                thread_zero.stop()
                break
            elif count_one ==  1:
                thread_one.stop()
                break
            elif count_two ==  2:
                thread_two.stop()
                break
            
        count_one = count_one + 1
      
    try:
        
        ##print(f.uploadCharacteristics())

    
        
    
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)
        
        time.sleep(2)
        ## Creates a template
        f.createTemplate()
        name = str(f.downloadCharacteristics())
        
        #f.loadTemplate(1, 0x02)
        #char_store = str (f.downloadCharacteristics(0x02))
        #name= char_store.translate(None, ',[]')
        
        query = "select * from user where finger = "+'"'+name+'"'
        cur.execute(query)   # update database
        result = cur.fetchone()
        if(result):
        #user found login allocate washroom
            
            print('user found')
            count = 0
            for x in thread_semaphore:
                if x==0:
                    if count == 0:
                        thread_zero = threading.Thread(target=thread_function,args=(count,))
                        thread_zero.start()
                        break
                    elif count ==  1:
                        thread_one = threading.Thread(target=thread_function,args=(count,))
                        thread_one.start()
                        break
                    elif count ==  2:
                        thread_two = threading.Thread(target=thread_function,args=(count,))
                        thread_two.start()
                        break
                    
                    
                count = count + 1
                if count == len(thread_semaphore):
                    print("All Booths Occupied")
        
        else:
        #user not found so insert finger print and then display generated user id to user
            print("new user")
            random = randint(999,9999)
            print(random)
            cur.execute("insert into user(finger,code) values('%s','%d')" %(name,random) )     # adding new finger print to db and generating user id
            cnx.commit()
         
    except Exception as e:
        pass
