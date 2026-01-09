#PortSwigger BlindSQL with Conditional Responses
- open burp
- use burp web search to intercept request.
- the website uses tracking cookies for analytics.
- vulnerability to exploit is the tracking cookie id.
- The web app performs an SQL query based on the cookie ID
- The only thing we will work with is website behavior, a welcome back message.
- Database has a table called users..with columns: username and password.
- Find password to administrator user

#How:
- After opening burp, click open browser option.
- Paste the lab URL on the browser.
- Refresh the page, and the website's request appears on the Proxy Intercept tab
- Right click the request, send it to repeater.

#Boolean Conditionals
- These conditionals always return TRUE or False.
- In the Tracking cookie Id, inject the condition ' AND 1='1'-- then click send
- ' AND 1='1'-- returns a welcome back message in the RENDER SECTION.
- Inject again with ' AND 1='2'-- and click send. No welcome message appears.

#Confirm a Table Exists
- Using the cookie tracking ID, we can check if a table exists by sending an arbitrary character. 
- The arbitrary character we will use is 'a'
- So inject ' AND (SELECT 'a' FROM users LIMIT 1) = 'a'--
- The query check selects the letter 'a' from users and limits it to just one 'a'. And the result should be ='a'--
- If the welcome message appears ON RENDER SECTION, then that means our table exists, and it's called users.
- if we entered ‘usersss’ instead of users, then the welcome back message won't appear, and that means a table called usersss doesn't exist.

#Confirm a user called Administrator exists
- Now we know a table called users exists.
- To check if a user with the username Administrator exists, we inject the following:
   ' AND (SELECT 'a' FROM users WHERE username ='administrator') = 'a'--
- Click send, and if the welcome message appears, then administrator exists.
- If we entered 'administratorrrr' then the welcome back message wouldn't appear, meaning that user doesn't exist.

#Arbitrary Character
- An arbitrary character, like 'a', is used to test the database.
- So if 'a' exists, the page shows a welcome back message.
- When the message appears, it means the user called administrator exists.
- In short, you are asking the database: IF THERE'S A USER CALLED ADMINISTRATOR, RETURN THE LETTER 'a'
- When it's returned, the page behaves normally: like showing a welcome back message.

#Script Needed to determine password length and extract password.
- Now we know the administrator exists, so now we need a script to:
  * Determine password length
  * Extract the exact administrator password string.

#Python Script for Solving BlindSQL with Conditionals
- We will import the following modules: requests, string, time.
- The requests module helps us interact with the web application using the GET method.
- The string module will be useful for extracting and manipulating strings (password is a string)
- The time module will help us trigger small time delays. Therefore, the server will not be overwhelmed with processing multiple requests.

#Input fields
- After importing the three modules, we will create two input fields
- The first input field is for the target_url.
- The second input field will carry TrackingId inside tracking_id variable
- Below these two inputs, we will add a dictionary called cookies, with key-value pairs {'TrackingId': tracking_id}

#Sending request with original cookie
- Send a requests.get and include the target_url plus the cookies dictionary.
- Store the response in an object 'r'
- Print r.status_code to check status code response from server.
- Print r.text to see the text response.
- Use if condition to check for "Welcome back!" in r.text
- If there's a "Welcome back!" print "Condition is TRUE", else print "Condition is FALSE"

-  NB: This request is important because it lets us test the server first before adding a payload.

#Sending request with modified cookie
- The modified cookie is a cookie that has a payload.
- We begin by defining a payload_injection function that takes the (payload) parameter 
- Take the tracking_id and add payload to it, then store it in a modified_cookie variable.
- Send a request.get with target_url and the cookies dictionary.
- Inside the cookies dictionary, change the value to modified_cookie. Leave the 'TrackingId' key as is.
- Return the response of the function. The returned value will be used by the program elsewhere.
- The payload will be defined later inside the loop.

#Checking the response
- In this section, we define a check_response function that checks (response) parameter.
- We return True if there is a "Welcome back!" message in response.text

#The for loop for checking Password Length
- This section will check the Length (L) of password in the range (1, 25)
- Define the payload as an f string
- The payload will use LENGTH function to check if password length is greater than > {L}
- Trigger a small time delay with time.sleep(3)
- Call the payload_injection(payload) function, and store server feedback in the response variable.
- Call  check_response(response) function to return True if there’s a "Welcome back!" message
- Outside the loop, Define an empty string str() and store it inside a password variable.
- This empty string will be useful in the next loop.

#The second loop for checking password characters.
- Define a for loop that checks every char position in the range 1-25:
for char in range (1, 25 + 1)
- Inside the loop, define another for loop that checks every character_guess in string.ascii_letters + string.digits
  * This new loop used the string variable.
  * The string checks each character as uppercase/lowercase(string.ascii_letters) and digits(string.digits)

- Define payload in an f string
- This payload will use SQL’s substring function.
  * Substring function lets us extract portions of a string, in this case, a password string.
  * The syntax for substring is: SUBSTRING(value, start_position, length)
  * Start_position dictates where to begin and length dictates how many string characters to take
  * For our lab, we will use SUBSTRING(password, {char}, 1)
  * Finally, the payload will compare the results and see if it’s equal to '{character_guess}'


- Still inside the second loop, call the payload_injection(payload) function and store feedback in response variable
- Next, call the check_response(response) function as an if condition.
- If the condition returns True, then the character_guess is stored inside a password variable
- Print password, trigger a small time delay of 0.5 seconds, and break the if condition.
- Finally the challenge was complete and the password was revealed.



































	



