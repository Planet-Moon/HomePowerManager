import copy
import logging
import threading
from time import sleep

logger = logging.getLogger(__name__)


def remove_from_list(list, start: int = 0, end: int = -1) -> list:
    if end < 0:
        end = len(list)
    del list[start:end]
    return list

class PowerManagerThread(threading.Thread):
    def __init__(self, power_manager, update_period = 1):
        self.power_manager = power_manager
        self.update_period = update_period
        self.enable = True
        threading.Thread.__init__(self, name="power_manager")
        pass

    def run(self):
        logger.info("PowerManager thread started")
        while self.enable:
            self.power_manager.distribute()
            sleep(self.update_period)
        logger.info("PowerManager thread stopped")


class PowerManager(object):
    def __init__(self, sources: list = [], sinks: list = []):
        self._sources = sources
        self._sinks = sinks
        self.power_distribution = {}
        for i in sinks:
            self.power_distribution[i.name] = i.using_power
        self._power_grid = lambda: 0

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
        self.power_distribution[sink.name] = sink.using_power

    def remove_sinks(self, start: int = 0, end: int = -1):
        self._sinks = remove_from_list(self._sinks, start, end)

    @property
    def power_grid(self) -> float:
        """Function to calulate the power from the grid.
        Positive if more power is drawn then generated.
        If more power is generated set to negative value.

        'lambda: power draw - power generation'

        Returns:
            float: power draw
        """
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

    def distribute(self) -> float:
        power = self.available_power - self.power_grid
        logger.info("available power: {} W".format(power))
        for i in self._sinks:
            request_power = copy.copy(i.request_power)
            grant_power = copy.copy(power)
            # Versuche einzuschalten bei genügend Leistung
            if grant_power >= request_power.min and request_power.max > 0:
                if grant_power > request_power.max:
                    grant_power = request_power.max
                # Einschaltversuch
                if i.allow_power(grant_power):
                    logger.info(i.name+": Turn on Success")
                else:
                    print("here")
                # Speichern der Leistungsverteilung
                self.power_distribution[i.name] = i.using_power
                # Abzug der verwendeten Leistung
                power -= i.using_power
            elif i.allow_power(0): # Versuche auszuschalten
                self.power_distribution[i.name] = 0
            else: # Berechne Verlust bei unerfolgreichem Ausschalten
                power -= self.power_distribution.get(i.name, request_power.min)

        logger.info("remaining power: {} W".format(power))
        logger.info("---------------------")
        return power
