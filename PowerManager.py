import copy


def remove_from_list(list, start: int = 0, end: int = -1) -> list:
    if end < 0:
        end = len(list)
    del list[start:end]
    return list


class PowerManager:
    def __init__(self, sources: list = [], sinks: list = []):
        self._sources = sources
        self._sinks = sinks
        self._power_grid = lambda: 0
        self._power_distribution = {}

    @property
    def sources(self) -> list:
        return self._sources

    @sources.setter
    def sources(self, source):
        self._sources.append(source)

    def remove_sources(self, start: int = 0, end: int = -1):
        self._sources = remove_from_list(self._sources, start, end)

    @property
    def sinks(self) -> list:
        return self._sinks

    @sinks.setter
    def sinks(self, sink):
        self._sinks.append(sink)

    def remove_sinks(self, start: int = 0, end: int = -1):
        self._sinks = remove_from_list(self._sinks, start, end)

    @property
    def power_grid(self) -> float:
        return self._power_grid()

    @power_grid.setter
    def power_grid(self, function):
        self._power_grid = function

    @property
    def available_power(self):
        power = 0
        for i in self._sources:
            power += getattr(i, "power", 0)
        return power

    def distribute(self):
        power = self.available_power - self.power_grid
        print("available power: {} W".format(power))
        for i in self._sinks:
            if power > i.request_power:
                self._power_distribution[i.name] = i.request_power
            else:
                self._power_distribution[i.name] = 0
            i.available_power = self._power_distribution[i.name]
            power -= i.available_power
        print("remaining power: {} W".format(power))
