import os
import csv
import simpy

from factory import Factory
from station import Station


def run_simulation(
    process_times: "list[float]",
    simulation_time: int = 1000,
    path_buffer: str = "buffer.csv",
    path_events: str = "events.csv",
    save_results: bool = True,
    capa_init: int = 0,
    capa_max: int = 10,
    capa_inf: int = int(1e2),
) -> None:
    """
    Function to simulate a manufacturing line with fully connected stations.

    The total number of stations is determined by the length of the provided
    list of process times. Each station is preceded and followed by a buffer.
    Hence, there will be only one more buffer than stations. The simulations'
    system boundaries are unlimited in supply and demand.

    Parameters
    ----------
    process_time : list[float]
        Process times for the created stations. Will determine the total number
        of stations and buffers in the simulation.
    simulation_time : int, default 1000
        Number of steps that the simulation will run for. The progression of
        the simulation is displayed using a simple progress bar.
    path_buffer : str, default "buffer.csv"
        File (and path) name to store the buffer values of the simulation run.
    path_events : str, default "events.csv"
        File (and path) name to store every event of the simulation run.
    save_results : bool, default True
        Parameter to execute the simulation without storing the buffer and
        event results in a separate csv file.
    capa_init : int, default 0
        Initial capacity of the simpy.Container that act as buffers in the
        simulation. Does not interfere with the later AP calculation, but helps
        to reduce the time for the system to be swung in.
    capa_max : int, default 10
        Maximum capacity of the simpy.Container that will cause stations to
        be blocked if they cannot put products/jobs into the buffer of the
        following station. Affects the bottleneck situation to a high degree.
    capa_inf : int, default 100
        Capacity level of the first station in the manufacturing line. Will
        be refilled once per time step to simulate a virtually unlimited
        supplier. This ensures that bottlenecks occur only due to throughput
        restrictions between stations, and not due to insufficient supply.
    """

    # initialize factory
    factory = Factory(
        process_times=process_times,
        path_buffer=path_buffer,
        path_events=path_events,
        save_results=save_results,
        capa_init=capa_init,
        capa_max=capa_max,
        capa_inf=capa_inf,
    )

    # run stations
    for station in factory.stations.values():
        factory.env.process(station.run_station(factory.env))

    # save?
    if save_results:
        # prevent overwriting
        if not os.path.exists(path_buffer):
            write_new_row(path_buffer, ["t"] + factory.buffer_names)
        # prevent overwriting
        if not os.path.exists(path_events):
            write_new_row(path_events, ["t", "num_station", "num_job", "event_type"])

    # run simulation
    print(
        f"Running simulation with {len(process_times)} stations for {simulation_time} steps. "
    )
    # for t in tqdm(range(1, simulation_time)):
    for t in range(1, simulation_time):
        # iterate one simulation step
        factory.env.run(until=t)
        # save current buffer levels to file
        # note: events are written as they occur by each Station
        _new_row = [t] + factory.get_buffer_levels()
        write_new_row(path_buffer, _new_row)
        # reset level of 'B0' to 'capa_inf'
        factory.restock_customer(capa_inf)


def write_new_row(path: str, row: list) -> None:
    with open(path, "a+", newline="") as f:
        csv.writer(f).writerow(row)


if __name__ == "__main__":
    scenario = {
        "process_times": [2, 2.25, 2, 2.25, 2],
        "simulation_time": 10000,
        "path_buffer": "buffer.csv",
        "path_events": "events.csv",
        "save_results": True,
        "capa_init": 0,
        "capa_max": 10,
        "capa_inf": int(1e2),
    }
    run_simulation(**scenario)
