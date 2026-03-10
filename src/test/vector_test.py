from core.vector import Vec2
def vec2_arithmetic() -> None:
	a = Vec2(1, 2)
	b = Vec2(3, 4)

	add_result = a + b
	assert add_result.x == 4
	assert add_result.y == 6

	sub_result = a - b
	assert sub_result.x == -2
	assert sub_result.y == -2

	mul_result = a * b
	