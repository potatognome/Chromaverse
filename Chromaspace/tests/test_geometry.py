from Chromaspace.geometry import Point2D, rotate_point


def test_rotate_point_90_degrees_about_origin():
    point = Point2D(1.0, 0.0)
    rotated = rotate_point(point, 90)
    assert rotated.as_tuple(6) == (0.0, 1.0)


def test_rotate_point_about_custom_origin():
    point = Point2D(2.0, 1.0)
    origin = Point2D(1.0, 1.0)
    rotated = rotate_point(point, 180, origin=origin)
    assert rotated.as_tuple(6) == (0.0, 1.0)
