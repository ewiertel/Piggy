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
        '''
        if not self.safe_to_dance():
            print("Not enough room to safely dance")
            return
        else:
            print("Lets dance.")
        '''
        for x in range(1):
            # self.chacha()
            # self.spin()
            self.dab()
            # self.moonwalk()

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
        self.turn_by_deg(60)
        self.servo(2000)
        self.turn_by_deg(-60)
        self.servo(1500)

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
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 3):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        print("I can't count how many obstacles are around me. Please give my programmer a zero.")

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")




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
