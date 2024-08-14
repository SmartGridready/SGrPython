from typing import Callable

from sgr_library.api import DataPointConverter
from sgr_library.converters.converter import HoursConverter, MinutesConverter, NoneConverter, SecondsConverter, TemperatureConverter, VoltDataPointConverter, UnsupportedConverter, \
    ReactiveEnergyConverter, PowerOverTimeConverter, CurrentConverter, PowerConverter, PercentConverter
from sgrspecification.generic import Units

converter_lookup: dict[Units, Callable[[Units], DataPointConverter]] = {
    Units.WATTS: lambda x: PowerConverter(x),
    Units.KILOWATTS: lambda x: PowerConverter(x),
    Units.VOLTS: lambda x: VoltDataPointConverter(x),
    Units.AMPERES: lambda x: CurrentConverter(x),
    Units.KILOVOLT_AMPERES_REACTIVE: lambda x: ReactiveEnergyConverter(x),
    Units.KILOVOLT_AMPERES: lambda x: ReactiveEnergyConverter(x),
    Units.KILOWATT_HOURS: lambda x: PowerOverTimeConverter(x),
    Units.KILOVOLT_AMPERES_REACTIVE_HOURS: lambda x: ReactiveEnergyConverter(x),
    Units.VOLT_AMPERES_REACTIVE: lambda x: ReactiveEnergyConverter(x),
    Units.HERTZ: lambda x : ReactiveEnergyConverter(x),
    Units.VOLT_AMPERES: lambda x: ReactiveEnergyConverter(x),

    Units.DEGREES_CELSIUS: lambda x: TemperatureConverter(x),

    Units.HOURS: lambda x: HoursConverter(x),
    Units.MINUTES: lambda x: MinutesConverter(x),
    Units.SECONDS: lambda x: SecondsConverter(x),

    Units.PERCENT: lambda x: PercentConverter(x),

    Units.NONE: lambda x: NoneConverter(x),

}


def build_converter(unit: Units) -> DataPointConverter:
    return converter_lookup.get(unit, lambda x: UnsupportedConverter(x))(unit)
