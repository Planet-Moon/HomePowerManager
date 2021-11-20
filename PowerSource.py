class PowerSource:
    def __init__(self, name: str):
        self.name:str = name
        self._power:float = 0

    def __str__(self):
        return str(self.__dict__)

    @property
    def power(self) -> float:
        return self._power

    @power.setter
    def power(self, power:float):
        self._power = power
