from pygaze.libscreen import Display, Screen
from pygaze.libinput import Keyboard
from libmpdev import *
import time
import math
import matplotlib.pyplot as plt


# create a Display to interact with the monitor
disp = Display()
 
# create a Screen to draw text on later
scr = Screen()
 
# create a Keyboard to catch key presses
kb = Keyboard(keylist=['escape'], timeout=1)
 
# create a MPy150 to communicate with a BIOPAC MP150
mp = MP150()

Y=[0];
t1 = time.time();
T=[0];

# set a starting value for key
key = None
# loop until a key is pressed
while key == None:

    # get a new sample from the MP150
    sample = mp.sample()
    t2 = time.time();
    T.append((t2-t1));
    Y.append(sample[0]);
    # use the first channel in a string (by using a wildcard)
    sampletext = "channel 0 = %.3f" % (sample[0])


    # Determine the background colour based on the sample
    # (this ranges between black and bright red).
    # Sample values usually are between 0 and 1. RGB values
    # are between 0 (no colour) and 255 (full colour). You
    # multiply the sample by 255 to get the colour value,
    # then you make sure it's an integer between 0 and 255.
    red = int(sample[0] * 255)
    # Make sure red is between 0 and 255.
    if red < 0:
        red = 0
    elif red > 255:
        red = 255
    # The other colour values will be 0
    green = 0
    blue = 0
    # Now set the background colour to the new colour.
    bgc = (red, green, blue)

    # Fill the Screen with the new background colour...
    scr.clear(colour=bgc)
    # ...and write the new sample text (white letters).
    scr.draw_text(text=sampletext, colour=(255,255,255), fontsize=100)

    # Now fill the Display with the updated Screen...
    disp.fill(scr)
    # ...and update the monitor!
    disp.show()

    # Don't forget to check if there is a keypress.
    key, presstime = kb.get_key()


# Close the connection with the MP150.
mp.close()
 
# End the experiment.
disp.close()
plt.plot(T,Y);
plt.show();
#print Y
