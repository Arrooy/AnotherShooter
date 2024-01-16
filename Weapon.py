import time
from Bullet import Bullet, GranadeBullet

class Weapon():
    def __init__(self, parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size) -> None:
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
    def __init__(self, parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size) -> None:
        super().__init__(parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size)
        
    def shootBullet(self, angle):
        if time.time_ns() - self.last_attack_time >= 1_000_000 * self.attack_speed_ms:
            self.last_attack_time = time.time_ns()
            for i in range(-2,2):
                Bullet(self.parent, angle + i * 3, self.max_bullet_speed, self.range, self.damage, self.bullet_size)

class GranadeLauncher(Weapon):
    def __init__(self, parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size) -> None:
        super().__init__(parent, max_bullet_speed, range, attack_speed_ms, damage, bullet_size)
    
    def shootBullet(self, angle):
        if time.time_ns() - self.last_attack_time >= 1_000_000 * self.attack_speed_ms:
            self.last_attack_time = time.time_ns()
            GranadeBullet(self.parent, angle, self.max_bullet_speed, self.range, self.damage, self.bullet_size)
