from BatteryManager import BatteryManager
from SMA_StorageBoy import SMA_StorageBoy


def main():
    sma_StorageBoy = SMA_StorageBoy("192.168.178.113")
    battery_manager = BatteryManager(inverters=[sma_StorageBoy])
    print("soc: "+str(battery_manager.soc))


if __name__ == "__main__":
    main()
