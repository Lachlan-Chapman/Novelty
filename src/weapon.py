class Weapon:
	def __init__(self, p_name: str = "Weapon", p_bulletSpeed: float = 100.0, p_fireRate: float = 1.0,  p_magazineSize: int = 10.0, p_reloadTime: float = 3.0):
		self.m_name = p_name
		self.m_bulletSpeed = p_bulletSpeed
		self.m_fireRate = p_fireRate
		self.m_magazineSize = p_magazineSize
		self.m_bulletCount = p_magazineSize
		self.m_reloadTime = p_reloadTime

	def shoot(self):
		print(f"{self.m_name} Shoots")
		#raise NotImplementedError #child must create specific shoot, no default shots