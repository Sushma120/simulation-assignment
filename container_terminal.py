import simpy
import random
from vessel import Vessel

class ContainerTerminal:
    def __init__(self, env, average_arrival_interval, berth_count, crane_count, truck_count,truck_delay,crane_lift):
        self.env = env
        self.average_arrival_interval = average_arrival_interval
        self.vessel_count = 0
        # Resource- manages limited resources and enable queueing.
        self.berths = simpy.Resource(env, capacity=berth_count)  
        self.cranes = simpy.Resource(env, capacity=crane_count)  
        self.trucks = simpy.Resource(env, capacity=truck_count)
        self.crane_lift_time = crane_lift  
        self.truck_turnaround_time = truck_delay 
        self.env.process(self.vessel_arrival_process())

    def vessel_arrival_process(self):
        while True:
            # vessel interval calculation
            arrival_interval = random.expovariate(1 / self.average_arrival_interval)
            yield self.env.timeout(arrival_interval) 

            # when new vessel arrived, increase the vessel count by 1
            self.vessel_count += 1
            vessel = Vessel(self.env, self, self.vessel_count)
            self.log_event(f"Vessel {vessel.id} has arrived.")

            # handle vessel will take care berth allocation and unloading containers.
            self.env.process(self.handle_vessel(vessel))

    def handle_vessel(self, vessel):
        # creates a request for one unit of this resource.
        with self.berths.request() as berth_request:
            yield berth_request
            self.log_event(f"Vessel {vessel.id} has secured a berth.")

            # If berth is secured , then vessel discharge process
            yield self.env.process(vessel.discharge()) 

    def log_event(self,message):
        # Log all events with specified message.
        print(f"Time {self.env.now:.2f}: {message}")
