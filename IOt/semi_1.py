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
import spidev
from import_keypad import getfinaldata
from final_lcd import display_lcd
from t import turbidity
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN) #PIR
GPIO.setup(11, GPIO.IN)
GPIO.setup(10, GPIO.IN)

cred = credentials.Certificate('./deepblueupt-4-firebase-adminsdk-5rnmz-3cc90e6541.json')


firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://deepblueupt-4.firebaseio.com/'
})
ref = db.reference()
posts_ref = ref.child('users')
ref1 = db.reference()
usage_ref = ref1.child('usage')

thread_semaphore = [0,18,9]
time_of_each_thread = [0,0,0]
semaphore_one = [0,0,0] #to detect using stae
semaphore_two = [0,0,0] #changed in every state to keep track of the occupancy of a booth
pir_connected_to_GPIO_mapped = [4,11,10]
count=0
code=0
key = ['0','0','0']

def thread_function(thread_number,key):
    
    time_in = datetime.datetime.now()
    
    x = 0
    thread_semaphore[thread_number] = 1
    print('Booth Number - '+str(thread_number+1))
    while 1:
        
        ## Detecting if user is entering in allocated toilet
        if GPIO.input(pir_connected_to_GPIO_mapped[thread_number]) and semaphore_one[thread_number]==0:
            time_of_each_thread[thread_number] = time.time()
            semaphore_one[thread_number] = 1
            semaphore_two[thread_number] = 1
            print("Entered " + str(thread_number+1))
            
        #If user is using (turbidity part)
        elif GPIO.input(pir_connected_to_GPIO_mapped[thread_number])==0 and semaphore_two[thread_number]==1:
            semaphore_two[thread_number] = 0
            
            print("Using " + str(thread_number+1))
        
        #check var assign incentive
        elif GPIO.input(pir_connected_to_GPIO_mapped[thread_number]) == 0 and semaphore_one[thread_number]==1:
            x=turbidity()
            if x in range(4000,4500):
                x=x+1
                print(x)
                
        elif GPIO.input(pir_connected_to_GPIO_mapped[thread_number]) and semaphore_one[thread_number]==1 and semaphore_two[thread_number]==0:                
            semaphore_two[thread_number] = 0
            semaphore_one[thread_number] = 0
            time_consumed = time.time() - time_of_each_thread[thread_number]
            print("left " + str(thread_number+1))
            
            thread_semaphore[thread_number] = 0
            
            time_out = datetime.datetime.now()
            total = time_out-time_in
            time1 = str(time_in)
            time2 = str(time_out)
            time3 = str(total)
            if key != "abcd":
                new_usage_ref = usage_ref.push()
                new_usage_ref.set({
                    'key': key,
                    'time_in': time1,
                    'time_out' : time2,
                    'total_time_used' : time3,
                    #'incentives': incentives,
                })
                ## new code
                ## x = turbidity
                if x > 3:
                    streak_ref = ref.child('user_streak').child(key)
                    data = streak_ref.get()
                    lastused = datetime.datetime.now()
                    if data!= None:
                        yourdate = datetime.datetime.strptime(data['last_usage'], '%Y-%m-%d %H:%M:%S.%f')
                        if (lastused.date()-yourdate.date()).days == 1:
                            
                                # other than 5 10 15 etc
                            streak = data['streak']+1
                            streak_ref.set({
                                'streak':streak,
                                'last_usage':str(lastused),
                                'completedStreak':data['completedStreak'],
                                'total_incentives':data['total_incentives'],
                                })
                                
                        elif (lastused.date()-yourdate.date()).days != 0:
                            ## Not same day
                            ## streak break
                            streak_ref.set({
                                'streak':1,
                                'last_usage':str(lastused),
                                'completedStreak':data['completedStreak'],
                                'total_incentives':data['total_incentives'],
                                    })
                    else:
                        # new user
                        # first time using hence giving points 
                        streak_ref.set({
                                'streak':1,
                                'last_usage':str(lastused),
                                'completedStreak':0,
                                'total_incentives':5,
                                })
                
                
            ## Done
            
            return
            #pass
        time.sleep(2)

#t1=t2=t0=0


def assign(count,key):
    for x in thread_semaphore:
        if x==0:
            if count == 0 : #and thread_zero.is_alive()==False:
                thread_zero = threading.Thread(target=thread_function,args=(count,key[0],))
                #print(thread_zero.is_alive())
                thread_zero.start()
                break
            elif count ==  1: # and thread_one.is_alive()==False:
                thread_one = threading.Thread(target=thread_function,args=(count,key[1]))
                thread_one.start()
                break
            elif count ==  2:# and thread_two.is_alive()==False:
                thread_two = threading.Thread(target=thread_function,args=(count,key[2]))
                thread_two.start()
                break                    
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
    
    
    
    print(positionNumber)
    key[count] = posts_ref.push({
        'Template': name,
        'Code': code,
        'Phone number' : phone,
        'positionNumber' : positionNumber
    }).key
    message="Your code is "+str(code)+"."
    
    print('Finger enrolled successfully! Your Unique Code is %d '%(code))
    response = sendPostRequest('MW7X5CZ2ZM4TKD8QT7BM7A240215VGSV', 'TZELXM1CEZVHE20I', 'stage', phone, '8286123583', message)
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
    display_lcd("Welcome")
    while True:
        #lcd
        #lcd and keypad
        #display_lcd("1- New User\n2- Existing User")
        #option = int(getfinaldata(1))
        print("1- New User\n2- Existing User\n3- Direct User\n4- Cleaner")
        option = int(getfinaldata(1))
        print(option)
        #option = int(keypadCall(1))
        
            #display_lcd("2- Existing User")
        
        if option == 1:
            #display_lcd("1- New User")
            #phone=input("Enter phone number :")
            #display_lcd("Enter phone number :")
            print("Enter phone number : ")
            #phone = getfinaldata(10)
            phone = '9769577063'
            #phone = keypadCall(10)
            code = randint(999,9999)
            print("Your Code is \n"+str(code))
            #display_lcd("your code is \n"+str(code))
            newuser(phone, int(code), f)
            
        elif option == 2 :
            #display_lcd("Enter Your Code:")
            #code = getfinaldata(4)
            #display_lcd(code)
            print("Enter your code : ")
            code = int(getfinaldata(4))
            print(code)
            #code = int(input())
            checkuser(code, f)
            
        elif option == 3 :
            key[count] = "abcd"
            assign(count,key)
            
        elif option == 4 :
            #display_lcd("1- Clean Booth\n2- Free Booth")
            print("1- Clean Booth\n2- Free Booth\n")
            option1= int(getfinaldata(1))
            print(option1)
            #display_lcd("Enter Booth Number")
            print("Enter Booth Number :")
            option2=int(getfinaldata(1))
            print(option2)
            if option1==1:
                thread_semaphore[option2-1] = 1
            if option1==2:
                thread_semaphore[option2-1] = 0
        else:
            print("hey")
            continue
if __name__=="__main__":
    main()