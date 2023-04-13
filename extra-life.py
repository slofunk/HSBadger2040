# This grabs info from the DonorDrive Extra life API and displays it on Badger 2040 W.
# This is an edit of the great example included in badgeros weather.py by Gadgetoid/Philip Howard. 
# Found here https://github.com/pimoroni/badger2040/blob/main/badger_os/examples/weather.py
# JCopeland April-3-20223

import badger2040
from badger2040 import WIDTH
import urequests
import jpegdec

URL = "https://extralife.donordrive.com/api/participants/000000"
# Display Setup
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(2)

jpeg = jpegdec.JPEG(display.display)

# Connects to the wireless network. Ensure you have entered your details in WIFI_CONFIG.py :).
display.connect()


def get_data():
    global sumDonations
    print(f"Requesting URL: {URL}")
    r = urequests.get(URL)
    # open the json data
    j = r.json()
    print("Data obtained!")
    print(j)

    # parse relevant data from JSON
    sumDonations = j["sumDonations"]
    
    r.close()

def draw_page():
    # Clear the display
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

    # Draw the page header
    display.set_font("bitmap6")
    display.set_pen(0)
    display.rectangle(0, 0, WIDTH, 20)
    display.set_pen(15)
    display.text("ExtraLife", 3, 4)
    display.set_pen(0)

    display.set_font("bitmap8")

    if sumDonations is not None:
        
        jpeg.open_file("/icons/extra-life.jpg")
        jpeg.decode(13, 40, jpegdec.JPEG_SCALE_HALF)
        display.set_pen(0)
        display.text(f"Total Raised: ${sumDonations}", int(WIDTH / 3), 28, WIDTH - 105, 2)
        
    else:
        display.set_pen(0)
        display.rectangle(0, 60, WIDTH, 25)
        display.set_pen(15)
        display.text("Unable to display fundraising info! Check your network settings in WIFI_CONFIG.py", 5, 65, WIDTH, 1)

    display.update()


get_data()
draw_page()

# Call halt in a loop, on battery this switches off power.
# On USB, the app will exit when A+C is pressed because the launcher picks that up.
while True:
    display.keepalive()
    display.halt()

