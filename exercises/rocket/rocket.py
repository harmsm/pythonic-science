__description__ = \
"""
A class for simulating a rocket landing on a planet.  This is designed as a tool
for students to learn how to poke around and understand a new API.
"""
__author__ = "Michael J. Harms"
__date__ = "2017-02-06"


import numpy as np
import random

class Rocket:
    """
    Rocket simulation class.  Simulates a rocket falling towards a planet.  It 
    uses a discrete time step approximation and assumes no atmosphere.  To land
    the rocket successfully, the x and y velocity of the rocket must be within 
    tolerances.  Further, there is a time limit before the simulation ends (you
    run out of air). 
    """

    def __init__(self,starting_position=(0.0,1000.0),
                 starting_velocity=(0.0,0.0)):
        """
        Start a rocket simulation.  
        
        starting_position: tuple or list with initial position in [x,y] (meters)
        starting_velocity: tuple or list with initial velocity [x,y] (meters/second)
        time_step: time step for simulation (seconds)
        """        
        
        # Constants
        self._X_THRUST_START   = 0.0        # kg/s
        self._Y_THRUST_START   = 0.0        # kg/s
        self._EXHAUST_VELOCITY = 100.0      # m/s
        self._X_THRUSTER_LIMIT = (-50,50)   # kg/s
        self._Y_THRUSTER_LIMIT = (  0,50)   # kg/s
        self._MAX_TIME = 200                # s
        
        # More constants
        self._SHIP_MASS = 1.0               # kg
        self._GRAVITY = -9.8                # m/s/s
        self._STARTING_FUEL = 1000.0        # kg
        self._DT = 1.0                      # s
        self._X_VELOCITY_TOLERANCE = 2.0    # m/s
        self._Y_VELOCITY_TOLERANCE = 2.0    # m/s

        # Initialize variables
        self._time = 0.0
        self._x_thruster = self._X_THRUST_START
        self._y_thruster = self._Y_THRUST_START
        self._fuel = self._STARTING_FUEL
        self._alive = True
        self._landed = False
        self._position =      [float(starting_position[0]),float(starting_position[1])]
        self._velocity =      [float(starting_velocity[0]),float(starting_velocity[1])]
        self._acceleration =  [0.0,0.0]
    
        
    def update(self):
        """
        Take a time step for the rocket given the current thrusters etc.
        """
    
        # If we're dead, don't do all the rest
        if not self.alive:
            return False
        
        # Update the time
        self._time = self._time + self._DT
    
        # Determine fuel consumption
        x_fuel = np.abs(self._x_thruster*self._DT)
        y_fuel = np.abs(self._y_thruster*self._DT)
        
        if self._fuel == 0.0:
            self._x_thruster = 0.0
            self._y_thruster = 0.0
        
        else:
            
            # If we're going to run out of fuel...
            if (x_fuel + y_fuel) > self._fuel:
        
                if x_fuel == 0:
                    avail_y_fuel = self._fuel
                    self._y_thruster = avail_y_fuel/y_fuel*self._y_thruster
                elif y_fuel == 0:
                    avail_x_fuel = self._fuel
                    self._x_thruster = avail_x_fuel/x_fuel*self._x_thruster
                else:
                    # Make a weighted average of the thrusters
                    avail_x_fuel = self._fuel*x_fuel/(x_fuel + y_fuel)
                    avail_y_fuel = self._fuel*y_fuel/(x_fuel + y_fuel)
            
                    # Turn down thrusters appropriatesly
                    self._x_thruster = avail_x_fuel/x_fuel*self._x_thruster
                    self._y_thruster = avail_y_fuel/y_fuel*self._y_thruster
            
                # out of fuel!
                self._fuel = 0.0
            else:
                self._fuel = self._fuel - x_fuel - y_fuel
        
        # Determine current ship mass
        current_mass = self._fuel + self._SHIP_MASS
    
        # Force from x-thruster
        F_x = self._x_thruster*self._EXHAUST_VELOCITY
    
        # Force from y-thruster and gravity
        F_y_thruster = self._y_thruster*self._EXHAUST_VELOCITY
        F_y_gravity = current_mass*self._GRAVITY
        F_y = F_y_thruster + F_y_gravity
      
        # Acceleration
        self._acceleration[0] = F_x/current_mass
        self._acceleration[1] = F_y/current_mass
    
        # Position
        self._position[0] = self._position[0] + self._velocity[0]*self._DT + 0.5*self._acceleration[0]*(self._DT)**2
        self._position[1] = self._position[1] + self._velocity[1]*self._DT + 0.5*self._acceleration[1]*(self._DT)**2
    
        # Velocity
        self._velocity[0] = self._velocity[0] + self._acceleration[0]*self._DT
        self._velocity[1] = self._velocity[1] + self._acceleration[1]*self._DT
        
        if self._position[1] <= 0.0:
            
            # CRASHED
            if abs(self._velocity[0]) > self._X_VELOCITY_TOLERANCE:
                self._alive = False    
            if abs(self._velocity[1]) > self._Y_VELOCITY_TOLERANCE:
                self._alive = False
                
                
                
            if self._alive:
                self._position[1] = 0.0
                self._x_thruster = 0.0
                self._y_thruster = 0.0
                self._velocity[0] = 0.0
                self._velocity[1] = 0.0
                self._landed = True
            else:

                death_messages = ["Maybe a future mission can recover your body.",
                                  "Your party contracts typhoid.  You are all dead.",
                                  "Reincarnation is not a landing strategy.",
                                  "Eject, eject, eject!",
                                  "What's this thing coming toward me very fast? So big and flat and round, it needs a big wide sounding name like 'Ow', 'Ownge', 'Round', 'Ground'! That's it! Ground! Ha! I wonder if it'll be friends with me? Hello, Ground!",
                                  "The safetey commission concludes that the pilot pushed the wrong button."]
                
                print("CRASHED: {}".format(random.choice(death_messages)))
            
        # Air (max time)
        if self._time > self._MAX_TIME:
            self._alive = False
            
            death_messages = ["Ack, ack, ack... gurgle",
                              "As president of Planet Spaceball, I can assure both you and your viewers that there's absolutely no air shortage whatsoever. Yes, of course. I've heard the same rumor myself.",
                              "'YOU FEAR TO DIE? 'It's not that I don't want... I mean, I've always...it's just that life is a habit that's hard to break...'"]
            print("RAN OUT OF AIR: {}".format(random.choice(death_messages)))
                
            
        # Landed
        if self._landed:
                
            landed_messages = ["Houston, the Eagle has Landed!",
                               "Glad that's over.",
                               "Hopefully you have enough fuel to go home.",
                               "Make sure you put on your space helmet before going outside."]
            print("LANDED: {}".format(random.choice(landed_messages)))
        
        
        # Return whether we're alive or dead
        return self.alive
    
    @property
    def rocket_specs(self):
        """
        Information about the rocket's tolerances. 
        """
        
        return {"min x_thruster setting":self._X_THRUSTER_LIMIT[0],
                "max x_thruster setting":self._X_THRUSTER_LIMIT[1],
                "min y_thruster setting":self._Y_THRUSTER_LIMIT[0],
                "max y_thruster setting":self._Y_THRUSTER_LIMIT[1],
                "x_velocity landing tolerance":self._X_VELOCITY_TOLERANCE,
                "y_velocity landing tolerance":self._Y_VELOCITY_TOLERANCE,
                "max time before air runs out":self._MAX_TIME}
    
    @property
    def time(self):
        """
        Current time.
        """
        return self._time
    
    @property
    def x_thruster(self):
        """
        Current x thruster setting.
        """
        
        return self._x_thruster
    
    @x_thruster.setter
    def x_thruster(self,x_thruster):
        """
        Update the x thruster
        """
        
        if x_thruster < self._X_THRUSTER_LIMIT[0]:
            self._x_thruster = self._X_THRUSTER_LIMIT[0]
        elif x_thruster > self._X_THRUSTER_LIMIT[1]:
            self._x_thruster = self._X_THRUSTER_LIMIT[1]
        else:
            self._x_thruster = x_thruster
        
    @property
    def y_thruster(self):
        """
        Current y thruster setting.
        """

        return self._y_thruster
    
    @y_thruster.setter
    def y_thruster(self,y_thruster):
        """
        Update the y thruster
        """
        if y_thruster < self._Y_THRUSTER_LIMIT[0]:
            self._y_thruster = self._Y_THRUSTER_LIMIT[0]
        elif y_thruster > self._Y_THRUSTER_LIMIT[1]:
            self._y_thruster = self._Y_THRUSTER_LIMIT[1]
        else:
            self._y_thruster = y_thruster
    
    @property
    def alive(self):
        """
        Whether you are alive or dead.
        """
        
        return self._alive
    
    @property
    def landed(self):
        """
        Whether you've landed or not.
        """
        
        return self._landed
    
    @property
    def fuel(self):
        """
        Current fuel status.
        """
        
        return self._fuel

    @property
    def position(self):
        """
        Current (x,y) position.
        """
        
        return self._position
    
    @property
    def velocity(self):
        """
        Current (x, y) velocity.
        """
        
        return self._velocity
    
    @property
    def acceleration(self):
        """
        Current (x,y) acceleration.
        """
        
        return self._acceleration


