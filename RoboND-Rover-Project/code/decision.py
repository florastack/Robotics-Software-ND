# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 09:07:57 2018

@author: Jie Wang
"""
import numpy as np

# The decision making module is based on the provided decision template.
# The rock picking is added to pick up rocks on mapping process
# Due to no wall following or any futrture stragegies, the rover easily got struct in local minima 
# Control module is also needed to make the motion more smoothly


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with #None means absence
    
    # Add rock picking decision making module 
    if Rover.nav_angles is not None:

        if Rover.picking_up == 1:
            Rover.throttle = 0
            Rover.steer = 0
            Rover.brake = Rover.brake_set # set to 10 
            Rover.mode = 'stop'
        elif Rover.near_sample == 1:
            Rover.brake = Rover.brake_set
            Rover.mode = 'stop'
            Rover.steer = 0
            Rover.send_pickup = True
            Rover.samples_collected += 1
        elif len(Rover.rock_dists) > 0:
            print(len(Rover.rock_dists))
            Rover.mode = 'rock'
            if Rover.vel < Rover.max_vel:
                # Set throttle value to throttle setting
                Rover.throttle = Rover.throttle_set
            else: # Else coast
                Rover.throttle = 0
            Rover.brake = 0
            # Set steering to average angle clipped to the range +/- 15
            Rover.steer = np.clip(np.mean(Rover.rock_angles * 180/np.pi), -15, 15)
        # Check for Rover.mode status
        elif Rover.mode == 'forward': 
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:  
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0

                # Set steering to average angle clipped to the range +/- 15
                Rover.steer = np.clip((np.mean(Rover.nav_angles * 180/np.pi)), -15, 15)
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -15 # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
					#Angle_weight = 0.9
					#Dist_weight = 0.1
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
					#Rover.steer = np.clip(Angle_weight*(np.mean(Rover.nav_angles * 180/np.pi)+Dist_weight*(np.mean(Rover.nav_dists)), -15, 15)
                    Rover.mode = 'forward'
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    # If in a state where want to pickup a rock send pickup command
    # if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
    #     Rover.send_pickup = True
    
    return Rover
