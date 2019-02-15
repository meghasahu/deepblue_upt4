import threading
import time
import firebase_admin
from pyfingerprint.pyfingerprint import PyFingerprint
from firebase_admin import credentials
from firebase_admin import db
import pymysql.cursors
from random import randint
import RPi.GPIO as GPIO
from sms import sendPostRequest
import datetime

from keytest import keypadCall
GPIO.setmode(GPIO.BCM)
#GPIO.setup(21, GPIO.IN) #PIR
#GPIO.setup(11, GPIO.IN)
#GPIO.setup(10, GPIO.IN)

cred = credentials.Certificate('./deepblueupt-4-firebase-adminsdk-5rnmz-3cc90e6541.json')


firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://deepblueupt-4.firebaseio.com/'
})
ref = db.reference()
posts_ref = ref.child('users')
ref1 = db.reference()
usage_ref = ref1.child('usage')

thread_semaphore = [0,7,0]
time_of_each_thread = [0,0,0]
semaphore_one = [0,0,0] #to detect using stae
semaphore_two = [0,0,0] #changed in every state to keep track of the occupancy of a booth
pir_connected_to_GPIO_mapped = [21,11,10]
count=0
code=0
key = ['0','0','0']

def thread_function(thread_number,key):
    
    time_in = datetime.datetime.now()
        
    
    thread_semaphore[thread_number] = 1
    print('Booth Number - '+str(thread_number+1))
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
            print("Time consumed : " + str(time_consumed))
            if(time_consumed<10):
                incentives = 0
                print("Fake usage")
            if time_consumed>10 and time_consumed<20:
                incentives = 5
                print("Gained 5 points")
            if time_consumed>20:
                incentives = 10
                print("Gained 10 points")
            thread_semaphore[thread_number] = 0
            '''if thread_number==0:
                thread_zero._stop()
            elif thread_number==1:
                thread_one._stop()
            elif thread_number==2:
                thread_two._stop()'''
            time_out = datetime.datetime.now()
            total = time_out-time_in
            time1 = str(time_in)
            time2 = str(time_out)
            time3 = str(total)
            new_usage_ref = usage_ref.push()
            new_usage_ref.set({
                'key': key,
                'time_in': time1,
                'time_out' : time2,
                'total_time_used' : time3,
                'incentives': incentives,
            })
            return
            
        #while GPIO.input(pir_connected_to_GPIO_mapped[thread_number]) and semaphore_two[thread_number]==1:
            #print('Infinite')
            #pass
        time.sleep(2)

#t1=t2=t0=0
'''thread_zero = threading.Thread(target=thread_function,args=(count,))
thread_one = threading.Thread(target=thread_function,args=(count,))
thread_two = threading.Thread(target=thread_function,args=(count,))'''

def assign(count,key):
    for x in thread_semaphore:
        if x==0:
            if count == 0 : #and thread_zero.is_alive()==False:
                thread_zero = threading.Thread(target=thread_function,args=(count,key[0],))
                #print(thread_zero.is_alive())
                thread_zero.start()
                break
            '''elif count ==  1: # and thread_one.is_alive()==False:
                thread_one = threading.Thread(target=thread_function,args=(count,key[1]))
                thread_one.start()
                break
            elif count ==  2:# and thread_two.is_alive()==False:
                thread_two = threading.Thread(target=thread_function,args=(count,key[2]))
                thread_two.start()
                break'''                    
        count = count + 1
        if count == len(thread_semaphore):
            print("All Booths Occupied")
    return(count)
            
        
def newuser(phone, code, f):
    
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)
    print('Remove finger...')
    f.createTemplate()
    positionNumber = f.storeTemplate()
    name = f.downloadCharacteristics()
    
    #f.loadTemplate(1, 0x02)
    #char_store = str(f.downloadCharacteristics(0x02))
    #name= char_store.translate(None, ',[]')
    print(name)
    
    new_post_ref = posts_ref.push()
    new_post_ref.set({
        'Template': name,
        'Code': code,
        'Phone number' : phone,
        'positionNumber': positionNumber,
    })
    message="Your code is "+str(code)+"."
    
    print('Finger enrolled successfully! Your Unique Code is %d '%(code))
    response = sendPostRequest('MW7X5CZ2ZM4TKD8QT7BM7A240215VGSV', 'TZELXM1CEZVHE20I', 'stage', phone, '8286123583', message)
    key[count] = new_post_ref.push().key()
    assign(count,key)
    #snapshot = posts_ref.order_by_child('Code').equal_to(code).get()
    
    
        
def checkuser(code,f):
    
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)
    print('Remove finger...')
    
    #fetch template having that code
    snapshot = posts_ref.order_by_child("Code").equal_to(code).get() #temp query
    if snapshot:
        for i in snapshot.items():
            key[count] = i[0]
        for i,j in snapshot.items():
            name= j['Template']
            print(name)
            f.uploadCharacteristics(0x02,name)
            
        
            if ( f.compareCharacteristics() != 0 ):
                #fin_check=1
                print("user found")
                assign(count,key)
                break
            else :
                print("User not found")
                break
                
                #print "Fingers do not match"
            #time.sleep(2)
        
    else:
        print("Code invalid")
    return
    
def finger_initialize():
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        if( f.verifyPassword() == False ):
            print("hey")
            raise ValueError('The given fingerprint sensor password is wrong!')
        return f

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)
## Tries to initialize the sensor
    
def main():
    
    f = finger_initialize()
    print("Welcome")
    while True:
        #option = input("Enter 1 for new user and 2 for already registered user : ")
        print("Enter 1 for new user and 2 for already registered user : ")
        #option = int(input("Enter a number: "))
        option = int(keypadCall(1))
        print("option")
        print(option)
        if option == 1:
            #phone=input("Enter phone number :")
            print("Enter phone number :")
            #phone = int(input())
            phone = keypadCall(10)
            code = randint(999,9999)
            print(code)
            newuser(phone, code, f)
            
        elif option==2 :
            code=input("Enter your code : ")
            print("Enter your code :")
            #code = int(input())
            checkuser(code, f)
        else:
            continue
if __name__=="__main__":
    main()