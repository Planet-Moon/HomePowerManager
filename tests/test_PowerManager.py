from PowerManager import PowerManager
from SMA_StorageBoy import SMA_StorageBoy
from BatteryManager import BatteryManager
from SimulationExamples import Source, Sink


def main():
    storage_boy = SMA_StorageBoy("192.168.178.113")
    sim_source_1 = Source("source1")
    sim_sink_1 = Sink("sink1")
    sim_sink_1.request_power = 50000
    sim_sink_2 = Sink("sink2")
    sim_sink_2.request_power = 2000
    battery_manager = BatteryManager(inverters=[storage_boy])
    sources = [battery_manager, sim_source_1]
    sinks = [sim_sink_1, sim_sink_2]
    power_manager = PowerManager(sources=sources, sinks=sinks)
    sinks.append(Sink("sink3"))
    power_manager.power_grid = lambda: storage_boy.LeistungBezug - \
        storage_boy.LeistungEinspeisung
    power_manager.distribute()
    print("power distribution: {}".format(power_manager._power_distribution))


if __name__ == "__main__":
    main()
