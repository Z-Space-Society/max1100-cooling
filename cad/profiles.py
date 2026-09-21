"""Extruded-profile parts, written to both Rhino (.3dm) and STL. All in mm.

A part is a list of Slabs: a flat outline (with optional polygon or round
holes) extruded between two z heights. That is how the card adapter is modelled in
Rhino, so each Slab becomes one native, editable Rhino Extrusion on its own
layer, and the STL is the union of the same Slabs, so it's a single
watertight body.

Frame: the CAD frame (README.md). Rhino's Top view is the
tail view.
"""
from dataclasses import dataclass, field
from math import cos, pi, sin
from pathlib import Path

import numpy as np
import rhino3dm as r
import trimesh
from manifold3d import CrossSection, FillRule, Manifold

REPO = Path(__file__).resolve().parent.parent
STL_DIR = REPO / "stl"
RHINO_DIR = REPO / "rhino"
CIRCLE_SEGMENTS = 64  # STL only; the .3dm gets true circles
FUSE_EPS = 0.001      # STL only; see to_mesh


@dataclass
class Hole:
    x: float
    y: float
    d: float


@dataclass
class Slab:
    layer: str
    outline: list                                # [(x, y), ...], not closed
    z0: float
    z1: float
    cutouts: list = field(default_factory=list)  # polygons, like outline
    holes: list = field(default_factory=list)    # Hole
    # "z": outline is (x, y), extruded z0 → z1 (the usual case).
    # "x": outline is (y, z), extruded x0 → x1 (passed as z0, z1). For walls
    # that slope in Y as they go in Z. No cutouts or holes.
    axis: str = "z"


@dataclass
class Curve:
    """Reference outline: goes in the .3dm only, never the STL."""
    layer: str
    outline: list
    z: float = 0.0


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def offset(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


# ---- Rhino ---------------------------------------------------------------

LAYER_COLORS = [(0, 0, 0), (200, 0, 0), (125, 38, 205), (0, 0, 255), (0, 127, 0)]


def _polyline(pts, z):
    return r.PolylineCurve([r.Point3d(x, y, z) for x, y in list(pts) + [pts[0]]])


def _circle(h, z):
    return r.Circle(r.Point3d(h.x, h.y, z), h.d / 2).ToNurbsCurve()


def _x_extrusion(s):
    assert not s.cutouts and not s.holes, "axis='x' slabs take no cutouts or holes"
    pts = list(s.outline)
    for attempt in range(2):
        curve = r.PolylineCurve([r.Point3d(s.z0, y, z) for y, z in pts + [pts[0]]])
        e = r.Extrusion.Create(curve, s.z1 - s.z0, True)
        b = e.GetBoundingBox()
        if abs(b.Min.X - s.z0) < 1e-6 and abs(b.Max.X - s.z1) < 1e-6:
            break
        pts = pts[::-1]  # wrong way round: the curve's normal sets the direction
    else:
        raise ValueError(f"could not extrude {s.layer} along +X")
    assert e.IsValid and e.IsSolid, f"bad extrusion on {s.layer}"
    return e


def write_3dm(items, name, source=""):
    f = r.File3dm()
    f.Settings.ModelUnitSystem = r.UnitSystem.Millimeters
    f.Settings.ModelAbsoluteTolerance = 0.001
    layers = {}
    for it in items:
        if it.layer not in layers:
            lay = r.Layer()
            lay.Name = it.layer
            lay.Color = (*LAYER_COLORS[len(layers) % len(LAYER_COLORS)], 255)
            layers[it.layer] = f.Layers.Add(lay)
        attrs = r.ObjectAttributes()
        attrs.LayerIndex = layers[it.layer]
        if source:  # shows in Rhino under Properties > Attribute User Text
            attrs.SetUserString("source", source)
        if isinstance(it, Curve):
            f.Objects.AddCurve(_polyline(it.outline, it.z), attrs)
            continue
        if it.axis == "x":
            f.Objects.AddExtrusion(_x_extrusion(it), attrs)
            continue
        e = r.Extrusion.Create(_polyline(it.outline, it.z0), it.z1 - it.z0, True)
        # Inner profiles go in the extrusion's local 2D frame, whose origin is
        # the outline's first point, not in world coordinates.
        ox, oy = it.outline[0]
        for c in it.cutouts:
            assert e.AddInnerProfile(_polyline(offset(c, -ox, -oy), 0))
        for h in it.holes:
            assert e.AddInnerProfile(_circle(Hole(h.x - ox, h.y - oy, h.d), 0))
        assert e.IsValid and e.IsSolid, f"bad extrusion on {it.layer}"
        f.Objects.AddExtrusion(e, attrs)
    out = RHINO_DIR / f"{name}.3dm"
    f.Write(str(out), 8)
    return out


# ---- STL -----------------------------------------------------------------

def _ccw(pts):
    a = np.asarray(pts, float)
    area = np.sum(a[:, 0] * np.roll(a[:, 1], -1) - np.roll(a[:, 0], -1) * a[:, 1])
    return a if area > 0 else a[::-1]


def _circle_pts(h):
    return [(h.x + h.d / 2 * cos(2 * pi * i / CIRCLE_SEGMENTS),
             h.y + h.d / 2 * sin(2 * pi * i / CIRCLE_SEGMENTS))
            for i in range(CIRCLE_SEGMENTS)]


def to_mesh(items):
    solid = Manifold()
    for s in items:
        if isinstance(s, Curve):
            continue
        loops = [_ccw(s.outline)] + [_ccw(c)[::-1] for c in s.cutouts] \
            + [_ccw(_circle_pts(h))[::-1] for h in s.holes]
        cs = CrossSection(loops, FillRule.EvenOdd)
        z0, z1 = s.z0, s.z1
        if s.axis == "x":
            # An X slab's end faces usually lie in the same plane as another
            # part's faces, and exactly coplanar faces break the union (STL not
            # watertight). Pull the ends in 1 µm; the .3dm stays exact.
            z0, z1 = z0 + FUSE_EPS, z1 - FUSE_EPS
        body = cs.extrude(z1 - z0).translate([0, 0, z0])
        if s.axis == "x":  # local (u, v, w) → world (x, y, z) = (w, u, v)
            body = body.transform([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]])
        solid += body
    m = solid.to_mesh()
    return trimesh.Trimesh(vertices=m.vert_properties[:, :3], faces=m.tri_verts)


def export(items, name, source=""):
    """Write rhino/<name>.3dm and stl/<name>.stl and print a sanity line."""
    p3 = write_3dm(items, name, source)
    mesh = to_mesh(items)
    STL_DIR.mkdir(exist_ok=True)
    ps = STL_DIR / f"{name}.stl"
    mesh.export(ps)
    print(f"{p3.relative_to(REPO)}, {ps.relative_to(REPO)}  "
          f"watertight: {mesh.is_watertight}  volume: {mesh.volume:.1f}  "
          f"extents: {mesh.extents.round(2)}  bounds: {mesh.bounds.round(2).tolist()}")
    return mesh
