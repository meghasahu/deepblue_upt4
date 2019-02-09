import zerosms
import requests
import json

URL = 'http://www.way2sms.com/api/v1/sendCampaign'

# get request
def sendPostRequest(apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  return requests.post(URL, req_params)

# get response
#message = "your generated code is random"
#response = sendPostRequest(URL, 'MW7X5CZ2ZM4TKD8QT7BM7A240215VGSV', 'TZELXM1CEZVHE20I', 'stage', 'receiver', '8286123583', message)
"""
  Note:-
    you must provide apikey, secretkey, usetype, mobile, senderid and message values
    and then requst to api
"""

