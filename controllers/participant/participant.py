from controller import Robot, Motion


class Alice (Robot):
    def run(self):
        # motion files are text files containing pre-recorded positions of the robot's joints
        handWave = Motion('../motions/HandWave.motion')
        handWave.setLoop(True)
        handWave.play()
        # retrieves the simulation time step (ms) from the world file
        time_step = int(self.getBasicTimeStep())
        while self.step(time_step) != -1:  # Mandatory function to make the simulation run
            pass


# create the Robot instance and run main loop
wrestler = Alice()
wrestler.run()


