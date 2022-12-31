"""Test CPU geometry functions."""

import math

import pytest

from fast_trimesh.fast_trimesh.cpu import geometry

Point2D = tuple[float, float]
Point3D = tuple[float, float, float]
Point = tuple[float, ...]
Line2D = tuple[Point2D, Point2D]
Line3D = tuple[Point3D, Point3D]
Line = tuple[Point, Point]
Triangle2D = tuple[Point2D, Point2D, Point2D]
Triangle3D = tuple[Point3D, Point3D, Point3D]
Triangle = tuple[Point, Point, Point]

SQRT_2 = math.sqrt(2)
SQRT_3 = math.sqrt(3)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        ((1, 0), (0, math.pi / 2), (0, 1)),
        ((1, 0), (0, math.pi), (-1, 0)),
        ((1, 0), (0, 3 * math.pi / 2), (0, -1)),
        ((1, 0), (0, 2 * math.pi), (1, 0)),
    ],
)
def test_rotate_2d(lhs: Point2D, rhs: Point2D, expected: Point2D) -> None:
    """Test rotation of a point in 2D.

    Args:
        lhs: The point.
        rhs: The angle.
        expected: The expected point.
    """

    result = geometry.rotate(lhs, rhs)
    assert result[0] == pytest.approx(expected[0], abs=1e-5)
    assert result[1] == pytest.approx(expected[1], abs=1e-5)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        ((0, 0), (1, 0), 1),
        ((0, 0), (0, 1), 1),
        ((0, 0), (1, 1), SQRT_2),
        ((0, 0, 0), (1, 0, 0), 1),
        ((0, 0, 0), (0, 1, 0), 1),
        ((0, 0, 0), (0, 0, 1), 1),
        ((0, 0, 0), (1, 1, 1), SQRT_3),
    ],
)
def test_distance(lhs: Point, rhs: Point, expected: float) -> None:
    """Test distance between two points.

    Args:
        lhs: The first point.
        rhs: The second point.
        expected: The expected distance.
    """

    assert geometry.distance(lhs, rhs) == pytest.approx(expected)  # type: ignore


@pytest.mark.parametrize(
    "lhs,expected",
    [
        (((0, 0), (1, 0), (0, 1)), 0.5),
        (((0, 0), (0, 1), (1, 0)), 0.5),
        (((0, 0), (1, 0), (1, 1)), 0.5),
        (((0, 0), (1, 1), (0, 1)), 0.5),
    ],
)
def test_area_triangle_2d(lhs: Triangle2D, expected: float) -> None:
    """Test area of a triangle in 2D.

    Args:
        lhs: The triangle.
        expected: The expected area.
    """

    assert geometry.area(lhs) == pytest.approx(expected)


@pytest.mark.parametrize(
    "lhs,expected",
    [
        (((0, 0, 0), (1, 0, 0), (0, 1, 0)), 0.5),
        (((0, 0, 0), (0, 0, 1), (1, 1, 0)), SQRT_2 / 2),
    ],
)
def test_area_triangle_3d(lhs: Triangle3D, expected: float) -> None:
    """Test area of a triangle in 2D.

    Args:
        lhs: The triangle.
        expected: The expected area.
    """

    assert geometry.area(lhs) == pytest.approx(expected)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        ((0, 0), ((0, 0), (1, 0)), (0, 0)),
        ((0, 0), ((0, 0), (0, 1)), (0, 0)),
        ((0, 0), ((1, 0), (2, 0)), None),
        ((0, 0), ((1, 0), (0, 1)), (0.5, 0.5)),
    ],
)
def test_project_point_to_line_2d(lhs: Point2D, rhs: Line2D, expected: Point2D | None) -> None:
    """Test projection of a point onto a line in 2D.

    Args:
        lhs: The point.
        rhs: The line.
        expected: The expected projection.
    """

    result = geometry.project(lhs, rhs)
    if result is None:
        assert expected is None
    else:
        assert expected is not None
        assert result[0] == pytest.approx(expected[0])
        assert result[1] == pytest.approx(expected[1])


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        ((0, 0, 0), ((0, 0, 0), (1, 0, 0)), (0, 0, 0)),
        ((0, 0, 0), ((0, 0, 0), (0, 1, 0)), (0, 0, 0)),
        ((0, 0, 0), ((0, 0, 0), (0, 0, 1)), (0, 0, 0)),
        ((0, 0, 0), ((1, 0, 0), (2, 0, 0)), None),
        ((0, 0, 0), ((1, 0, 0), (0, 1, 0)), (0.5, 0.5, 0)),
    ],
)
def test_project_point_to_line_3d(lhs: Point3D, rhs: Line3D, expected: Point3D | None) -> None:
    """Test projection of a point onto a line in 3D.

    Args:
        lhs: The point.
        rhs: The line.
        expected: The expected projection.
    """

    result = geometry.project(lhs, rhs)
    if result is None:
        assert expected is None
    else:
        assert expected is not None
        assert result[0] == pytest.approx(expected[0])
        assert result[1] == pytest.approx(expected[1])
        assert result[2] == pytest.approx(expected[2])


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        ((0, 0, 0), ((0, 0, 1), (0, 1, 1), (1, 0, 1)), (0, 0, 1)),
        ((0, 0, 0), ((0, -1, 1), (1, 1, 1), (-1, 0, 1)), (0, 0, 1)),
    ],
)
def test_project_point_to_triangle_3d(lhs: Point3D, rhs: Triangle3D, expected: Point3D | None) -> None:
    """Test projection of a point onto a triangle in 3D.

    Args:
        lhs: The point.
        rhs: The triangle.
        expected: The expected projection.
    """

    result = geometry.project(lhs, rhs)
    if result is None:
        assert expected is None
    else:
        assert expected is not None
        assert geometry.distance(result, expected) == pytest.approx(0)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        (((0, 0), (1, 0)), ((0, 1), (0, 2)), None),  # Intersect, but not in segment
        (((0, 0), (1, 1)), ((1, 1), (2, 2)), None),  # Parallel
        (((0, 0), (1, 1)), ((-1, -1), (2, 2)), None),  # Parallel, overlapping
        (((0, 0), (1, 1)), ((0, 1), (1, 0)), (0.5, 0.5)),  # Intersect
        (((0, 0), (-1, -1)), ((0, 1), (1, 0)), None),  # Intersect, but not in segment
    ],
)
def test_line_line_intersection_2d(lhs: Line2D, rhs: Line2D, expected: Point2D | None) -> None:
    """Test intersection of two lines in 2D.

    Args:
        lhs: The first line.
        rhs: The second line.
        expected: The expected intersection.
    """

    result = geometry.intersection(lhs, rhs)
    if result is None:
        assert expected is None
    else:
        assert expected is not None
        assert geometry.distance(result, expected) == pytest.approx(0)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        (((0, 0, 0), (0, 1, 1)), ((0, 0, 1), (0, 1, 0)), ((0, 0.5, 0.5), (0, 0.5, 0.5))),  # Intersect
        (((0, 0, 0), (1, 1, 1)), ((0, 0, 1), (1, 1, 0)), ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))),  # Intersect
        (((0, 0, 0), (1, 1, 1)), ((0, 0, 1), (1, 1, 2)), None),  # Parallel
    ],
)
def test_line_line_nearest_points_3d(lhs: Line3D, rhs: Line3D, expected: tuple[Point3D, Point3D] | None) -> None:
    """Test intersection of two lines in 3D.

    Args:
        lhs: The first line.
        rhs: The second line.
        expected: The expected intersection.
    """

    result = geometry.nearest_points(lhs, rhs)
    if result is None:
        assert expected is None, result
    else:
        assert expected is not None, result
        assert geometry.distance(result[0], expected[0]) == pytest.approx(0)
        assert geometry.distance(result[1], expected[1]) == pytest.approx(0)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        (((0, 0, -1), (0, 0, 1)), ((-1, -1, 0), (1, 1, 0), (1, -1, 0)), (0, 0, 0)),
        (((0, 0, -1), (0, 0, 1)), ((-1, -1, 0), (-1, 0, 0), (0, -1, 0)), None),
        (((0, 0, 0), (1, 1, 1)), ((0, 0, 1), (0, 1, 1), (1, 0, 0)), (0.5, 0.5, 0.5)),
    ],
)
def test_line_triangle_intersection_3d(lhs: Line3D, rhs: Triangle3D, expected: Point3D | None) -> None:
    """Test intersection of a line and a triangle in 3D.

    Args:
        lhs: The line.
        rhs: The triangle.
        expected: The expected intersection.
    """

    result = geometry.intersection(lhs, rhs)
    does_intersect = geometry.intersects(lhs, rhs)
    assert does_intersect == (result is not None)

    if result is None:
        assert expected is None
    else:
        assert expected is not None, result
        assert geometry.distance(result, expected) == pytest.approx(0)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        ((0, 0), ((0, 0), (1, 0)), 0),
        ((0, 0), ((0, 0), (0, 1)), 0),
        ((0, 0), ((1, 0), (2, 0)), 1),
        ((0, 0), ((0, 1), (1, 1)), 1),
    ],
)
def test_point_to_line_2d_min_distance(lhs: Point2D, rhs: Line2D, expected: float) -> None:
    """Test distance between a point and a line in 2D.

    Args:
        lhs: The point.
        rhs: The line.
        expected: The expected distance.
    """

    assert geometry.min_distance(lhs, rhs) == pytest.approx(expected)
    assert geometry.min_distance(lhs, (rhs[1], rhs[0])) == pytest.approx(expected)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        (((0, 0), (1, 0)), ((0, 0), (1, 0)), 0),
        (((0, 0), (1, 0)), ((0, 0), (0, 1)), 0),
        (((0, 0), (1, 0)), ((1, 0), (2, 0)), 0),
        (((0, 0), (1, 0)), ((0, 1), (1, 1)), 1),
        (((0, 0), (1, 0)), ((0, 1), (0, 2)), 1),
        (((0, 0), (1, 0)), ((0, 2), (0, 3)), 2),
        (((0, 0), (0, 1)), ((1, 2), (1, 3)), SQRT_2),
    ],
)
def test_line_to_line_2d_min_distance(lhs: Line2D, rhs: Line2D, expected: float) -> None:
    """Tests minimum distances between two lines in 2D.

    Args:
        lhs: The first line.
        rhs: The second line.
        expected: The expected minimum distance.
    """

    assert geometry.min_distance(lhs, rhs) == pytest.approx(expected)
    assert geometry.min_distance(lhs, (rhs[1], rhs[0])) == pytest.approx(expected)
    assert geometry.min_distance((lhs[1], lhs[0]), rhs) == pytest.approx(expected)
    assert geometry.min_distance((lhs[1], lhs[0]), (rhs[1], rhs[0])) == pytest.approx(expected)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        ((0, 0), ((0, 0), (1, 0), (0, 1)), 0),
        ((0, 0), ((0, 0), (0, 1), (1, 0)), 0),
        ((0, 0), ((0, 1), (1, 1), (0, 2)), 1),
        ((0, 0), ((1, 1), (1, 2), (2, 2)), SQRT_2),
        ((0, 0), ((2, 1), (-1, -1), (-1, 1)), 0),
        ((0, 0), ((1, 0), (2, 0), (1, 1)), 1),
        ((0, 0), ((0, 2), (0, 3), (1, 2)), 2),
    ],
)
def test_point_to_triangle_2d_min_distance(lhs: Point2D, rhs: Triangle2D, expected: float) -> None:
    """Tests minimum distances between a point and a triangle in 2D.

    Args:
        lhs: The point.
        rhs: The triangle.
        expected: The expected minimum distance.
    """

    assert geometry.min_distance(lhs, rhs) == pytest.approx(expected)
    assert geometry.min_distance(lhs, (rhs[1], rhs[2], rhs[0])) == pytest.approx(expected)
    assert geometry.min_distance(lhs, (rhs[2], rhs[1], rhs[0])) == pytest.approx(expected)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        (((0, 0), (1, 0)), ((0, 0), (1, 0), (0, 1)), 0),
        (((0, 0), (1, 0)), ((0, 0), (0, 1), (1, 0)), 0),
        (((0, 0), (1, 0)), ((0, 1), (1, 1), (0, 2)), 1),
        (((0, 0), (1, 0)), ((1, 1), (1, 2), (2, 2)), 1),
        (((0, 0), (1, 0)), ((2, 1), (-1, -1), (-1, 1)), 0),
    ],
)
def test_line_to_triangle_2d_min_distance(lhs: Line2D, rhs: Triangle2D, expected: float) -> None:
    """Tests minimum distances between a line and a triangle in 2D.

    Args:
        lhs: The line.
        rhs: The triangle.
        expected: The expected minimum distance.
    """

    assert geometry.min_distance(lhs, rhs) == pytest.approx(expected)
    assert geometry.min_distance(lhs, (rhs[1], rhs[2], rhs[0])) == pytest.approx(expected)
    assert geometry.min_distance(lhs, (rhs[2], rhs[1], rhs[0])) == pytest.approx(expected)
    assert geometry.min_distance((lhs[1], lhs[0]), rhs) == pytest.approx(expected)
    assert geometry.min_distance((lhs[1], lhs[0]), (rhs[1], rhs[2], rhs[0])) == pytest.approx(expected)
    assert geometry.min_distance((lhs[1], lhs[0]), (rhs[2], rhs[1], rhs[0])) == pytest.approx(expected)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        ((0, 0, 0), ((0, 0, 0), (1, 0, 0)), 0),
        ((0, 0, 0), ((0, 0, 0), (0, 1, 0)), 0),
        ((0, 0, 0), ((0, 0, 0), (0, 0, 1)), 0),
        ((0, 0, 0), ((1, 0, 0), (2, 0, 0)), 1),
        ((0, 0, 0), ((0, 1, 0), (1, 1, 0)), 1),
        ((0, 0, 0), ((0, 0, -1), (0, 0, 1)), 0),
    ],
)
def test_point_to_line_3d_min_distance(lhs: Point3D, rhs: Line3D, expected: float) -> None:
    """Test distance between a point and a line.

    Args:
        lhs: The point.
        rhs: The line.
        expected: The expected minimum distance.
    """

    assert geometry.min_distance(lhs, rhs) == pytest.approx(expected)
    assert geometry.min_distance(lhs, (rhs[1], rhs[0])) == pytest.approx(expected)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        (((0, 0, 0), (1, 0, 0)), ((0, 0, 0), (1, 0, 0)), 0),
        (((0, 0, 0), (1, 0, 0)), ((0, 0, 0), (0, 1, 0)), 0),
        (((0, 0, 0), (1, 0, 0)), ((0, 0, 0), (0, 0, 1)), 0),
        (((0, 0, 0), (1, 0, 0)), ((1, 0, 1), (2, 0, 1)), 1),
        (((0, 0, 0), (1, 0, 0)), ((0, 1, 0), (1, 1, 0)), 1),
        (((0, 0, -1), (0, 0, 1)), ((-1, 1, 0), (1, 1, 0)), 1),
    ],
)
def test_line_to_line_3d_min_distance(lhs: Line3D, rhs: Line3D, expected: float) -> None:
    """Test distance between a line and a line.

    Args:
        lhs: The line.
        rhs: The line.
        expected: The expected minimum distance.
    """

    assert geometry.min_distance(lhs, rhs) == pytest.approx(expected)
    assert geometry.min_distance(lhs, (rhs[1], rhs[0])) == pytest.approx(expected)
    assert geometry.min_distance((lhs[1], lhs[0]), rhs) == pytest.approx(expected)
    assert geometry.min_distance((lhs[1], lhs[0]), (rhs[1], rhs[0])) == pytest.approx(expected)


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        ((0, 0, 0), ((0, 0, 0), (1, 0, 0), (0, 1, 0)), 0),
        ((0, 0, 0), ((0, 0, 1), (1, 0, 1), (0, 1, 1)), 1),
        ((0, 2, 0), ((0, 0, -1), (1, 0, -1), (0, 0, 1)), 2),
        ((0, 0, 0), ((0, -1, 1), (1, 1, 1), (-1, 0, 1)), 1),
    ],
)
def test_point_to_triangle_3d_min_distance(lhs: Point3D, rhs: Triangle3D, expected: float) -> None:
    """Tests minimum distances between a point and a triangle in 3D.

    Args:
        lhs: The point.
        rhs: The triangle.
        expected: The expected minimum distance.
    """

    assert geometry.min_distance(lhs, rhs) == pytest.approx(expected)
    assert geometry.min_distance(lhs, (rhs[1], rhs[2], rhs[0])) == pytest.approx(expected)
    assert geometry.min_distance(lhs, (rhs[2], rhs[1], rhs[0])) == pytest.approx(expected)
