import random


class Source:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return str(self.__dict__)

    @property
    def power(self):
        return random.randint(2000, 4000)


class Sink:
    def __init__(self, name: str):
        self.name = name
        self._request_power = random.randint(0, 4000)
        self._allowed_power = 0
        self._power_priority = 0

    def __str__(self):
        return str(self.__dict__)

    @property
    def power_priority(self):
        return self._power_priority

    @power_priority.setter
    def power_priority(self, priority):
        self._power_priority = priority

    @property
    def allowed_power(self):
        return self._allowed_power

    @allowed_power.setter
    def allowed_power(self, allowed_power):
        self._allowed_power = allowed_power
        print("power allowed: {} W".format(self._allowed_power))

    @property
    def request_power(self):
        return self._request_power - self._allowed_power

    @request_power.setter
    def request_power(self, request_power):
        self._request_power = request_power
