import geometry


class TestPoint:

    def test_add_vector_origin(self):
        p = geometry.Point(0, 0, 0)
        p += geometry.Vector(1, 2, 3)

        assert p.x == 1
        assert p.y == 2
        assert p.z == 3

    def test_add_vector(self):
        p = geometry.Point(-1, -2, -3)
        p += geometry.Vector(1, 2, 3)

        assert p.x == 0
        assert p.y == 0
        assert p.z == 0
