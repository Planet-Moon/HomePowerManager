import logging

logger = logging.getLogger(__name__)

class PowerSink:
    def __init__(self, name: str):
        self.name = name
        self._request_power = 0
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
        logger.info("power allowed: {} W".format(self._allowed_power))

    def allow_power(self,power:float=0.0) -> bool:
        """This is used to check if power ready to be used

        Args:
            power (float, optional): Allowed power by power manager. Defaults to 0.0.

        Returns:
            bool: True if power can be used
        """
        self._allowed_power = power
        return True

    @property
    def request_power(self):
        return self._request_power - self._allowed_power

    @request_power.setter
    def request_power(self, request_power):
        self._request_power = request_power
