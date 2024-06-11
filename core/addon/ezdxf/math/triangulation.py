# Copyright (c) 2022, Manfred Moitzi
# License: MIT License
from __future__ import annotations
from typing import Iterable, Iterator, Sequence, Optional
import ezdxf
from ezdxf.math import Vec2, UVec, Vec3, safe_normal_vector, OCS

if ezdxf.options.use_c_ext:
    try:
        from ezdxf.acc.mapbox_earcut import earcut
    except ImportError:
        from ._mapbox_earcut import earcut
else:
    from ._mapbox_earcut import earcut

__all__ = [
    "mapbox_earcut_2d",
    "mapbox_earcut_3d",
]


def mapbox_earcut_2d(
    exterior: Iterable[UVec], holes: Optional[Iterable[Iterable[UVec]]] = None
) -> list[Sequence[Vec2]]:
    """Mapbox triangulation algorithm with hole support for 2D polygons.

    Implements a modified ear slicing algorithm, optimized by z-order
    curve hashing and extended to handle holes, twisted polygons, degeneracies
    and self-intersections in a way that doesn't guarantee correctness of
    triangulation, but attempts to always produce acceptable results for
    practical data.

    Source: https://github.com/mapbox/earcut

    Args:
        exterior: exterior polygon as iterable of :class:`Vec2` objects
        holes: iterable of holes as iterable of :class:`Vec2` objects, a hole
            with single point represents a `Steiner point`_.

    Returns:
        yields the result as 3-tuples of :class:`Vec2` objects

    .. _Steiner point: https://en.wikipedia.org/wiki/Steiner_point_(computational_geometry)

    """
    points: list[Vec2] = Vec2.list(exterior)
    if len(points) == 0:
        return []
    holes_: list[list[Vec2]] = []
    if holes:
        holes_ = [Vec2.list(hole) for hole in holes]
    return earcut(points, holes_)


def mapbox_earcut_3d(
    exterior: Iterable[UVec], holes: Optional[Iterable[Iterable[UVec]]] = None
) -> Iterator[tuple[Vec3, Vec3, Vec3]]:
    """Mapbox triangulation algorithm with hole support for flat
    3D polygons.

    Implements a modified ear slicing algorithm, optimized by z-order
    curve hashing and extended to handle holes, twisted polygons, degeneracies
    and self-intersections in a way that doesn't guarantee correctness of
    triangulation, but attempts to always produce acceptable results for
    practical data.

    Source: https://github.com/mapbox/earcut

    Args:
        exterior: exterior polygon as iterable of :class:`Vec3` objects
        holes: iterable of holes as iterable of :class:`Vec3` objects, a hole
            with single point represents a `Steiner point`_.

    Returns:
        yields the result as 3-tuples of :class:`Vec3` objects

    Raise:
        TypeError: invalid input data type
        ZeroDivisionError: normal vector calculation failed

    """
    polygon = list(exterior)
    if len(polygon) == 0:
        return

    if not isinstance(polygon[0], Vec3):
        raise TypeError("Vec3() as input type required")
    if polygon[0].isclose(polygon[-1]):
        polygon.pop()
    count = len(polygon)
    if count < 3:
        return
    if count == 3:
        yield polygon[0], polygon[1], polygon[2]
        return

    ocs = OCS(safe_normal_vector(polygon))
    elevation = ocs.from_wcs(polygon[0]).z  # type: ignore
    exterior_ocs = list(ocs.points_from_wcs(polygon))
    holes_ocs: list[list[Vec3]] = []
    if holes:
        holes_ocs = [list(ocs.points_from_wcs(hole)) for hole in holes]

    for triangle in earcut(exterior_ocs, holes_ocs):
        yield tuple(  # type: ignore
            ocs.points_to_wcs(Vec3(v.x, v.y, elevation) for v in triangle)
        )
