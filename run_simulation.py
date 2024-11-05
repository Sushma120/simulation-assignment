import simpy
from container_terminal import ContainerTerminal

if __name__ == "__main__":
    #Input variables and values.
    SIMULATION_TIME = 30
    ARRIVAL_INTERVAL = 5
    BERTH_COUNT = 2
    CRANE_COUNT = 2
    TRUCK_COUNT = 2
    TRUCK_TURNAROUND_TIME=6
    CRANE_LIFT_TIME=3

    # Create simpy environment
    env = simpy.Environment() 

    #Initialize with main simulation component
    terminal = ContainerTerminal(env, average_arrival_interval=ARRIVAL_INTERVAL, berth_count=BERTH_COUNT, crane_count=CRANE_COUNT, truck_count=TRUCK_COUNT,truck_delay=TRUCK_TURNAROUND_TIME,crane_lift=CRANE_LIFT_TIME)

    # Run simulation 
    env.run(until=SIMULATION_TIME) 
