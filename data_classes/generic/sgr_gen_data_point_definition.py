from dataclasses import dataclass, field
from typing import List, Optional
from data_classes.generic.sgr_gen_type_definitions import (
    SgrBasicGenArrayDptypeType,
    SgrBasicGenDataPointTypeType,
    SgrLegibDocumentationType,
    SgrMropresenceLevelIndicationType,
    SgrNamelistType,
    SgrRwptype,
    SgrUnits,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class SgrDataPointDescriptionType:
    """This schema sheet serves the generation of the data point for to define
    a single data point, its type and links to potential attributes.

    Dieses Schema dient der Erzeugung eines einzelnen Datenpunktes zur
    Definition des Datentyps und der Verbindung mit möglichen
    Attributen.

    :ivar basic_data_type:
    :ivar basic_array_data_type:
    :ivar dp_name_list:
    :ivar dp_legib_desc: this is the public explanation of the
        functionlity of this Datapoint
    :ivar dp_prg_desc:
    :ivar datapoint_name: Bezeichnung des Datenpunktes: «Schlagwort»,
        welches die Bedeutung identifiziert. Diese Bezeichnung gilt
        neben der Indexnummer als Definition für den SmartGridready
        Namespace für die maschinenlesbaren Daten.
    :ivar rwp_datadirection: RWP (Eigenschaft des Datenpunktes)
        bezeichnet die Datenrichtung und die Datenhaltung R = lesen aus
        Sicht des Profilnutzers W = schreiben aus Sicht der
        Profilnutzers P = persistente Speicherung der Daten
    :ivar mro_visibility_indicator: MRO (Relevanz) Die Gewichtung der
        Variable bezüglich des Nutzens M = muss (mandatory) Datenpunkt R
        = empfohlener (recommended) Datenpunkt O = optionaler Datenpunkt
    :ivar unit:
    """
    class Meta:
        name = "SGrDataPointDescriptionType"

    basic_data_type: Optional[SgrBasicGenDataPointTypeType] = field(
        default=None,
        metadata={
            "name": "basicDataType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    basic_array_data_type: Optional[SgrBasicGenArrayDptypeType] = field(
        default=None,
        metadata={
            "name": "basicArrayDataType",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    dp_name_list: Optional[SgrNamelistType] = field(
        default=None,
        metadata={
            "name": "dpNameList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    dp_legib_desc: List[SgrLegibDocumentationType] = field(
        default_factory=list,
        metadata={
            "name": "dpLegibDesc",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )
    dp_prg_desc: List[SgrLegibDocumentationType] = field(
        default_factory=list,
        metadata={
            "name": "dpPrgDesc",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )
    datapoint_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "datapointName",
            "type": "Attribute",
        }
    )
    rwp_datadirection: Optional[SgrRwptype] = field(
        default=None,
        metadata={
            "name": "rwpDatadirection",
            "type": "Attribute",
        }
    )
    mro_visibility_indicator: Optional[SgrMropresenceLevelIndicationType] = field(
        default=None,
        metadata={
            "name": "mroVisibilityIndicator",
            "type": "Attribute",
        }
    )
    unit: Optional[SgrUnits] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
