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
        
        self.LEFT_DEFAULT = 96.5
        self.RIGHT_DEFAULT = 100
        self.exit_heading = 0
        self.corner_count = 0
        self.SAFE_DIST = 350
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?
        self.load_defaults()
        

    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
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
        # HIGHER - ORDERED
        # check to see it is safe to dance
        if not self.safe_to_dance():
            print("Not enough room to safely dance")
            return
        else:
            print("Lets dance.")
        for x in range(3):
            self.chacha()
            self.spin()
            self.dab()
            self.moonwalk()

    def safe_to_dance(self):
        """ Does a 360 distance check to see if dance floor is clear """
        for x in range(4):
            for ang in range(self.MIDPOINT-400, self.MIDPOINT+400, 100):
                self.servo(ang)
                time.sleep(.1)
                if self.read_distance() < 250:
                    return False
            self.turn_by_deg(90)
        return True

    

    def chacha(self):
        """back and forth movement"""
        self.turn_by_deg(-30)
        self.turn_by_deg(60)
        self.turn_by_deg(-60)
        self.turn_by_deg(60)
        self.turn_by_deg(-60)
        self.turn_by_deg(60)
        self.turn_by_deg(-60)
        self.turn_by_deg(60)
        self.turn_by_deg(-60)
        self.turn_by_deg(30)


    def spin(self):
        """fast spin in a circle, turns back"""
        self.turn_by_deg(180)
        self.turn_by_deg(180)
        self.turn_by_deg(-180)
        self.turn_by_deg(-180)

    def dab(self):
        """head moves right while bot moves left, then goes back to original place"""
        self.right()
        self.servo(2000)
        time.sleep(.25)
        self.stop()
        self.left()
        self.servo(1500)
        time.sleep(.25)
        self.stop()


    def moonwalk(self):
        """moves backwards alternating power between left and right wheels"""
        self.back()
        time.sleep(1)
        self.turn_by_deg(-30)
        self.back()
        time.sleep(1)
        self.turn_by_deg(60)
        self.back()
        time.sleep(1)
        self.stop()



    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 150):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """ Does a 360 scan and returns the number of obstacles it sees"""
        found_something = False #trigger
        trigger_distance = 250
        count = 0
        starting_position = self.get_heading() #write down starting position
        self.right(primary=60, counter=-60)
        while self.get_heading() != starting_position:
            if self.read_distance() < trigger_distance and not found_something:
                found_something = True
                count += 1
                print("\n FOUND SOMETHING!!!! \n")
            elif self.read_distance() > trigger_distance and found_something:
                found_something = False 
                print("I have a clear view. Resetting my counter")
        self.stop()
        print("I found this many things: %d" % count)
        return count 


    def quick_check(self):
        # 3 quick checks
        for ang in range(self.MIDPOINT-150, self.MIDPOINT+151, 150):
            self.servo(ang)
            if self.read_distance() < self.SAFE_DIST:
                return False

        # if I get to the end, i found nothing dangerous
        return True

    def nav(self):
            "robot able to navigate by checking surroundings"
            # assuming that we are facing the exit at the start
            self.exit_heading = self.get_heading()
            
            print("-----------! NAVIGATION ACTIVATED !------------\n")
            print("-------- [ Press CTRL + C to stop me ] --------\n")
            print("-------------! EXIT IS AT %d !---------------\n" % self.exit_heading) 
            self.corner_count = 0
            self.get_heading() # record the starting angle

            while True:
                self.servo(self.MIDPOINT) # return servo to the center 
                while self.quick_check():
                    self.corner_count = 0
                    self.fwd()
                    time.sleep(.01)
                self.stop()
                self.scan() # go to scan method and check surroundings
                self.corners()

                # to do: make turns biased towards the exit
                # to do: add a double corner count if its stuck between two corners
                # to do: 
    def path_towards_exit(self):
        where_I_started = self.get_heading() 
        self.turn_to_deg(self.exit_heading)
        if self.quick_check():
            return True
        else:
            self.turn_to_deg(where_I_started)
        return False    

    def escape(self):
        self.deg_fwd(-360)
        self.turn_to_deg(self.exit_heading)
        self.corner_count = 0

    def corners(self):
        self.corner_count += 1
        if self.corner_count > 3:
            self.escape()
        left_total = 0
        left_count = 0
        right_total = 0
        right_count = 0
        for ang, dist in self.scan_data.items():
            if ang < self.MIDPOINT:
                right_total += dist
                right_count +=1
            else:
                left_total += dist
                left_count += 1
        left_avg = left_total / left_count
        right_avg = right_total / right_count
        if left_avg > right_avg:
            self.turn_by_deg(-45)
        else:
            self.turn_by_deg(45)



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
