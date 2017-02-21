import math


class Vector(object):
    def __init__(self, angle_rad):
        self.set_angle_rad(angle_rad)

    def get_angle_rad(self):
        return math.radians(self._angle_deg)

    def set_angle_rad(self, angle_rad):
        self._angle_deg = math.degrees(angle_rad)

    angle = property(get_angle_rad, set_angle_rad)

    def get_angle_deg(self):
        return self._angle_deg

    def set_angle_deg(self, angle_deg):
        self._angle_deg = angle_deg

    angle_deg = property(get_angle_deg, set_angle_deg)


v = Vector(2 * math.pi)
print(v.angle)
print(v.angle_deg)

v.angle = math.pi
print(v.angle)
print(v.angle_deg)

print(Vector.angle, Vector.angle.getter, Vector.angle.setter)
print(Vector.angle_deg, Vector.angle_deg.getter, Vector.angle_deg.setter)
