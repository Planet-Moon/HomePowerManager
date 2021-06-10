from PowerManager import PowerManager
from SMA_StorageBoy import SMA_StorageBoy
from SMA_SunnyBoy import SMA_SunnyBoy
from BatteryManager import BatteryManager
from SimulationExamples import ExamplePowerSource, ExamplePowerSink

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(threadName)s %(filename)s %(lineno)d: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    storage_boy = SMA_StorageBoy("192.168.178.113")
    sunny_boy = SMA_SunnyBoy("192.168.178.128", "sunny_boy")
    sim_source_1 = ExamplePowerSource("source1")
    sim_sink_1 = ExamplePowerSink("sink1")
    sim_sink_1.request_power = 50000
    sim_sink_2 = ExamplePowerSink("sink2")
    sim_sink_2.request_power = (1500, 1800)
    battery_manager = BatteryManager(inverters=[storage_boy])
    sources = [battery_manager, sunny_boy, sim_source_1]
    sinks = [sim_sink_1, sim_sink_2]
    power_manager = PowerManager(sources=sources, sinks=sinks)
    sinks.append(ExamplePowerSink("sink3"))
    power_manager.power_grid = lambda: storage_boy.LeistungBezug - \
        storage_boy.LeistungEinspeisung
    power_manager.distribute()
    logger.error("power distribution: {}".format(power_manager._power_distribution))


if __name__ == "__main__":
    main()
