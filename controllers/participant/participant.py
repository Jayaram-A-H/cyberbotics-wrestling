from controller import Robot
import sys
sys.path.append('..')
from utils.motion_library import MotionLibrary
from utils.camera import Camera
from utils.image_processing import ImageProcessing as IP
from utils.accelerometer import Accelerometer
from utils.finite_state_machine import FiniteStateMachine
from utils.current_motion_manager import CurrentMotionManager
from utils.fall_detection import FallDetection

class Wrestler (Robot): 
    def __init__(self):
        Robot.__init__(self)
        self.time_step = int(self.getBasicTimeStep())    
        self.accelerometer = Accelerometer(self, self.time_step)
        self.RShoulderRoll = self.getDevice('RShoulderRoll')
        self.LShoulderRoll = self.getDevice('LShoulderRoll')
        self.fall_detector = FallDetection(self.time_step, self)
        self.current_motion = CurrentMotionManager()
        self.library = MotionLibrary()
        
    def run(self):
        
        while self.step(self.time_step) != -1:  # mandatory function to make the simulation run
            self.current_motion.set(self.library.get('ForwardLoop'))
            self.fall_detector.check()
            #img = self.camera.get_image()
            #_,_, horizontal = IP.locate_opponent(img)
            #if horizontal is None:
            #    hor=0
            #else: hor= horizontal * 2 / img.shape[1] - 1     
            
wrestler = Wrestler()
wrestler.run()
