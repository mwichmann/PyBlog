import math


class Vector(object):
    def __init__(self, value):
        self.angle = value

    @property
    def angle(self):
        return math.radians(self._angle_deg)

    @angle.setter
    def angle(self, value):
        self._angle_deg = math.degrees(value)

    @property
    def angle_deg(self):
        return self._angle_deg

    @angle_deg.setter
    def angle_deg(self, value):
        self._angle_deg = value


v = Vector(2*math.pi)
print("Rad: {}, Deg: {}".format(v.angle, v.angle_deg))

v.angle = math.pi
print("Rad: {}, Deg: {}".format(v.angle, v.angle_deg))

v.angle_deg = 90.0
print("Rad: {}, Deg: {}".format(v.angle, v.angle_deg))

print(Vector.angle, Vector.angle.getter, Vector.angle.setter)
print(Vector.angle_deg, Vector.angle_deg.getter, Vector.angle_deg.setter)
