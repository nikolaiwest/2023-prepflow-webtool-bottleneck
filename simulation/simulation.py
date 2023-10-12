import os
import csv
import pandas as pd

from .factory import Factory
from .bottlenecks import Bottlenecks


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

    events = get_events(path="events.csv")
    events.to_csv("events.csv")


def write_new_row(path: str, row: list) -> None:
    with open(path, "a+", newline="") as f:
        csv.writer(f).writerow(row)


def get_events(path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["status"] = "init"

    for index, event in df.iterrows():
        # set 'status' to 'active' if a new job was started
        if event["event_type"] == "job start" and event["num_job"] != 1:
            df.loc[index, "status"] = "active"
        elif event["event_type"] == "job finish":
            _check_status = station_remains_active(
                df, event["num_station"], event["num_job"]
            )
            if _check_status.size > 0 and _check_status:
                df.loc[index, "status"] = "active"
            else:
                df.loc[index, "status"] = "passive"
        else:
            # remain init for 'num_job' == 1
            pass
    return df


def station_remains_active(events, num_station, num_job) -> bool:
    time_finish_last_job = events[
        (events["num_station"] == num_station)
        & (events["num_job"] == num_job)
        & (events["event_type"] == "job finish")
    ]["t"].values
    time_start_next_job = events[
        (events["num_station"] == num_station)
        & (events["num_job"] == num_job + 1)
        & (events["event_type"] == "job start")
    ]["t"].values
    return time_finish_last_job == time_start_next_job


# Just for testing
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
    # Run
    run_simulation(**scenario)
    # Load results from file
    buffer_level = pd.read_csv("buffer.csv")
    events = pd.read_csv("events.csv")
    # Get active periods
    bottlenecks = Bottlenecks(events)
    active_periods = bottlenecks.calc_active_periods()
    # Save
    active_periods.to_csv("active_periods.csv")
