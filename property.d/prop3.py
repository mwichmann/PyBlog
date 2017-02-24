import math


class Vector(object):
    def __init__(self, value):
        self.angle = value

    @property
    def angle(self):
        return math.radians(self.angle_deg)

    @angle.setter
    def angle(self, value):
        self.angle_deg = math.degrees(value)


v = Vector(2 * math.pi)
print("Rad: {}, Deg: {}".format(v.angle, v.angle_deg))

v.angle = math.pi
print("Rad: {}, Deg: {}".format(v.angle, v.angle_deg))

v.angle_deg = 90.0
print("Rad: {}, Deg: {}".format(v.angle, v.angle_deg))
