import csv
import simpy

from scipy.stats import expon


class Station:
    def __init__(self, process_time: float, station_name: str, path_events: str):
        self.pt: float = process_time
        self.name = station_name
        self.path_events = path_events

        self.buffer_get: simpy.Container
        self.buffer_put: simpy.Container
        self.finished_jobs: int = 0
        self.break_down: bool = False
        self.state = "init"

    def _change_state(self, new_state: str):
        state_dict = {
            "active": 0,
            "starved": 1,
            "blocked": 2,
            "breakdown": 3,
        }
        self.state = state_dict[new_state]

    def run_station(self, env: simpy.Environment):
        while True:
            # change state: waiting for material
            self._change_state("starved")
            # get material
            yield self.buffer_get.get(1)
            # change state: running job
            self._change_state("active")
            # time out while running

            write_new_row(
                path=self.path_events,
                row=[
                    round(env.now, 3),
                    self.name[1:],
                    self.finished_jobs + 1,
                    "job start",
                ],
            )
            yield env.timeout(self._apply_var(self.pt))
            write_new_row(
                path=self.path_events,
                row=[
                    round(env.now, 3),
                    self.name[1:],
                    self.finished_jobs + 1,
                    "job finish",
                ],
            )

            self.finished_jobs += 1
            # change state: returning material
            self._change_state("blocked")
            # return material
            yield self.buffer_put.put(1)

    def _apply_var(self, pt: float) -> float:
        # return max(0, random.gauss(pt, pt*STD_DEV))
        return max(0, expon.rvs(scale=pt, loc=pt, size=1)[0])


def write_new_row(path: str, row: list) -> None:
    with open(path, "a+", newline="") as f:
        csv.writer(f).writerow(row)
