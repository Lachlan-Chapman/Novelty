from core.vector import Vec2

#a method of python that autogenerates a class to store data only with operator overloads | i wanna do it my self
# from dataclasses import dataclass
# @dataclass
# class Transform:
# 		position: Vec2
# 		rotation: float
# 		size: Vec2

class Transform:
	def __init__(
		self,
		p_position: Vec2 | None = None,
		p_rotation: float | None = None,
		p_size: Vec2 | None = None
	):
		self.position: Vec2 = p_position if p_position is not None else Vec2(0.0, 0.0)
		self.rotation: float = p_rotation if p_rotation is not None else 0.0
		self.size: Vec2 = p_size if p_size is not None else Vec2(0.0, 0.0)