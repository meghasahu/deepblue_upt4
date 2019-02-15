from keypad import keypad
import time
from final_lcd import display_lcd


def getdata():
    kp = keypad()
    # Loop while waiting for a keypress
    digit = None
    while digit == None:
        digit = kp.getKey()
        kp.exit()
    return digit


def getfinaldata(n):
    ret = ''
    i = 0
    loopcount = n
    while i<loopcount:
        
    #for i in range(0,n):
        data = getdata()
        print(data)
        if(data=='*'):
            i=i-1
            ret = ret[:-1]
        if(data!='*'):
            ret = ret+str(data)
            i=i+1
        time.sleep(0.1)
        display_lcd(str(ret))
        
        print('i'+str(i))
    return ret
print(getfinaldata(10))