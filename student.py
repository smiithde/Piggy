#!/usr/bin python3
from teacher import PiggyParent
import sys
import time

class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 80
        self.RIGHT_DEFAULT = 80
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)
        self.load_defaults()
        
    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        
    def menu(self):
        #NEED Docstring Comments for all of the Dance moves must be specific
        ## Has to summerize what it does
        ###Also explain everything that is happening and leave comments for everything 
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "s": ("Shy", self.shy),
                "f": ("Follow", self.follow),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''

    def dance(self):
        """A higher-ordered algorithm to make your robot dance"""

        if not self.safe_to_dance():
            return False #SHUT THE DANCE DOWN
        # TODO: make up own dance         # self.forward_shuffle()
        # lower-ordered example....
        for x in range(2):
            self.forward_shuffle()
            self.shimmy()
            self.twirl_around()
            self.swerve_right()
            self.swerve_left()
            self.swerve_right()
            self.swerve_left()
        # TODO: combine swerves and make it go for 3 times
        # TODO: lessen distance for forward 
        self.stop()
        

    def safe_to_dance(self):
        """ Does a 360 distance check and returns true if safe """
        # check for all fail/early-termination conditions
        for x in range(4):
            if self.read_distance() < 300:
                print("NOT SAFE TO DANCE!")
                return False
            else:
                self.turn_by_deg(90)
        #after all checks have been down. We deduce it's safe
        print ("SAFE TO DANCE, RAMSTEIN!") 
        return True 

    def shake(self):
        """ Another example move """
        self.deg_fwd(720)
        self.stop()

    def shimmy(self):
        """ Shaking both the head and body in opposite directions while moving forward"""
        for x in range(2):
            self.servo(1000) # moving the head to the right
            self.veer_left()
            time.sleep(.1)
            self.servo(2000) # moving the head to the left 
            time.sleep(.1) #giving it time to process what is happening and move
            self.servo(1000)
            self.veer_right()
            self.servo(2000)
            time.sleep(1)
            self.back()
            time.sleep(.01)
        self.stop()

    def veer_left(self):
        """ Shifting Lower Body to the Left"""
        self.fwd(left=90, right=50)
    
    def veer_right(self):
        """ Shifting Lower Body to the Right """
        self.fwd(left=50, right=90)
   
    def forward_shuffle(self):
        """ Walk Forward"""
        for x in range(2):
            self.fwd()
            time.sleep(.01)
            self.stop()

    def twirl_around(self):
        """Spinning around in a complete circle"""
        self.left(primary=100, counter=-100)
        time.sleep(5)
        self.stop()

    def swerve_right(self):
        """ Turns to the right in a circular position"""
        self.right() 
        time.sleep(.95) 
        self.stop()
        self.servo(1000) 
        time.sleep(.2) 
        self.servo(2000)
        
    
    def swerve_left(self):
        """ Turns to the left in a circular position"""
        self.left()
        time.sleep(.95)
        self.stop()
        self.servo(2000)
        time.sleep(.2)
        self.servo(1000)

    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 3):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        pass

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        
        # TODO: build self.quick_check() that does a fast, 3-part check instead of read_distance
        while self.read_distance() > 250:  # TODO: fix this magic number
            self.fwd()
            time.sleep(.01)
        self.stop()
        # TODO: scan so we can decide left or right
        # TODO: average the right side of the scan dict
        # TODO: average the left side of the scan dict
        


###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
