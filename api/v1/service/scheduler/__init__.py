from .hanazono import HanazonoFacilityOptimizeService
from .kuze import KuzeFacilityOptimizeService

facility_class_map = {
    1: HanazonoFacilityOptimizeService,
    2: KuzeFacilityOptimizeService
}
