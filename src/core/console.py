class Console:
	def info(self, p_message: str):
		print(f"[INFO] {p_message}")
	
	def warn(self, p_message: str):
		print(f"[WARN] {p_message}")

	def error(self, p_message: str):
		print(f"[ERROR] {p_message}")

CONSOLE = Console()