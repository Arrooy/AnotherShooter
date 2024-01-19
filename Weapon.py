import time
from Bullet import Bullet, GranadeBullet

class Weapon():
    def __init__(self, parent, max_bullet_speed=25, range=100, attack_speed_ms=150, damage=1, bullet_size=25) -> None:
        self.id = parent.id
        self.parent = parent
        self.max_bullet_speed = max_bullet_speed    
        self.range = range
        self.damage = damage
        self.bullet_size = bullet_size
        self.attack_speed_ms = attack_speed_ms
        self.last_attack_time = time.time_ns()

        
    def shootBullet(self, angle):
        if time.time_ns() - self.last_attack_time >= 1_000_000 * self.attack_speed_ms:
            self.last_attack_time = time.time_ns()
            Bullet(self.parent, angle, self.max_bullet_speed, self.range, self.damage, self.bullet_size)

class Shotgun(Weapon):
    def __init__(self, parent, max_bullet_speed=20, range=35,  attack_speed_ms=500, damage=1, bullet_size=10) -> None:
        super().__init__(parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size)
        
    def shootBullet(self, angle):
        if time.time_ns() - self.last_attack_time >= 1_000_000 * self.attack_speed_ms:
            self.last_attack_time = time.time_ns()
            for i in range(-2,2):
                Bullet(self.parent, angle + i * 3, self.max_bullet_speed, self.range, self.damage, self.bullet_size)

class GranadeLauncher(Weapon):
    def __init__(self, parent, max_bullet_speed=20, range=25,  attack_speed_ms=200, damage=2, bullet_size=10) -> None:
        super().__init__(parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size)
    
    def shootBullet(self, angle):
        if time.time_ns() - self.last_attack_time >= 1_000_000 * self.attack_speed_ms:
            self.last_attack_time = time.time_ns()
            GranadeBullet(self.parent, angle, self.max_bullet_speed, self.range, self.damage, self.bullet_size)

class Rocket(Weapon):
    def __init__(self, parent, max_bullet_speed=10, range=45, attack_speed_ms=2500, damage=5, bullet_size=50) -> None:
        super().__init__(parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size)
    
class MachineGun(Weapon):
    def __init__(self, parent, max_bullet_speed=25, range=75, attack_speed_ms=50, damage=0.5, bullet_size=5) -> None:
        super().__init__(parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size)

class Sniper(Weapon):
    def __init__(self, parent, max_bullet_speed=45, range=75, attack_speed_ms=2000, damage=5, bullet_size=7) -> None:
        super().__init__(parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size)