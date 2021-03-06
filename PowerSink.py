import logging
from typing import Union

logger = logging.getLogger(__name__)

class Power_range(object):
    def __init__(self,min:float=0,max:float=0):
        self._min:float = min
        self._max:float = max

    def __str__(self):
        return "{'min':"+str(self._min)+", 'max':"+str(self._max)+"}"

    @property
    def min(self) -> float:
        return self._min

    @min.setter
    def min(self, value:float):
        if value <= self._max and value >= 0:
            self._min = value
        else:
            self._min = self._max

    @property
    def max(self)-> float:
        return self._max

    @max.setter
    def max(self, value:float):
        if value >= self._min and value >= 0:
            self._max = value
        else:
            self._max = self._min

    def floor(self):
        self._max = self._min

    def ceil(self):
        self._min = self._max

    def mean(self):
        avg = (self._max + self._min)/2
        self._min = avg
        self._max = avg



class PowerSink:
    def __init__(self, name: str):
        self.name:str = name
        self._request_power:Power_range = Power_range()
        self._allowed_power:float = 0

    def __str__(self) -> str:
        return str(self.__dict__)

    @property
    def using_power(self) -> float:
        return self._allowed_power

    @property
    def allowed_power(self) -> float:
        return self._allowed_power

    @allowed_power.setter
    def allowed_power(self, allowed_power: float):
        self._allowed_power = allowed_power

    def allow_power(self,power:float=0.0) -> bool:
        """This is used to check if power ready to be used

        Args:
            power (float, optional): Allowed power by power manager. Defaults to 0.0.

        Returns:
            bool: True if power can be used
        """
        self._allowed_power = power
        logger.info("power allowed: {} W".format(self._allowed_power))
        return True

    @property
    def request_power(self) -> Power_range:
        return Power_range(
            self._request_power.min,
            self._request_power.max)

    @request_power.setter
    def request_power(self, value:Union[float,list[int],tuple[int]]):
        if isinstance(value,(list, tuple)):
            self._request_power.max = value[1]
            self._request_power.min = value[0]
        else:
            self._request_power.max = value
            self._request_power.min = value

def main():
    power_sink = PowerSink("test_sink")
    power_sink.request_power = (75, 100)
    print("request_power: {}".format(power_sink.request_power))
    power_sink.request_power = (75, 70)
    print("request_power: {}".format(power_sink.request_power))

if __name__ == '__main__':
    main()
