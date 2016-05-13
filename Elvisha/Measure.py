import win32api, win32con
import pygame, sys, os
from subprocess import Popen, PIPE
def setCursor(x,y):
    win32api.SetCursorPos((x,y));

def redirect_stdout():
    print "Redirecting stdout"
    #sys.stdout.flush() # <--- important when redirecting to files
    newstdout = os.dup(1)
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 1)
    os.close(devnull)
    sys.stdout = os.fdopen(newstdout, 'w')
    sys.stdout.flush()

if __name__ == '__main__':
    pygame.init();
    #setCursor(0,win32api.GetSystemMetrics(1))
    pygame.joystick.init();
    print pygame.joystick.get_count()
    Stick = pygame.joystick.Joystick(0);
    Stick.init();
    print Stick.get_numaxes()
    done = False
    move = 0;
    while done==False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.JOYAXISMOTION:
                if move==0:
                    #redirect_stdout();
                    #old_std_out = sys.stdout;
                    #print sys.stdout;
                    #sys.stdout = open('trash.txt','w');
                    #print sys.stdout;
                    x_init = Stick.get_axis(0);
                    y_init = Stick.get_axis(1);
                    #sys.stdout = old_std_out;
                    #print x_init,y_init
                move = move+1;
                #print "movement";
                #x = Stick.get_axis(0);
                #y = Stick.get_axis(1);
                [x,y] = [Stick.get_axis(0)-x_init,Stick.get_axis(1)-y_init];
                x_value = "x "+ str(x);
                y_value = "y "+ str(y);
                print x,y

    pygame.quit()
        
    
