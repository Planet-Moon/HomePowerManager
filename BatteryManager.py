from SMA_StorageBoy import SMA_StorageBoy


class BatteryManager:
    supported_inverters = (SMA_StorageBoy)  # add supported_inverters here

    def __init__(self, inverters: list = [], name:str="Batterymanager") -> None:
        self.name = name
        self._inverters = []
        for i in inverters:
            self.addInverter(i)

        # test if all are working
        self.power
        self.soc
        self.present_discharge
        self.present_charge
        self.charge
        self.total_capacity
        self.charge_missing

    @property
    def inverters(self) -> list:
        return self._inverters

    def addInverter(self, inverter) -> None:
        """Add inverter to BatteryManager

        Args:
            inverter (self.supported_inverters): Any inverter type in supported_inverters

        Raises:
            TypeError: When inverter is not in the tuple of supported inverters
        """
        if isinstance(inverter, self.supported_inverters):
            class InverterModel:
                def __init__(self, inverter, needed_power=0, available_power=0):
                    self.device = inverter
                    self.needed_power = needed_power
                    self.available_power = available_power

            self._inverters.append(InverterModel(inverter))
        else:
            raise TypeError("Inverter not supported")

    @property
    def power(self) -> int:
        """Calculate the power needed or available

        Returns:
            int: power needed (<0) or available (>0) (W)
        """
        needed_power = 0
        available_power = 0
        for i in self._inverters:
            if i.device.soc < 65:
                i.needed_power = i.device.maxChargePower
                i.available_power = 0
            if i.device.soc > 85:
                i.needed_power = 0
                i.available_power = i.device.maxDischargePower

            # Initialization
            if i.needed_power == 0 and i.available_power == 0:
                i.needed_power = 0
                i.available_power = i.device.maxDischargePower

            needed_power += i.needed_power
            available_power += i.available_power
        if needed_power > 0:
            return needed_power * -1
        else:
            return available_power

    @property
    def soc(self) -> float:
        """Mean state of charge

        Returns:
            float: Mean state of charge (%)
        """
        _soc = 0
        for i in self._inverters:
            _soc += i.device.soc
        return _soc/len(self._inverters)

    @property
    def present_discharge(self) -> int:
        """Present amount of power being discharged

        Returns:
            int: discharging power (W)
        """
        _present_discharge = 0
        for i in self._inverters:
            _present_discharge += i.device.present_discharge
        return _present_discharge

    @property
    def present_charge(self) -> int:
        """Present amount of power being charged

        Returns:
            int: charging power (W)
        """
        _present_charge = 0
        for i in self._inverters:
            _present_charge += i.device.present_charge  # ! BUG
        return _present_charge

    @property
    def charge(self) -> int:
        """Charged energy in the batteries

        Returns:
            int: charged energy (Wh)
        """
        _charge = 0
        for i in self._inverters:
            _charge += i.device.present_charge  # ! BUG
        return _charge

    @property
    def total_capacity(self) -> int:
        """Total nominal capacity of all batteries

        Returns:
            int: Nominal capacity of all batteries (Wh)
        """
        _cap = 0
        for i in self._inverters:
            _cap += i.device.nomCapacity
        return _cap

    @property
    def charge_missing(self) -> int:
        """Total charge missing until batteries are full

        Returns:
            int: charge missing (Wh)
        """
        _charge_missing = 0
        for i in self._inverters:
            _charge_missing += i.device.nomCapacity - i.device.present_charge  # ! BUG
        return _charge_missing
