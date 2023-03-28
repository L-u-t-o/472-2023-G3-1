import VehicleCalculations
import datetime
import time
# Goal: Simulating traffic lights
# Precondition: The system contains a diagram of the virtual road network. There is a traffic light on a road.
# Postcondition: Vehicles adapt depending on the state of the traffic light.

# Global Variables
green_light = True
light_Times = {}    # (road name, time since traffic light was last changed)

# Vehicles adapt depending on the state of the traffic light.
# Parameters:
#   trafficLight - The current traffic light on the given road
#   vehicles - The current set of vehicles interacting with the traffic light
#   timeSinceLastChange - The time since last change passed in from 3.3 Automatic Simulation
# Returns:
#   vehicles - The list of vehicles that have interacted with the traffic light
def trafficLightInteraction (trafficLight, vehicles, timeSinceLastChange):
    # Traffic Light Variables
    trafficLight_road = trafficLight["road"]
    trafficLight_position = trafficLight["position"]
    trafficLight_cycle = trafficLight["cycle"]
    
    # Track the time when the traffic light was first read
    if trafficLight_road not in light_Times:
        light_Times[trafficLight_road] = datetime.datetime.now()
    # If the time of the traffic light was previously recorded, calculate the difference between now and recorded time
    else:
        difference_time = datetime.datetime.now() - light_Times[trafficLight_road]
        timeSinceLastChange = difference_time.total_seconds()

    # 1 & 1.1. IF time since last change > cycle, THEN change the color of the light (green ⇐⇒ red)
    if timeSinceLastChange > trafficLight_cycle:
        green_light = False
    
    # 2 & 2.1. IF traffic light is green, THEN vehicles in front of the traffic light may accelerate back up
    if green_light == True:
        # Invoke acceleration function for ALL vehicles in front of the current traffic light
        i = 0
        while i < len(vehicles):
            # Make sure the current vehicle is on the current road
            if vehicles[i]["road"] == trafficLight_road:        
                # Adjust acceleration of vehicle if the vehicle is behind the traffic light's position
                if vehicles[i]["position"] < trafficLight_position:
                    VehicleCalculations.calculateAcceleration(vehicles, i)

    # 3.1 IF traffic light is red
    if green_light == False:
        # 3.1.1 THEN IF the first vehicle in front of the light is in the deceleration distance
        distance = trafficLight_position - vehicles[0]["position"] # Calculate distance between traffic light & first vehicle position
        if distance > 0 & distance < VehicleCalculations.decelerationDistance:
            # 3.1.1.1 THEN apply the deceleration factor to the vehicle
            1 # Function unavailable (Pending 3.1 team) 
        # 3.1.2 ELSE IF the first vehicle in front of the light is in the first half of the stopping distance
        elif distance > (VehicleCalculations.stoppingDistance / 2) & distance < VehicleCalculations.stoppingDistance:
            # 3.1.2.1 THEN stop the vehicle
            1 # Function unavailable (Pending 3.1 team)
    
    # Return the list of vehicles that have interacted with the traffic light with updated attributes\
    return vehicles