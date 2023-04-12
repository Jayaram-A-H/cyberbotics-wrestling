from controller import Robot
import sys


# We provide a set of utilities to help you with the development of your controller. You can find them in the utils folder.
# If you want to see a list of examples that use them, you can go to https://github.com/cyberbotics/wrestling#demo-robot-controllers
sys.path.append('..')
from utils.motion_library import MotionLibrary
from utils.camera import Camera
from utils.image_processing import ImageProcessing as IP
from utils.accelerometer import Accelerometer
from utils.finite_state_machine import FiniteStateMachine
from utils.current_motion_manager import CurrentMotionManager

class Wrestler (Robot): 
    def __init__(self):
        Robot.__init__(self)
        self.time_step = int(self.getBasicTimeStep())    
        self.fsm=FiniteStateMachine(
            states=['DEFAULT','FRONT_FALL','BACK_FALL','BLOCKING_MOTION','JUST_STAND'],
            initial_state='DEFAULT',
            actions={
                'DEFAULT':self.walk,
                'BLOCKING_MOTION':self.pending,
                'FRONT_FALL':self.front_fall,
                'BACK_FALL':self.back_fall,
                'JUST_STAND':self.just_stand
            }
        )
        self.accelerometer = Accelerometer(self, self.time_step)
        self.RShoulderRoll = self.getDevice('RShoulderRoll')
        self.LShoulderRoll = self.getDevice('LShoulderRoll')
        
        self.current_motion = CurrentMotionManager()
        self.library = MotionLibrary()
        
    def run(self):
        # to load all the motions from the motions folder, we use the MotionLibrary class:
        #self.camera = Camera(self)
        
        # retrieves the WorldInfo.basicTimeTime (ms) from the world file
        self.current_motion.set(self.library.get('Stand'))
        #self.current_motion.set(self.library.get('Forwards50'))
        self.fsm.transition_to('DEFAULT')
        
        while self.step(self.time_step) != -1:  # mandatory function to make the simulation run
            self.detect_fall()
            self.fsm.execute_action()
            #img = self.camera.get_image()
            #_,_, horizontal = IP.locate_opponent(img)
            #if horizontal is None:
            #    hor=0
            #else: hor= horizontal * 2 / img.shape[1] - 1
            
    def detect_fall(self):
        '''Detect a fall and update the FSM state.'''
        [acc_x, acc_y, _] = self.accelerometer.get_new_average()
        if acc_x < -7:
            self.fsm.transition_to('FRONT_FALL')
        elif acc_x > 7:
            self.fsm.transition_to('BACK_FALL')
        if acc_y < -7:
            # Fell to its right, pushing itself on its back
            self.RShoulderRoll.setPosition(-1.2)
        elif acc_y > 7:
            # Fell to its left, pushing itself on its back
            self.LShoulderRoll.setPosition(1.2)

    def pending(self):
        # waits for the current motion to finish before doing anything else
        if self.current_motion.is_over():
            self.fsm.transition_to('JUST_STAND')
            
    def just_stand(self):
        if self.current_motion.get() != self.library.get('Stand'):
            self.current_motion.set(self.library.get('Stand'))


    def walk(self):
        if self.current_motion.get() != self.library.get('Forwards50'):
            self.current_motion.set(self.library.get('Forwards50'))

    def front_fall(self):
        self.current_motion.set(self.library.get('GetUpFront'))
        self.fsm.transition_to('BLOCKING_MOTION')

    def back_fall(self):
        self.current_motion.set(self.library.get('GetUpBack'))
        self.fsm.transition_to('BLOCKING_MOTION')


    
            
            



# create the Robot instance and run main loop
wrestler = Wrestler()
wrestler.run()
