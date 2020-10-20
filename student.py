#!/usr/bin python3
from collections import OrderedDict
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
        self.RIGHT_DEFAULT = 85
        self.SAFE_DISTANCE = 200 #<-- change this number as needed
        self.CLOSE_DISTANCE = 40
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
        for _ in range(2):
            self.side_to_side()
            self.moon_walk()
            self.forward_shuffle()
            self.square()
            self.shimmy()
            self.sprinkler()
            self.twirl_around()
            self.moon_walk()
            self.wheelie()
            for _ in range(2):
                self.swerve_right()
                self.swerve_left()     
        self.stop()

# Brennen's wheelie method
    def wheelie(self):
        """ Leaps forward / almost like a wheelie """
        for _ in range(4):
            self.fwd(right=90, left=90)
            time.sleep(.5)
            self.servo(1000)
            time.sleep(.1)
            self.servo(2000)
            time.sleep(.1)
            self.fwd(right=-100, left=-100)
            time.sleep(.1)
            self.servo(-1000)
        self.stop()

    def square(self):
        """ Goes in a four corner direction """
        for _ in range(4):
            self.forward_shuffle()
            self.turn_by_deg(360)
    
    def side_to_side(self):
        """ Moves head left and right """
        for _ in range(4):
            self.servo(1000)
            time.sleep(.3)
            self.servo(2000)
            time.sleep(.3)
            self.stop()

    def safe_to_dance(self):
        """ Does a 360 distance check and returns true if safe """
        # check for all fail/early-termination conditions
        for _ in range(4):
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
        for x in range(1):
            self.servo(1000) # moving the head to the right
            self.veer_left()
            time.sleep(.5)
            self.servo(2000) # moving the head to the left 
            time.sleep(.5) #giving it time to process what is happening and move
            self.servo(1000)
            self.veer_right()
            time.sleep(.5)
            self.servo(2000)
            time.sleep(.5)
            self.stop()

    def veer_left(self):
        """ Shifting Lower Body to the Left"""
        self.fwd(left=90, right=50)
    
    def veer_right(self):
        """ Shifting Lower Body to the Right """
        self.fwd(left=50, right=90)

    def sprinkler(self):
        """ Stops at each point and shakes head """
        for angle in range(20, 200, 20):
            self.turn_by_deg(angle)
            time.sleep(.1)
            self.servo(1000)
            self.servo(2000)
            time.sleep(.1)
        self.stop()
   
    def forward_shuffle(self):
        """ Walk Forward"""
        for x in range(1):
            self.deg_fwd(180)
            time.sleep(.01)

    
    def moon_walk(self):
        """ Walking Backward """
        for _ in range(2):
            self.back()
            time.sleep(.5)

    def twirl_around(self):
        """Spinning around in a complete circle"""
        self.left(primary=100, counter=-100)
        time.sleep(5)
        self.stop()

    def swerve_right(self):
        """ Turns to the right in a circular position"""
        self.right() 
        time.sleep(.95) 
        self.servo(1000) 
        time.sleep(.2) 
        self.servo(2000)
    
    def swerve_left(self):
        """ Turns to the left in a circular position"""
        self.left()
        time.sleep(.95)
        self.servo(2000)
        time.sleep(.2)
        self.servo(1000)

    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 50):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()
        # sort the scan data for easier analysis
        self.scan_data = OrderedDict(sorted(self.scan_data.items()))
    def right_or_left(self):
        """ Should I turn left or right? Returns a 'r' or 'l' based on scan data """
        self.scan()

        right_sum = 0
        right_avg = 0
        left_sum = 0
        left_avg = 0


        # analyze scan results
        for angle in self.scan_data:
            # average up the distances on the right side
            if angle < self.MIDPOINT:
                right_sum += self.scan_data[angle]
                right_avg += 1
            else:
                left_sum += self.scan_data[angle]
                left_avg += 1

        # calculate averages
        left_avg = left_sum / left_avg
        right_avg = right_sum / right_avg

        if left_avg > right_avg:
            return 'l'
        else:
            return 'r'

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        see_an_object = False
        for angle in range(0, 360, 90):
            self.turn_by_deg(angle)
            # do a scan of the area in front of the robot
            self.scan()
            # FIGURE OUT HOW MANY OBSTACLES THERE WERE
            see_an_object = False
            count = 0
            for angle in self.scan_data:
                dist = self.scan_data[angle]
                if dist < self.SAFE_DISTANCE and not see_an_object:
                    see_an_object = True
                    count += 1
                    print("~~~~ I SEE SOMETHING!!! ~~~~")
                elif dist > self.SAFE_DISTANCE and see_an_object:
                    see_an_object = False
                    print ("I guess the object ended")


                print("ANGLE: %d | DIST: %d" % (angle, dist))
        print("\nI saw %d objects" % count)
            

    def quick_check(self):
        """ Moves the servo to three angles and performs a distance check """
        #Write a better docustring
        #loop three times and move the servo
        for ang in range(self.MIDPOINT - 200, self.MIDPOINT + 201, 200):
            self.servo(ang)
            time.sleep(.1)
            if self.read_distance() < self.SAFE_DISTANCE:
                return False
        # if the three-part check didn't freak out 
        return True
# trying to make it move in a circle to check all primeters before going backwards
    def turn_left_until_clear(self):
        """ Rotate right until no obstacle is seen """
        print("----TURNING UNTIL CLEAR!!!----")
        # make sure we're looking straight
        self.servo(self.MIDPOINT)
        # so long as we see something close, keep turning left
        while self.read_distance() < self.SAFE_DISTANCE + 100:
            self.left(primary=50, counter=-50)
            time.sleep(.05)
        # stop motion before we end the method
        self.stop()
        self.turn_by_deg(-25)
        

    def turn_right_until_clear(self):
        """ Rotate right until no obstacle is seen """
        print("----TURNING UNTIL CLEAR!!!----")
        # make sure we're looking straight
        self.servo(self.MIDPOINT)
        # so long as we see something close, keep turning left
        while self.read_distance() < self.SAFE_DISTANCE + 100:
            self.right(primary=50, counter=-50)
            time.sleep(.05)
        # stop motion before we end the method
        self.stop
        self.turn_by_deg(25)
        

    def nav(self):
        """  Auto-pilot program """
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # 
        exit_angle = self.get_heading()
        # because I've written down the exit's angle, at anytime  I can use:
        # self.turn_to_deg(exit_ang)
        turn_count = 0
        while True:
            if not self.quick_check():
                turn_count += 1
                self.stop()
                self.back()
                time.sleep(1)
                self.stop()
                if turn_count > 3 and turn_count % 4 == 0:
                    self.turn_to_deg(exit_angle)
                elif 'l' in self.right_or_left():
                    self.turn_left_until_clear()
                else:
                    self.turn_right_until_clear()
                turn_count += 1

            else:
                self.fwd(left = 100, right = 100)
    
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
