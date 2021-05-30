class PowerSource:
    def __init__(self, name: str):
        self.name = name
        self._power = 0

    def __str__(self):
        return str(self.__dict__)

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, power):
        self._power = power
