from dataclasses import dataclass, field
from typing import List, Optional
from data_classes.generic.sgr_enum_profile_type import ProfileTypeEnumType
from data_classes.generic.sgr_enum_sub_profile_type import SubProfileTypeEnumType
from data_classes.generic.sgr_gen_type_definitions import (
    SgrLegibDocumentationType,
    SgrMropresenceLevelIndicationType,
    SgrNamelistType,
    SgrVersionNumberType,
)

__NAMESPACE__ = "http://www.smartgridready.com/ns/V0/"


@dataclass
class SgrProfilenumberType:
    """Specification of design source 0 means: specified by SmartGridready, the
    Porfilenumber follows the SmargGirdready scheme.

    &gt;0 means: specfied by manufacturer hhhh, the Profilenumber
    followos a manufacturors scheme

    :ivar specs_owner_id: This number idntifies the creator of this
        instance definition 0 means "This is a SmartGridready
        specification, SGr definition are valid" means "designed and
        manufaturer hhhh" and a seperate set of definitions created by
        the manufacturer is valid The profile number
        hhhh.nnnn.uuuu.ss.VV.vv is documented in the SGr profile
        specification number
    :ivar profile_identification: The Profile Identfication identiofis
        the main profile classes. The enumeration text is also
        documented with numbers being referenced in the profile number
        hhhh.nnnn.uuuu.ss.VV.vv as nnnn
    :ivar sub_profile_ident:
    :ivar sgr_level_of_operation: SGrLevelOfOperation defines a controls
        complexity level 1) single contact 2) 2 or more contacts /state
        controlled interface 3) statical defined characteristics tables
        4) dynamic realtime control combined with statical defined
        characteristics tables 5) dynamic realtime control combined with
        dynamic changeable characteristics tables 6) prognosis based
        systems
    :ivar version_number:
    """
    class Meta:
        name = "SGrProfilenumberType"

    specs_owner_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "specsOwnerId",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    profile_identification: Optional[ProfileTypeEnumType] = field(
        default=None,
        metadata={
            "name": "profileIdentification",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    sub_profile_ident: Optional[SubProfileTypeEnumType] = field(
        default=None,
        metadata={
            "name": "subProfileIdent",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    sgr_level_of_operation: Optional[int] = field(
        default=None,
        metadata={
            "name": "sgrLevelOfOperation",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    version_number: Optional[SgrVersionNumberType] = field(
        default=None,
        metadata={
            "name": "versionNumber",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )


@dataclass
class SgrProfileDescriptionType:
    """
    Profile Element for to be used for the generation of SGrGenericDevices and
    the Ecore modelling the generation of the generic profile level interface
    class Profil Element zur Integration in generische Gerätedefinitionen oder
    zur Erzeugung von ecore-Modellierungen.

    :ivar profile_number:
    :ivar fp_name_list:
    :ivar fp_legib_desc: this is the published information related to
        this functional profile
    :ivar fp_prg_desc:
    :ivar profile_name:
    :ivar mro_visibility_indicator:
    """
    class Meta:
        name = "SGrProfileDescriptionType"

    profile_number: Optional[SgrProfilenumberType] = field(
        default=None,
        metadata={
            "name": "profileNumber",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "required": True,
        }
    )
    fp_name_list: Optional[SgrNamelistType] = field(
        default=None,
        metadata={
            "name": "fpNameList",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
        }
    )
    fp_legib_desc: List[SgrLegibDocumentationType] = field(
        default_factory=list,
        metadata={
            "name": "fpLegibDesc",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )
    fp_prg_desc: List[SgrLegibDocumentationType] = field(
        default_factory=list,
        metadata={
            "name": "fpPrgDesc",
            "type": "Element",
            "namespace": "http://www.smartgridready.com/ns/V0/",
            "max_occurs": 4,
        }
    )
    profile_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "profileName",
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
