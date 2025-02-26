# 3.3
from TrafficSimulation2 import *
from VehicleCalculations import calculateVehicleSpeedAndPosition, calculateVehicleOOB
from TrafficLightSimulation  import trafficLightInteraction
from SimulationIntersection import turnVehiclesAtIntersection
from BusStopSimulation import *
import os
import time
import __main__

# Goal: Run simulation automatically
# Precondition: The system contains a diagram of the virtual road network.
# Postcondition: The traffic in the road network is simulated.


# AutomaticSimulation contains all object lists and functions necessary for automatic simulation.
# First create AutomaticSimulation object, then call update on that object
# Atributes:
#   trafficSystem
#       - TrafficSystem object from TrafficSimulation2.py
#   vehicle_list
#       - vehicle list generated from trafficSystem
#   traffic_light_list
#       - traffic light list generated from trafficSystem
# Methods:
#   vehicle_on_road()
#       -prints all vehicles' position and road
#   traffic_light_on_road()
#       -prints all traffic lights' position and cycle
#   update()
#       -calls vehicle_on_road() and traffic_light_on_road()

INPUT_FILE_PATCH = "./InputFiles/prototype2.xml"

class AutomaticSimulation:
    def __init__(self, input_file):
        # create a TrafficSystem object from the input file
        if (input_file != ""):
            self.trafficSystem = TrafficSystem()
            self.trafficSystem.ReadElementsFromFile(input_file)
            self.file_name = os.path.basename(input_file)
        else:
            self.trafficSystem = TrafficSystem()
            self.trafficSystem.ReadElementsFromFile(INPUT_FILE_PATCH) 
            self.file_name = os.path.basename(INPUT_FILE_PATCH)       
        # Get Vehicle List
        self.vehicle_list = self.trafficSystem.vehicleList
        # Get Traffic Light List
        self.traffic_light_list = self.trafficSystem.trafficLightList
        # Get Road List
        self.road_list = self.trafficSystem.roadList
        # Get Crossroads
        self.intersection_list = self.trafficSystem.intersectionList
        # Simulate Intersection
        #self.intersection_sim = IntersectionSim(self.intersection_list, self.road_list, self.traffic_light_list)
        #Get Bus Stop list
        self.bus_stop_list = self.trafficSystem.busStopList
        # List of indices of vehicles that are out of bounds
        self.to_be_removed = []

        # Store current state of trafficlight
        self.trafficlight_current_states = []
        for i in range(len(self.traffic_light_list)):
            if i%2 == 0:
                color = "green"
            else:
                color = "red"
            self.trafficlight_current_states.append({"color": color, "counter": 0})

    def vehicle_on_road(self):
        

        # 1. FOR any vehicle in the road network
        for i in range(len(self.vehicle_list)):
            # 3.1 GOES HERE
            # Execute use-case 3.1 out on the vehicle            
            # print("\n==============")
            # print("Vehicle:" , i)
            # print("==============")
            # print("    -> road: ", self.vehicle_list[i]["road"])
            # print("    -> position: ", self.vehicle_list[i]["position"])
            # print("    -> speed: ", self.vehicle_list[i]["speed"])
            # print("    -> acceleration: ", self.vehicle_list[i]["acceleration"])
            # print("    -> type: ", self.vehicle_list[i]["type"])
            
            # Get new speed and position
            calculateVehicleSpeedAndPosition(self.vehicle_list, i)
            if 'GraphicsEngine.py' in __main__.__file__:
                self.vehicle_list[i]['road'], self.vehicle_list[i]['position'] = self.intersection_sim.is_approaching_N_selected_road(self.vehicle_list[i]['road'], self.vehicle_list[i]['position'])



    def traffic_light_on_road(self):

        # print("\n============================")
        # print("TRAFFICLIGHTS DISPLAY")
        # print("============================")

        # 2. FOR any traffic light in the road networkz
        for i in range(len(self.traffic_light_list)):
            # print("Road: ", self.traffic_light_list[i]["road"])
            # print("    -> position: ", self.traffic_light_list[i]["position"])
            # print("    -> cycle: ", self.traffic_light_list[i]["cycle"])
            trafficLightInteraction(self.traffic_light_list, self.vehicle_list, i, self.trafficlight_current_states)

    def bus_stop_on_road(self):
        for i in range(len(self.bus_stop_list)):
            busStopSimulation(self.bus_stop_list, self.vehicle_list, i)

    def intersection_on_road(self):
        for i in range(len(self.intersection_list)):
            turnVehiclesAtIntersection(self.intersection_list, i, self.vehicle_list)

    def create_vehicle_on_road(self, road, position, speed, acceration, type):
        self.vehicle_list.append({"road": road,
                                  "position": position,
                                  "speed": speed,
                                  "acceleration": acceration,
                                  "type": type})
        
    def remove_vehicles_off_road(self):
        for i in sorted(self.to_be_removed, reverse=True):
            del self.vehicle_list[i]
        
        self.to_be_removed.clear()

    def create_traffic_light_on_road(self, road, position, cycle, color):
        self.traffic_light_list.append({"road": road,
                                        "position": position, 
                                        "cycle": cycle})
        self.trafficlight_current_states.append({"color": color, "counter": 0})

    def update(self):
        self.vehicle_on_road()
        self.traffic_light_on_road()
        self.bus_stop_on_road()
        self.intersection_on_road()
        calculateVehicleOOB(self.vehicle_list, self.road_list, self.to_be_removed)
        


# simulation = AutomaticSimulation()

# t_end = time.time() + 60 * 15
# while time.time() < t_end:
#     simulation.update()
#     print("\n======================================================================================\n")
#     time.sleep(1)