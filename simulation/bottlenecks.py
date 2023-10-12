import numpy as np
import pandas as pd


class Bottlenecks:
    def __init__(
        self,
        events: pd.DataFrame,
    ):
        self.events = events

    def _get_event_length(self) -> int:
        t_max = max(self.events["t"])
        if t_max % 1 == 0:
            return int(t_max)
        else:
            return int(t_max) + 1

    def _get_event_stations(self, how: str) -> list:
        if how == "name":
            return [f"S{n}" for n in self.events["num_station"].unique().tolist()]
        elif how == "num":
            return [n for n in self.events["num_station"].unique().tolist()]
        else:
            raise ValueError(f"{how} not accepted")

    def _get_t_of_first_active(self, step: int, station: int) -> float:
        subset = self.events[
            (self.events["num_station"] == station) & (self.events["t"] <= step)
        ]
        t_first_active = 0
        for _, step in subset[::-1].iterrows():
            if step["status"] == "passive" or step["status"] == "init":
                break
            else:
                t_first_active = step["t"]
        return t_first_active

    def calc_active_periods(self) -> pd.DataFrame:
        events_length = self._get_event_length()
        station_names = self._get_event_stations(how="name")
        station_nums = self._get_event_stations(how="num")
        # create new resut df
        active_periods = pd.DataFrame(
            np.nan, index=range(events_length), columns=station_names
        )
        # iter over results and the time of the first active state
        print(f"Calculating the active periods for all {len(station_names)} stations.")
        for index, _ in active_periods.iterrows():
            # print(f"- getting period resets: {index}/{events_length}", flush=True)
            for station_name, station_num in zip(station_names, station_nums):
                active_periods.loc[index, station_name] = self._get_t_of_first_active(
                    index,
                    station_num,
                )

        # repeat iteration to update active periods for all timesteps
        for index, _ in active_periods.iterrows():
            # print(f"- getting remaining time: {index}/{events_length}", flush=True)
            for station_name, station_num in zip(station_names, station_nums):
                if active_periods.loc[index, station_name] != 0:
                    active_periods.loc[index, station_name] = (
                        index - active_periods.loc[index, station_name]
                    )
                elif active_periods.loc[index, station_name] == 0 and index > 0:
                    active_periods.loc[index, station_name] = (
                        active_periods.loc[index - 1, station_name] + 1
                    )
                else:
                    active_periods.loc[index, station_name] = 0
        # determine bottleneck station
        active_periods["bottleneck"] = active_periods.idxmax(axis=1)
        return active_periods
