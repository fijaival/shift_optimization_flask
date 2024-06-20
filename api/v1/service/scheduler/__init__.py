from .hanazono.shift_scheduler import HanazonoFacilityOptimizeService
from .kuze.shift_scheduler import KuzeFacilityOptimizeService

facility_class_map = {
    1: HanazonoFacilityOptimizeService,
    2: KuzeFacilityOptimizeService
}
