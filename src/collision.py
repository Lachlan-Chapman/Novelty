from src.vector import Vec2
class CircleCollider:
	def __init__(self, p_position: Vec2, p_radius: float):
		self.m_position = p_position
		self.m_radius = p_radius
	
	def hit(self, p_other) -> bool:
		dist = p_other.m_postion - self.m_position
		mag = dist.magnitude()
		if mag <= 2*self.m_radius:
			return True
		return False 