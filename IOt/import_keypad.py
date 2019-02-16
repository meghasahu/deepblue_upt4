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
        
        if(data=='*'):
            i=i-1
            ret = ret[:-1]
        if(data!='*' and data!='#'):
            ret = ret+str(data)
            i=i+1
        if(data=='#'):
            ret = ret+str("6")
            i=i+1
              
        time.sleep(0.25)
        print(str(ret))
    return ret
print(getfinaldata(10))