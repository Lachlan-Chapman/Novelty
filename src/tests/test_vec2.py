import math
from core.vector import Vec2
def test_vec2() -> None:
	a = Vec2(1, 2)
	b = Vec2(3, 4)

	add_result = a + b
	assert add_result.x == a.x + b.x
	assert add_result.y == a.y + b.y

	sub_result = a - b
	assert sub_result.x == a.x - b.x
	assert sub_result.y == a.y - b.y

	mul_result = a * b
	assert mul_result.x == a.x * b.x
	assert mul_result.y == a.y * b.y

	mul_result = a * 2
	assert mul_result.x == a.x * 2
	assert mul_result.y == a.y * 2

	div_result = a / b
	assert div_result.x == a.x / b.x
	assert div_result.y == a.y / b.y

	div_result = a / 2
	assert div_result.x == a.x / 2
	assert div_result.y == a.y / 2

	assert a.dot(b) == (a.x * b.x) + (a.y * b.y)

	verified_mag = math.sqrt(a.x * a.x + a.y * a.y)
	assert a.magnitude == verified_mag
	assert a.lengthSquared == a.x * a.x + a.y * a.y

	assert a.normalised == Vec2(a.x / verified_mag, a.y / verified_mag)



