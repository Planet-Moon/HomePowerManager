import random
from PowerSource import PowerSource
from PowerSink import PowerSink


class ExamplePowerSource(PowerSource):
    def __init__(self, name: str):
        super(ExamplePowerSource, self).__init__(name)

    @property
    def power(self):
        return random.randint(5000, 6000)


class ExamplePowerSink(PowerSink):
    def __init__(self, name: str):
        super(ExamplePowerSink, self).__init__(name)
        self.request_power = (random.randint(0, 2000), random.randint(2000, 4000))

    def allow_power(self,power:float=0.0) -> bool:
        rand = random.randint(0,9)
        if rand > 5 or True:
            self._allowed_power = power
            return True
        else:
            return False

class ExampleSink(PowerSink):
    def __init__(self, name: str):
        super().__init__(name=name)
