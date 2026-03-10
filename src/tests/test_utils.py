import math
from core.utils import clamp, toDegrees, toRadians
def test_utils() -> None:
	theta_rad = 0.275
	theta_deg = toDegrees(theta_rad)
	assert toRadians(theta_deg) == theta_rad

	to_clamp = 0.25
	assert clamp(to_clamp, 0.0, 0.1) == 0.1
	assert clamp(to_clamp, 0.5, 0.75) == 0.5
	assert clamp(to_clamp, 0, 0.5) == to_clamp