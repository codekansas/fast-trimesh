"""Tests Delaunay triangulation."""

import random

from tmesh import Point2D, triangulate_2d


def test_simple_triangulate_2d() -> None:
    """Tests Delaunay triangulation."""

    points = [
        Point2D(0.0, 0.0),
        Point2D(1.0, 0.0),
        Point2D(0.0, 1.0),
        Point2D(1.0, 1.0),
    ]
    trimesh = triangulate_2d(points)

    assert len(trimesh.vertices) == 4
    assert len(trimesh.faces) == 2
    assert sorted(trimesh.vertices) == sorted(points)


def test_large_triangulate_2d() -> None:
    """Tests Delaunay triangulation for 100 random points."""

    # Because of numerical errors this will sometimes still fail to
    # triangulate densely packed points. Keeping these frozen to prevent
    # flaky tests and disabling shuffling (although, it is usually better
    # to shuffle for runtime performance).
    random.seed(1337)
    points = [Point2D(random.random(), random.random()) for _ in range(100)]
    trimesh = triangulate_2d(points, shuffle=False)

    assert len(trimesh.vertices) == 100
    assert sorted(trimesh.vertices) == sorted(points)

    # Checks that each vertex is part of a face.
    vertices = {
        vertex
        for face in trimesh.faces
        for vertex in trimesh.get_triangle(face).vertices()
    }
    assert vertices == set(points)

    # Builds an adjacency map for vertices.
    vertex_map = {i: set() for i in range(len(points))}
    for face in trimesh.faces:
        for edge in face.get_edges(directed=False):
            vertex_map[edge.a].add(edge.b)
            vertex_map[edge.b].add(edge.a)

    # Checks the Delaunay condition for each face, to ensure that this is
    # a valid triangulation.
    for face in trimesh.faces:
        triangle = trimesh.get_triangle(face)
        for vertex in face.get_vertices():
            for neighbor in vertex_map[vertex]:
                if neighbor in face:
                    continue
                assert not triangle.contains_point(points[neighbor])
