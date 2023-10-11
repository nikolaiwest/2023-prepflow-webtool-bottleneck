import simpy
from station import Station


class Factory:
    def __init__(
        self,
        process_times: "list[int]",
        path_events: str,
        path_buffer: str,
        save_results: bool,
        capa_init: int,
        capa_max: int,
        capa_inf: int,
    ):
        self.env = simpy.Environment()
        self.process_times = process_times
        self.path_events = path_events
        self.path_buffer = path_buffer
        self.save_results = save_results
        self.capa_init = capa_init
        self.capa_max = capa_max
        self.capa_inf = capa_inf
        self.num_stations = len(process_times)
        self.num_buffers = self.num_stations + 1

        self.station_names = [f"S{i}" for i in range(self.num_stations)]
        self.buffer_names = [f"B{i}" for i in range(self.num_buffers)]
        self.stations = self._get_stations()
        self.buffers = self._get_buffers()

        self._update_stations()

    def _update_stations(self):
        for n in range(self.num_stations):
            self.stations[self.station_names[n]].buffer_get = self.buffers[
                self.buffer_names[n]
            ]
            self.stations[self.station_names[n]].buffer_put = self.buffers[
                self.buffer_names[n + 1]
            ]

    def _buffer_selector(self, n):
        if n == 0:
            return simpy.Container(  # first buffer
                env=self.env, capacity=float("inf"), init=self.capa_inf
            )
        elif n == self.num_stations:
            return simpy.Container(  # last buffer
                env=self.env, capacity=float("inf"), init=0
            )
        else:
            return simpy.Container(
                env=self.env, capacity=self.capa_max, init=self.capa_init
            )

    def _get_buffers(self) -> "dict[str, simpy.Container]":
        return {
            buffer_name: self._buffer_selector(int(buffer_name[1:]))
            for buffer_name in self.buffer_names
        }

    def _get_stations(self) -> "dict[str, Station]":
        return {
            station_name: Station(
                process_time=pt,
                station_name=station_name,
                path_events=self.path_events,
            )
            for (station_name, pt) in zip(self.station_names, self.process_times)
        }

    def get_buffer_levels(self) -> "list[int]":
        return [buffer.level for buffer in self.buffers.values()]

    def get_station_states(self) -> "list[str]":
        return [station.state for station in self.stations.values()]

    def restock_customer(self, capa_inf: int) -> None:
        curr_stock = self.buffers[self.buffer_names[0]].level
        if curr_stock < capa_inf:
            self.buffers[self.buffer_names[0]].put(capa_inf - curr_stock)
