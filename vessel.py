import simpy

class Vessel:
    def __init__(self, env, terminal, id, containers=150):
        self.env = env
        self.terminal = terminal
        self.id = id
        self.containers = containers

    def discharge(self):
        # creates a request for one unit of this resource.
        with self.terminal.cranes.request() as crane_request:
            # pauses the process until a crane becomes available
            yield crane_request
            self.terminal.log_event(f"Vessel {self.id} has secured a crane.")
            
            # For each container - truck should be available
            for container in range(1,self.containers+1):
                self.env.process(self.unload_container(container))

                yield self.env.timeout(self.terminal.crane_lift_time) # delay of 3minutes crane to truck 
                self.terminal.log_event(f"Truck transporting container {container } of vessel {self.id} to the yard.")

                yield self.env.timeout(self.terminal.truck_turnaround_time)  # delay of 6 minutes
                self.terminal.log_event(f"Truck has returned to the quay for the next container.")

            self.terminal.log_event(f"Vessel {self.id} has finished discharging and leaves the berth.")
    
    def unload_container(self,container):
        with self.terminal.trucks.request() as truck_request:
            yield truck_request
            self.terminal.log_event(f"Crane is unloading container {container } of vessel {self.id} onto a truck.")
