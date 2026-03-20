class Groups: #limited by 32 groups since we are using 1 bit per group and ints
	PLAYER: int = 1 << 0
	ENEMY: int = 1 << 1
	PROJECTILE: int = 1 << 2