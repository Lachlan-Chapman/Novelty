def clamp(p_value, p_min, p_max):
	if p_value < p_min:
		return p_min
	if p_value > p_max:
		return p_max
	return p_value

from src.vector import Vec2
class Collider:
	#simple distance check
	def collideCircleCirlce(self, p_a, p_b) -> bool:
		delta = Vec2(
			(p_a.m_position.x - p_b.m_position.x),
			(p_a.m_position.y - p_b.m_position.y)
		)
		radius = p_a.m_radius + p_b.m_radius
		return (delta.x * delta.x + delta.y * delta.y) <= radius * radius
	
	def collideRectangleRectangle(self, p_a, p_b):
		delta = Vec2(
			abs(p_a.m_position.x - p_b.m_position.x),
			abs(p_a.m_position.y - p_b.m_position.y)
		)

		#is distance between centers closer then the combined half sizes, if so edges are overlapping
		overlap_x = delta.x <= (p_a.m_dimensions.x * 0.5 + p_b.m_dimensions.x * 0.5)
		overlap_y = delta.y <= (p_a.m_dimensions.y * 0.5 + p_b.m_dimensions.y * 0.5)
	
		return overlap_x and overlap_y

	def collideCircleRectangle(self, p_circle, p_rectangle):
		min_rect = Vec2(
			(p_rectangle.m_position.x - p_rectangle.m_dimensions.x * 0.5),
			(p_rectangle.m_position.y - p_rectangle.m_dimensions.y * 0.5)
		)
		max_rect = Vec2(
			(p_rectangle.m_position.x + p_rectangle.m_dimensions.x * 0.5),
			(p_rectangle.m_position.y + p_rectangle.m_dimensions.y * 0.5)
		)

		closest = Vec2(
			clamp(p_circle.m_position.x, min_rect.x, max_rect.x),
			clamp(p_circle.m_position.y, min_rect.y, max_rect.y) 
		)

		delta = Vec2(
			(p_circle.m_position.x - closest.x),
			(p_circle.m_position.y - closest.y)
		)

		return delta.x * delta.x + delta.y * delta.y <= p_circle.m_radius * p_circle.m_radius
	
	def overlaps(self, p_a, p_b):
		if p_a.m_shape == "circle" and p_b.m_shape == "circle":
			#print("circle circle collide")
			return self.collideCircleCirlce(p_a, p_b)
		
		if p_a.m_shape == "circle" and p_b.m_shape == "rectangle":
			#print("circle circle rectangle")
			return self.collideCircleRectangle(p_a, p_b)
		
		if p_a.m_shape == "rectangle" and p_b.m_shape == "circle":
			#print("rectangle circle collide")
			return self.collideCircleRectangle(p_b, p_a)
		
		if p_a.m_shape == "rectangle" and p_b.m_shape == "rectangle":
			#print("rectangle rectangle collide")
			return self.collideRectangleRectangle(p_a, p_b)
		return False #default if its not one of those types
	
	def collideSAT(self, p_a, p_b):
		p_a.updateGeometry() #only SAT needs vertices and normals to be accurate, so this allows for only doing all that math each collision over each frame
		p_b.updateGeometry() #make sure shapes vertices and surface are all set before we start doing collision logic
		edge_normals = p_a.getEdgeNormals() + p_b.getEdgeNormals() #combined lists of both shapes local axes
		for axis in edge_normals:
			a_min_max = p_a.project(axis)
			b_min_max = p_b.project(axis)

			if a_min_max.y < b_min_max.x or b_min_max.y < a_min_max.x:
				return False #found at least 1 axis they dont touch on
		return True