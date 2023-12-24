import geometry
import math
import pytest


class TestVector:

    def test_magnitude_origin(self, vector_origin):
        assert vector_origin.magnitude == 0

    def test_magnitude_1st_quad(self, vector_1st_quad):
        assert vector_1st_quad.magnitude == math.sqrt(1 + 4 + 9)

    def test_magnitude_2nd_quad(self, vector_2nd_quad):
        assert vector_2nd_quad.magnitude == math.sqrt(1 + 4 + 9)

    def test_magnitude_3rd_quad(self, vector_3rd_quad):
        assert vector_3rd_quad.magnitude == math.sqrt(1 + 4 + 9)

    def test_magnitude_4th_quad(self, vector_4th_quad):
        assert vector_4th_quad.magnitude == math.sqrt(1 + 4 + 9)

    def test_angleXY_1st_quad(self, vector_1st_quad):
        assert vector_1st_quad.angleXY == math.atan2(vector_1st_quad.y, vector_1st_quad.x)

    def test_angleXY_2nd_quad(self, vector_2nd_quad):
        assert vector_2nd_quad.angleXY == math.atan2(vector_2nd_quad.y, vector_2nd_quad.x)

    def test_angleXY_3rd_quad(self, vector_3rd_quad):
        assert vector_3rd_quad.angleXY == math.atan2(vector_3rd_quad.y, vector_3rd_quad.x)

    def test_angleXY_4th_quad(self, vector_4th_quad):
        assert vector_4th_quad.angleXY == math.atan2(vector_4th_quad.y, vector_4th_quad.x)

    def test_equals(self, vector_1st_quad, vector_2nd_quad, vector_3rd_quad, vector_4th_quad):
        v1 = vector_1st_quad.clone()
        v2 = vector_2nd_quad.clone()
        v2.x = v1.x
        v2.y = v1.y
        v2.z = v1.z

        assert vector_1st_quad == v1
        assert vector_1st_quad == v2
        assert vector_1st_quad != vector_2nd_quad
        assert vector_1st_quad != vector_3rd_quad
        assert vector_1st_quad != vector_4th_quad

    def test_iadd_1st_quad(self, vector_1st_quad: geometry.Vector):
        v = vector_1st_quad.clone()
        v += geometry.Vector(1, 2, 3)

        assert v == geometry.Vector(2, 4, 6)

    def test_iadd_2nd_quad(self, vector_2nd_quad: geometry.Vector):
        v = vector_2nd_quad.clone()
        v += geometry.Vector(1, 2, 3)

        assert v == geometry.Vector(2, 0, 6)

    def test_iadd_3rd_quad(self, vector_3rd_quad: geometry.Vector):
        v = vector_3rd_quad.clone()
        v += geometry.Vector(1, 2, 3)

        assert v == geometry.Vector(0, 0, 6)

    def test_iadd_4th_quad(self, vector_4th_quad: geometry.Vector):
        v = vector_4th_quad.clone()
        v += geometry.Vector(1, 2, 3)

        assert v == geometry.Vector(0, 4, 6)

    def test_imul_1st_quad(self, vector_1st_quad: geometry.Vector):
        v = vector_1st_quad.clone()
        v *= 2

        assert v == geometry.Vector(2, 4, 6)

    def test_imul_2nd_quad(self, vector_2nd_quad: geometry.Vector):
        v = vector_2nd_quad.clone()
        v *= 2

        assert v == geometry.Vector(2, -4, 6)

    def test_imul_3rd_quad(self, vector_3rd_quad: geometry.Vector):
        v = vector_3rd_quad.clone()
        v *= 2

        assert v == geometry.Vector(-2, -4, 6)

    def test_imul_4th_quad(self, vector_4th_quad: geometry.Vector):
        v = vector_4th_quad.clone()
        v *= 2

        assert v == geometry.Vector(-2, 4, 6)

    def test_itruediv_1st_quad(self, vector_1st_quad: geometry.Vector):
        v = vector_1st_quad.clone()
        v /= 2

        assert v == geometry.Vector(0.5, 1, 1.5)

    def test_itruediv_2nd_quad(self, vector_2nd_quad: geometry.Vector):
        v = vector_2nd_quad.clone()
        v /= 2

        assert v == geometry.Vector(0.5, -1, 1.5)

    def test_itruediv_3rd_quad(self, vector_3rd_quad: geometry.Vector):
        v = vector_3rd_quad.clone()
        v /= 2

        assert v == geometry.Vector(-0.5, -1, 1.5)

    def test_itruediv_4th_quad(self, vector_4th_quad: geometry.Vector):
        v = vector_4th_quad.clone()
        v /= 2

        assert v == geometry.Vector(-0.5, 1, 1.5)

    def test_rotateXY_1st_quad_pos(self, vector_1st_quad: geometry.Vector):
        # Verified via https://www.vcalc.com/wiki/vCalc/V3+-+Vector+Rotation
        v = vector_1st_quad.rotateXY(math.pi / 4)

        assert v.x == pytest.approx(-0.7071, 0.0001)
        assert v.y == pytest.approx(2.1213, 0.0001)
        assert v.angleXY == pytest.approx(vector_1st_quad.angleXY + (math.pi / 4))

    def test_rotateXY_1st_quad_neg(self, vector_1st_quad: geometry.Vector):
        # Verified via https://www.vcalc.com/wiki/vCalc/V3+-+Vector+Rotation
        v = vector_1st_quad.rotateXY(-math.pi / 4)

        assert v.x == pytest.approx(2.1213, 0.0001)
        assert v.y == pytest.approx(0.7071, 0.0001)
        assert v.angleXY == pytest.approx(vector_1st_quad.angleXY - (math.pi / 4))

    def test_rotateXY_2nd_quad_pos(self, vector_2nd_quad: geometry.Vector):
        # Verified via https://www.vcalc.com/wiki/vCalc/V3+-+Vector+Rotation
        v = vector_2nd_quad.rotateXY(math.pi / 4)

        assert v.x == pytest.approx(2.1213, 0.0001)
        assert v.y == pytest.approx(-0.7071, 0.0001)
        assert v.angleXY == pytest.approx(vector_2nd_quad.angleXY + (math.pi / 4))

    def test_rotateXY_2nd_quad_neg(self, vector_2nd_quad: geometry.Vector):
        # Verified via https://www.vcalc.com/wiki/vCalc/V3+-+Vector+Rotation
        v = vector_2nd_quad.rotateXY(-math.pi / 4)

        assert v.x == pytest.approx(-0.7071, 0.0001)
        assert v.y == pytest.approx(-2.1213, 0.0001)
        assert v.angleXY == pytest.approx(vector_2nd_quad.angleXY - (math.pi / 4))

    def test_rotateXY_3rd_quad_pos(self, vector_3rd_quad: geometry.Vector):
        # Verified via https://www.vcalc.com/wiki/vCalc/V3+-+Vector+Rotation
        v = vector_3rd_quad.rotateXY(math.pi / 4)

        assert v.x == pytest.approx(0.7071, 0.0001)
        assert v.y == pytest.approx(-2.1213, 0.0001)
        assert v.angleXY == pytest.approx(vector_3rd_quad.angleXY + (math.pi / 4))

    def test_rotateXY_3rd_quad_neg(self, vector_3rd_quad: geometry.Vector):
        # Verified via https://www.vcalc.com/wiki/vCalc/V3+-+Vector+Rotation
        v = vector_3rd_quad.rotateXY(-math.pi / 4)

        assert v.x == pytest.approx(-2.1213, 0.0001)
        assert v.y == pytest.approx(-0.7071, 0.0001)
        assert v.angleXY == pytest.approx(vector_3rd_quad.angleXY - (math.pi / 4))

    def test_rotateXY_4th_quad_pos(self, vector_4th_quad: geometry.Vector):
        # Verified via https://www.vcalc.com/wiki/vCalc/V3+-+Vector+Rotation
        v = vector_4th_quad.rotateXY(math.pi / 4)

        assert v.x == pytest.approx(-2.1213, 0.0001)
        assert v.y == pytest.approx(0.7071, 0.0001)
        assert v.angleXY == pytest.approx(vector_4th_quad.angleXY + (math.pi / 4))

    def test_rotateXY_4th_quad_neg(self, vector_4th_quad: geometry.Vector):
        # Verified via https://www.vcalc.com/wiki/vCalc/V3+-+Vector+Rotation
        v = vector_4th_quad.rotateXY(-math.pi / 4)

        assert v.x == pytest.approx(0.7071, 0.0001)
        assert v.y == pytest.approx(2.1213, 0.0001)
        assert v.angleXY == pytest.approx(vector_4th_quad.angleXY - (math.pi / 4))

    def test_angle_between_1st_quad_x_axis(self, vector_1st_quad: geometry.Vector):
        a = vector_1st_quad.angleToXY(geometry.Vector(1, 0, 0))
        assert a == pytest.approx(-vector_1st_quad.angleXY)

    def test_angle_between_1st_quad_y_axis(self, vector_1st_quad: geometry.Vector):
        a = vector_1st_quad.angleToXY(geometry.Vector(0, 1, 0))
        assert a == pytest.approx((math.pi / 2) - vector_1st_quad.angleXY)

    def test_angle_between_1st_quad_neg_x_axis(self, vector_1st_quad: geometry.Vector):
        a = vector_1st_quad.angleToXY(geometry.Vector(-1, 0, 0))
        assert a == pytest.approx(math.pi - vector_1st_quad.angleXY)

    def test_angle_between_1st_quad_neg_y_axis(self, vector_1st_quad: geometry.Vector):
        a = vector_1st_quad.angleToXY(geometry.Vector(0, -1, 0))
        assert a == pytest.approx(-vector_1st_quad.angleXY - (math.pi / 2))

    def test_angle_between_2nd_quad_x_axis(self, vector_2nd_quad: geometry.Vector):
        a = vector_2nd_quad.angleToXY(geometry.Vector(1, 0, 0))
        assert a == pytest.approx(-vector_2nd_quad.angleXY)

    def test_angle_between_2nd_quad_y_axis(self, vector_2nd_quad: geometry.Vector):
        a = vector_2nd_quad.angleToXY(geometry.Vector(0, 1, 0))
        assert a == pytest.approx((math.pi / 2) - vector_2nd_quad.angleXY)

    def test_angle_between_2nd_quad_neg_x_axis(self, vector_2nd_quad: geometry.Vector):
        a = vector_2nd_quad.angleToXY(geometry.Vector(-1, 0, 0))
        assert a == pytest.approx(math.pi - vector_2nd_quad.angleXY)

    def test_angle_between_2nd_quad_neg_y_axis(self, vector_2nd_quad: geometry.Vector):
        a = vector_2nd_quad.angleToXY(geometry.Vector(0, -1, 0))
        assert a == pytest.approx(-(math.pi / 2) - vector_2nd_quad.angleXY)

    def test_angle_between_3rd_quad_x_axis(self, vector_3rd_quad: geometry.Vector):
        a = vector_3rd_quad.angleToXY(geometry.Vector(1, 0, 0))
        assert a == pytest.approx(-vector_3rd_quad.angleXY)

    def test_angle_between_3rd_quad_y_axis(self, vector_3rd_quad: geometry.Vector):
        a = vector_3rd_quad.angleToXY(geometry.Vector(0, 1, 0))
        assert a == pytest.approx((math.pi / 2) - vector_3rd_quad.angleXY)

    def test_angle_between_3rd_quad_neg_x_axis(self, vector_3rd_quad: geometry.Vector):
        a = vector_3rd_quad.angleToXY(geometry.Vector(-1, 0, 0))
        assert a == pytest.approx(math.pi - vector_3rd_quad.angleXY)

    def test_angle_between_3rd_quad_neg_y_axis(self, vector_3rd_quad: geometry.Vector):
        a = vector_3rd_quad.angleToXY(geometry.Vector(0, -1, 0))
        assert a == pytest.approx(-(math.pi / 2) - vector_3rd_quad.angleXY)

    def test_angle_between_4th_quad_x_axis(self, vector_4th_quad: geometry.Vector):
        a = vector_4th_quad.angleToXY(geometry.Vector(1, 0, 0))
        assert a == pytest.approx(-vector_4th_quad.angleXY)

    def test_angle_between_4th_quad_y_axis(self, vector_4th_quad: geometry.Vector):
        a = vector_4th_quad.angleToXY(geometry.Vector(0, 1, 0))
        assert a == pytest.approx((math.pi / 2) - vector_4th_quad.angleXY)

    def test_angle_between_4th_quad_neg_x_axis(self, vector_4th_quad: geometry.Vector):
        a = vector_4th_quad.angleToXY(geometry.Vector(-1, 0, 0))
        assert a == pytest.approx(math.pi - vector_4th_quad.angleXY)

    def test_angle_between_4th_quad_neg_y_axis(self, vector_4th_quad: geometry.Vector):
        a = vector_4th_quad.angleToXY(geometry.Vector(0, -1, 0))
        assert a == pytest.approx(-(math.pi / 2) - vector_4th_quad.angleXY)


@ pytest.fixture
def vector_origin() -> geometry.Vector:
    return geometry.Vector(0, 0, 0)


@ pytest.fixture
def vector_1st_quad() -> geometry.Vector:
    return geometry.Vector(1, 2, 3)


@ pytest.fixture
def vector_2nd_quad() -> geometry.Vector:
    return geometry.Vector(1, -2, 3)


@ pytest.fixture
def vector_3rd_quad() -> geometry.Vector:
    return geometry.Vector(-1, -2, 3)


@ pytest.fixture
def vector_4th_quad() -> geometry.Vector:
    return geometry.Vector(-1, 2, 3)
