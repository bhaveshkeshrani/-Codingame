import sys
import math

X_MAX = 16000
Y_MAX = 9000
CARS_COUNT = 2


def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Point(object):
    """ Point class: Reprepsents a point in the x, y, z space. """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '{0}({1}, {2}, {3})'.format(self.__class__.__name__, self.x,
                                           self.y, self.z)

    def substract(self, point):
        """ Return a Point instance as the displacement of two points. """
        return Point(point.x - self.x, point.y - self.y, point.z - self.z)

    @classmethod
    def from_list(cls, l):
        """ Return a Point instance from a given list """

        x, y, z = map(float, l)
        return cls(x, y, z)


class Vector(Point):
    """ Vector class: Represents a vector in the x, y, z space. """

    def __init__(self, x, y, z=0):
        self.vector = [x, y, z]
        super(Vector, self).__init__(x, y, z)

    def add(self, number):
        """ Return a Vector instance as the product of the vector and a real
            number. """

        return self.from_list([x + number for x in self.vector])

    def multiply(self, number):
        """ Return a Vector instance as the product of the vector and a real
            number. """

        return self.from_list([x * number for x in self.vector])

    def magnitude(self):
        """ Return magnitude of the vector. """

        return (math.sqrt(reduce(lambda x, y: x + y,
                                 [x ** 2 for x in self.vector])))

    def sum(self, vector):
        """ Return a Vector instance as the vector sum of two vectors. """

        return (self.from_list([x + vector.vector[self.vector.index(x)]
                                for x in self.vector]))

    def substract(self, vector):
        """ Return a Vector instance as the vector difference of two vectors.
        """

        return (self.from_list([vector.vector[self.vector.index(x)] - x for x in
                                self.vector]))

    def dot(self, vector, theta=None):
        """ Return the dot product of two vectors. If theta is given then the
        dot product is computed as v1*v1 = |v1||v2|cos(theta). Argument theta
        is measured in degrees. """

        if theta is not None:
            return (self.magnitude() * vector.magnitude() *
                    math.degrees(math.cos(theta)))
        return (reduce(lambda x, y: x + y,
                       [x * vector.vector[self.vector.index(x)]
                        for x in self.vector]))

    def cross(self, vector):
        """ Return a Vector instance as the cross product of two vectors """

        return Vector((self.y * vector.z - self.z * vector.y),
                      (self.z * vector.x - self.x * vector.z),
                      (self.x * vector.y - self.y * vector.x))

    def angle(self, vector):
        """ Return the angle between two vectors in degrees. """

        return (math.degrees(math.acos((self.dot(vector) / (self.magnitude() *
                                                            vector.magnitude())))))

    def parallel(self, vector):
        """ Return True if vectors are parallel to each other. """

        if self.cross(vector).magnitude() == 0:
            return True
        return False

    def perpendicular(self, vector):
        """ Return True if vectors are perpendicular to each other. """

        if self.dot(vector) == 0:
            return True
        return False

    def non_parallel(self, vector):
        """ Return True if vectors are non-parallel. Non-parallel vectors are
            vectors which are neither parallel nor perpendicular to each other.
        """

        if (self.is_parallel(vector) is not True and
                    self.is_perpendicular(vector) is not True):
            return True
        return False

    @classmethod
    def from_points(cls, point1, point2):
        """ Return a Vector instance from two given points. """

        if isinstance(point1, Point) and isinstance(point2, Point):
            displacement = point1.substract(point2)
            return cls(displacement.x, displacement.y, displacement.z)
        raise TypeError


class Path():
    x = None
    y = None
    trust = None

    def set_path(self, x, y, trust):
        self.x, self.y, self.trust = x, y, trust

    def get_string(self):
        print("{0} {1} {2}".format(self.x, self.y, self.trust))


class Area():
    checkpoints = []
    checkpoint_count = 0
    laps = 0

    def __init__(self):
        self.laps = int(input())
        self.checkpoint_count = int(input())
        for i in range(self.checkpoint_count):
            checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
            self.checkpoints.append({'x': checkpoint_x, 'y': checkpoint_y})

    def get_checkpoint_by_id(self, i):
        return self.checkpoints[i]

    def get_laps_count(self):
        return self.laps

    def get_checkpoint_count(self):
        return self.checkpoint_count

class Player():
    _title = ''
    x = int(X_MAX / 2)
    y = int(Y_MAX / 2)
    vx = vy = angle = next_check_point_id = 0
    boost_not_used = True
    calculated_skidding_vector = None
    calculated_path = Path()
    calculated_lap = 0

    def __init__(self, title):
        self._title = title

    def scan_data(self):
        # x: x position of your pod
        # y: y position of your pod
        # vx: x speed of your pod
        # vy: y speed of your pod
        # angle: angle of your pod
        # next_check_point_id: next check point id of your pod
        from_x, from_y = self.x, self.y
        self.x, self.y, self.vx, self.vy, self.angle, self.next_check_point_id = [int(j) for j in input().split()]
        self.calculated_skidding_vector = Vector(from_x, from_y, 0).substract(
            Vector(self.x, self.y, 0))  # .multiply(self.next_checkpoint_dist)

    def calculate_path(self, area):
        angle_abs = abs(self.angle)
        next_checkpoint = area.get_checkpoint_by_id(self.next_check_point_id)
        laps_count = area.get_laps_count()
        checkpoint_count = area.get_checkpoint_count()
        next_checkpoint_dist = dist(self.x, self.y, next_checkpoint['x'], next_checkpoint['y'])
        if (angle_abs > 90):
            self.calculated_path.set_path(next_checkpoint['x'], next_checkpoint['y'], 0)
        elif ((next_checkpoint_dist > 6000 or (
                checkpoint_count == self.next_check_point_id and laps_count == self.calculated_lap)) and angle_abs < 5 and self.boost_not_used):
            self.boost_not_used = False
            self.calculated_path.set_path(next_checkpoint['x'], next_checkpoint['y'], "BOOST")
        else:
            thrust = 100
            if next_checkpoint_dist < 2500:
                thrust = 50

            if next_checkpoint_dist < 1000:
                thrust = 100

            x, y = self.correct_path(next_checkpoint)
            self.calculated_path.set_path(x, y, thrust)
            # Vectors Logik starts from here

    def correct_path(self, next_checkpoint):
        target_vector = Vector(next_checkpoint['x'], next_checkpoint['y'], 0)
        if self.calculated_skidding_vector.x > 10000:
            corection_vector = target_vector
        else:
            corection_vector = target_vector.sum(self.calculated_skidding_vector.multiply(-1))
        corection_vector = target_vector
        # print(movement_vector, file=sys.stderr)
        # print(self.next_checkpoint_x, self.next_checkpoint_y, file=sys.stderr)
        return [int(corection_vector.x), int(corection_vector.y)]

class Act():
    players = []
    opponents = []
    area = None

    def __init__(self):
        for i in range(CARS_COUNT):
            self.opponents.append(Player('Opponent#' + str(i)))
            self.players.append(Player('Player#' + str(i)))
        self.area = Area()

    def get_players_data(self):
        for i in range(CARS_COUNT):
            self.players[i].scan_data()

    def get_oponents_data(self):
        for i in range(CARS_COUNT):
            self.opponents[i].scan_data()

    def calculate_path(self):
        for i in range(CARS_COUNT):
            self.players[i].calculate_path(self.area)

    def run(self):
        for i in range(CARS_COUNT):
            self.players[i].calculated_path.get_string()

action = Act()
while True:
    action.get_players_data()
    action.get_oponents_data()
    action.calculate_path()
    action.run()
