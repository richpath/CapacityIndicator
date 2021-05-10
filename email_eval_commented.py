from pythonping import ping # Used to ping an IP address to check network connection; will be included in next version
import email
import imaplib # Email and imaplib libraries used to check email and its contents
import time
import board
import neopixel # Board and neopixel libraries by Adafruit; used for controlling LED strips from Pi's GPIO pins
import datetime
from datetime import timedelta # Time, datetime and timedelta libraries used for formatting and evaluating dates and times
import random # Library used for generating random numbers

# Set the variable checkdate to yesterday
checkdate=(datetime.date.today()-datetime.timedelta(1)).strftime("%d-%b-%Y")

# Set pins on the Pi's GPIO for controlling LED strips
pixel_pin1 = board.D10
pixel_pin2 = board.D12
pixel_pin3 = board.D21

# Define the number of pixels in each strip
num_pixels1 = 118
num_pixels2 = 118
num_pixels3 = 1

# Set a list of colors to randomly choose from for the "multi" color effect demo
colors = [[255,0,0],[0,255,0],[0,0,255],[255,0,255],[255,255,0],[0,255,255],[255,100,0],[128,0,255],[0,128,255]]
# Set the RGB order of the particular WS2812b LED strips used that the Neopixel library should translate to
ORDER = neopixel.GRB
# Instantiate the three LED strips
pixels1 = neopixel.NeoPixel(
    pixel_pin1, num_pixels1, brightness=0.9, auto_write=False, pixel_order=ORDER
)
pixels2 = neopixel.NeoPixel(
    pixel_pin2, num_pixels2, brightness=0.9, auto_write=False, pixel_order=ORDER
)
pixels3 = neopixel.NeoPixel(
    pixel_pin3, num_pixels3, brightness=1, auto_write=False, pixel_order=ORDER
)

# The email code is based on example codes provided at the following sites: https://www.devdungeon.com/content/read-and-send-email-python; https://humberto.io/blog/sending-and-receiving-emails-with-python/

EMAIL = 'lighttest@rich-path.com'
# Password string will be replaced with an encrypted version instead of passed as plain text
PASSWORD = '*******'
SERVER = 'mail.rich-path.com'

# Instantiate imaplib mail object - connect to the server and go to its Inbox
mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('inbox')

# Create global variable for alert level text string
level=""

# Email is filtered to include only messages with the phrase "Capacity Level" in the subject and received since the date set in the checkdate variable (the previous day). Can also be filtered to include messages sent only from a specific email address.
status, data = mail.search(None, '(SUBJECT "Capacity Level" SINCE {0})'.format(checkdate))
# Create list to collect data for all emails kept after the filter
mail_ids = []
# Go through the list splitting its blocks of bytes and appending to the mail_ids list
for block in data:
    # The split function with no parameter transforms the text or bytes into a list using spaces as the separator:
    # a'1 2 3'.split() => [a'1', a'2', a'3']
    mail_ids += block.split()
if len(mail_ids) > 0:
    # Look at only the last email in the list and get that email message to extract its content
    # The content data in the '(RFC822)' format is a nested list with a tuple containing a header, content, and a closing byte b')'
    status, data = mail.fetch(mail_ids[-1], '(RFC822)')
    for response_part in data:
        if isinstance(response_part, tuple):
            # If the email does contain a tuple, get the content of its second element - the content
            message = email.message_from_bytes(response_part[1])
            # From the content data,  extract who sent the message (from), its subject text (subject), and the date it arrived (date)
            mail_from = message['from']
            mail_subject = message['subject']
            mail_date = message['date']
            # In the subject text string, if the word "Red" occurs, fill both left and right LED strips entirely with RGB red color in all four shapes
            if "Red" in mail_subject:
                level="RED"
                pixels1.fill((255,0,0))
                pixels2.fill((255,0,0))
            # Else, if the word "Orange" occurs in the subject text, fill left and right LED strips with RGB orange color only up through the bottom three shapes; keep top shape unlit/black
            elif "Orange" in mail_subject:
                level="ORANGE"
                for i in range(118):
                    if i<89:
                        pixels1[i] = (255,75,0)
                        pixels2[i] = (255,75,0)
                    else:
                        pixels1[i] = (0,0,0)
                        pixels2[i] = (0,0,0)
            # Else, if the word "Yellow" occurs in the subject text, fill left and right LED strips with RGB yellow color only up through the bottom two shapes; keep the upper two shapes unlit/black
            elif "Yellow" in mail_subject:
                level="YELLOW"
                for i in range(118):
                    if i<58:
                        pixels1[i] = (255,255,0)
                        pixels2[i] = (255,255,0)
                    else:
                        pixels1[i] = (0,0,0)
                        pixels2[i] = (0,0,0)
            # Else, if the word "Green" occurs in the subject text, fill left and right LED strips with RGB green color only in the bottom shape; keep the upper three shapes unlit/black
            elif "Green" in mail_subject:
                level="GREEN"
                for i in range(118):
                    if i<29:
                        pixels1[i] = (0,255,0)
                        pixels2[i] = (0,255,0)
                    else:
                        pixels1[i] = (0,0,0)
                        pixels2[i] = (0,0,0)
            # A "Multi" mode is included just for fun color demostration purposes - this chooses a random color from the previously defined 'colors' list and will set both LED strips to that color in all four of the shapes and then displays the updated colors.
            elif "Multi" in mail_subject:
                for l in range(5):
                    clr=random.randint(0,8)   
                    r = colors[clr][0]
                    g = colors[clr][1]
                    b = colors[clr][2]
                    pixels1.fill((r,g,b))
                    pixels2.fill((r,g,b))
                    pixels1.show()
                    pixels2.show()
                    time.sleep(1)
            # Write the text of the date and color alert level (from the email message that has been evaluated) to the "levellog" text file. This is a temporary operations logging procedure - this will likely not be used in the production version since the text file could continue to grow and fill up space on the Pi's SD card.
            with open('levellog.txt','a') as f:
                f.write(mail_date + ": " + level +"/n/r")
    # The show() command displays the latest color set for the LEDs
    pixels1.show()
    pixels2.show()
    # This loop blinks the single troubleshooting LED light on the controller box 10 times to indicate that the program has run successfully. Other troubleshooting color indications will be added in the next update.
    for i in range(10):
        pixels3.fill((0,0,0))
        pixels3.show()
        time.sleep(0.5)
        pixels3.fill((0,255,0))
        pixels3.show()