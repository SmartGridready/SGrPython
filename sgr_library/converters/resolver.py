from typing import Callable

from sgr_library.api import DataPointConverter
from sgr_library.converters.converter import VoltDataPointConverter, UnsupportedConverter, \
    ReactiveEnergyConverter, PowerOverTimeConverter, CurrentConverter, PowerConverter, PercentConverter
from sgr_library.data_classes.generic import Units

converter_lookup: dict[Units, Callable[[Units], DataPointConverter]] = {
    Units.VOLTS: lambda x: VoltDataPointConverter(x),
    Units.MEGAVOLTS: lambda x: VoltDataPointConverter(x),
    Units.KILOVOLTS: lambda x: VoltDataPointConverter(x),
    Units.MILLIVOLTS: lambda x: VoltDataPointConverter(x),
    Units.VOLT_AMPERES_REACTIVE: lambda x: ReactiveEnergyConverter(x),
    Units.MEGAVOLT_AMPERES_REACTIVE: lambda x: ReactiveEnergyConverter(x),
    Units.KILOVOLT_AMPERES_REACTIVE: lambda x: ReactiveEnergyConverter(x),
    Units.KILOWATT_HOURS: lambda x: PowerOverTimeConverter(x),
    Units.WATT_HOURS: lambda x: PowerOverTimeConverter(x),
    Units.MEGAWATT_HOURS: lambda x: PowerOverTimeConverter(x),
    Units.AMPERES: lambda x: CurrentConverter(x),
    Units.MILLIAMPERES: lambda x: CurrentConverter(x),
    Units.HORSEPOWER: lambda x: PowerConverter(x),
    Units.WATTS: lambda x: PowerConverter(x),
    Units.MEGAWATTS: lambda x: PowerConverter(x),
    Units.KILOWATTS: lambda x: PowerConverter(x),
    Units.KILOVOLT_AMPERES: lambda x: PowerConverter(x),
    Units.VOLT_AMPERES: lambda x: PowerConverter(x),
    Units.MEGAVOLT_AMPERES: lambda x: PowerConverter(x),
    Units.PERCENT: lambda x: PercentConverter(x),
}


def build_converter(unit: Units) -> DataPointConverter:
    return converter_lookup.get(unit, lambda x: UnsupportedConverter(x))(unit)
