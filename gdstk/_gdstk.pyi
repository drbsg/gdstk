import pathlib
import datetime
import sys
from typing import Optional, Iterable, Any, List, Dict, Tuple, Set, Union
from collections.abc import Callable, Sequence

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

import numpy
from numpy.typing import ArrayLike # type: ignore

class Cell:
    labels: List[Label]
    name: str
    paths: List[Union[FlexPath, RobustPath]]
    polygons: List[Polygon]
    properties: List[List[Union[str, bytes, float]]]
    references: List[Reference]
    def __init__(self, name: str) -> None: ...
    def add(self, *elements: Union[Polygon, FlexPath, RobustPath, Label, Reference]) -> Self: ...
    def area(self, by_spec: bool = False) -> Union[float, Dict[Tuple[int, int], float]]: ...
    def bounding_box(self) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]: ...
    def convex_hull(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def copy(
        self,
        name: str,
        translation: Union[Tuple[float, float], complex] = (0, 0),
        rotation: float = 0,
        magnification: float = 1,
        x_reflection: bool = False,
        deep_copy: bool = True,
    ) -> Cell: ...
    def delete_property(self, name: str) -> Self: ...
    def dependencies(self, recursive: bool = True) -> Sequence[Union[Cell, RawCell]]: ...
    def filter(
        self,
        spec: Iterable[Tuple[int, int]],
        remove: bool = True,
        polygons: bool = True,
        paths: bool = True,
        labels: bool = True,
    ) -> Self: ...
    def flatten(self, apply_repetitions: bool = True) -> Self: ...
    def get_labels(
        self,
        apply_repetitions: bool = True,
        depth: Optional[int] = None,
        layer: Optional[int] = None,
        texttype: Optional[int] = None,
    ) -> List[Label]: ...
    def get_paths(
        self,
        apply_repetitions: bool = True,
        depth: Optional[int] = None,
        layer: Optional[int] = None,
        datatype: Optional[int] = None,
    ) -> List[Union[RobustPath, FlexPath]]: ...
    def get_polygons(
        self,
        apply_repetitions: bool = True,
        include_paths: bool = True,
        depth: Optional[int] = None,
        layer: Optional[int] = None,
        datatype: Optional[int] = None,
    ) -> List[Polygon]: ...
    def get_property(self, name: str) -> Optional[List[List[Union[str, bytes, float]]]]: ...
    def remove(self, *elements: Union[Label, Polygon, RobustPath, FlexPath, Reference]) -> Self: ...
    def set_property(
        self, name: str, value: Union[str, bytes, float, Sequence[Union[str, bytes, float]]]
    ) -> Self: ...
    def write_svg(
        self,
        outfile: Union[str, pathlib.Path],
        scaling: float = 10,
        precision: int = 6,
        shape_style: Optional[Dict[Tuple[int, int], Dict[str, str]]] = None,
        label_style: Optional[Dict[Tuple[int, int], Dict[str, str]]] = None,
        background: str = "#222222",
        pad: Union[float, str] = "5%",
        sort_function: Optional[Callable[[Polygon, Polygon], bool]] = None,
    ) -> Self: ...

class Curve:
    tolerance: float
    def __init__(self, xy: Union[Tuple[float, float], complex], tolerance: float = 0.01) -> None: ...
    def arc(
        self,
        radius: Union[float, Tuple[float, float]],
        initial_angle: float,
        final_angle: float,
        rotation: float = 0,
    ) -> Self: ...
    def bezier(
        self, xy: Sequence[Union[Tuple[float, float], complex]], relative: bool = False
    ) -> Self: ...
    def commands(self, *args: Union[float, str]) -> Self: ...
    def cubic(
        self, xy: Sequence[Union[Tuple[float, float], complex]], relative: bool = False
    ) -> Self: ...
    def cubic_smooth(
        self, xy: Sequence[Union[Tuple[float, float], complex]], relative: bool = False
    ) -> Self: ...
    def horizontal(self, x: Union[Sequence[float], float], relative: bool = False) -> Self: ...
    def interpolation(
        self,
        points: Sequence[Tuple[float, float]],
        angles: Optional[Sequence[float]] = None,
        tension_in: Union[float, Sequence[float]] = 1,
        tension_out: Union[float, Sequence[float]] = 1,
        initial_curl: float = 1,
        final_curl: float = 1,
        cycle: bool = False,
        relative: bool = False,
    ) -> Self: ...
    def parametric(
        self,
        curve_function: Callable[[float], Union[Tuple[float, float], complex]],
        relative: bool = True,
    ) -> Self: ...
    def points(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def quadratic(
        self, xy: Sequence[Union[Tuple[float, float], complex]], relative: bool = False
    ) -> Self: ...
    def quadratic_smooth(
        self, xy: Sequence[Union[Tuple[float, float], complex]], relative: bool = False
    ) -> Self: ...
    def segment(
        self,
        xy: Union[Tuple[float, float, complex], Sequence[Union[Tuple[float, float], complex]]],
        relative: bool = False,
    ) -> Self: ...
    def turn(self, radius: float, angle: float) -> Self: ...
    def vertical(self, y: Union[float, Sequence[float]], relative: bool = False) -> Self: ...

class RaithData:
    base_cell_name: str
    dwelltime_selection: int
    pitch_parallel_to_path: float
    pitch_perpendicular_to_path: float
    pitch_scale: float
    periods: int
    grating_type: int
    dots_per_cycle: int
    def __init__(
        self,
        base_cell_name: str,
        dwelltime_selection: int,
        pitch_parallel_to_path: float,
        pitch_perpendicular_to_path: float,
        pitch_scale: float,
        periods: int,
        grating_type: int,
        dots_per_cycle: int,
    ) -> None: ...

class FlexPath:
    bend_function: Tuple[
        Optional[Callable[[float, float, float, float], List[Tuple[float, float]]]], ...
    ]
    bend_radius: Tuple[float, ...]
    datatypes: Tuple[int, ...]
    ends: Tuple[
        Union[Literal["flush", "extended", "round", "smooth", Tuple[float, float]], Callable[[float, float, float, float], List[Tuple[float, float]]]],
        ...]
    joins: Tuple[
        Union[Literal["natural", "miter", "bevel", "round", "smooth"], Callable[[float, float, float, float, float, float], List[Tuple[float, float]]]],
        ...]
    layers: Tuple[int, ...]
    num_paths: int
    properties: List[List[Union[str, bytes, float]]]
    repetition: Repetition
    scale_width: bool
    simple_path: bool
    size: int
    tolerance: float
    raith_data: RaithData
    def __init__(
        self,
        points: Union[Tuple[float, float, complex], Sequence[Union[Tuple[float, float], complex]]],
        width: Union[float, Sequence[float]],
        offset: Union[float, Sequence[float]] = 0,
        joins: Union[Literal["natural", "miter", "bevel", "round", "smooth", Callable[
            [float, float, float, float, float, float], Sequence[Union[Tuple[float, float], complex]]
        ]], Sequence[
            Union[Literal["natural", "miter", "bevel", "round", "smooth"], Callable[
                [float, float, float, float, float, float], Sequence[Union[Tuple[float, float], complex]]
            ]]
        ]] = "natural",
        ends: Union[Union[Literal["flush", "extended", "round", "smooth", Tuple[float, float]], Callable[[float, float, float, float], Sequence[Union[Tuple[float, float], complex]]]], Sequence[
            Union[Literal["flush", "extended", "round", "smooth", Tuple[float, float]], Callable[[float, float, float, float], Sequence[Union[Tuple[float, float], complex]]]]
        ]] = "flush",
        bend_radius: Union[float, Sequence[float]] = 0,
        bend_function: Union[Optional[
            Callable[[float, float, float, float], Sequence[Union[Tuple[float, float], complex]]]
        ], Sequence[
            Callable[[float, float, float, float], Sequence[Union[Tuple[float, float], complex]]]
        ]] = None,
        tolerance: float = 1e-2,
        simple_path: bool = False,
        scale_width: bool = True,
        layer: Union[int, Sequence[int]] = 0,
        datatype: Union[int, Sequence[int]] = 0,
    ) -> None: ...
    def apply_repetition(self) -> List[Self]: ...
    def arc(
        self,
        radius: Union[float, Tuple[float, float]],
        initial_angle: float,
        final_angle: float,
        rotation: float = 0,
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
    ) -> Self: ...
    def bezier(
        self,
        xy: Sequence[Union[Tuple[float, float], complex]],
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
        relative: bool = False,
    ) -> Self: ...
    def commands(self, *args: Union[str, float]) -> Self: ...
    def copy(self) -> Self: ...
    def cubic(
        self,
        xy: Sequence[Union[Tuple[float, float], complex]],
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
        relative: bool = False,
    ) -> Self: ...
    def cubic_smooth(
        self,
        xy: Sequence[Union[Tuple[float, float], complex]],
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
        relative: bool = False,
    ) -> Self: ...
    def delete_gds_property(self, attr: int) -> Self: ...
    def delete_property(self, name: str) -> Self: ...
    def get_gds_property(self, attr: int) -> Optional[str]: ...
    def get_property(self, name: str) -> Optional[List[List[Union[str, bytes, float]]]]: ...
    def horizontal(
        self,
        x: Union[float, Sequence[float]],
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
        relative: bool = False,
    ) -> Self: ...
    def interpolation(
        self,
        points: Sequence[Union[Tuple[float, float], complex]],
        angles: Optional[Sequence[float]] = None,
        tension_in: Union[float, Sequence[float]] = 1,
        tension_out: Union[float, Sequence[float]] = 1,
        initial_curl: float = 1,
        final_curl: float = 1,
        cycle: bool = False,
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
        relative: bool = False,
    ) -> Self: ...
    def mirror(
        self, p1: Union[Tuple[float, float], complex], p2: Union[Tuple[float, float], complex] = (0, 0)
    ) -> Self: ...
    def offsets(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def parametric(
        self,
        path_function: Callable[[float], Union[Tuple[float, float], complex]],
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
        relative: bool = True,
    ) -> Self: ...
    def path_spines(self) -> List[numpy.ndarray[Any, numpy.dtype[numpy.float64]]]: ...
    def quadratic(
        self,
        xy: Sequence[Union[Tuple[float, float], complex]],
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
        relative: bool = False,
    ) -> Self: ...
    def quadratic_smooth(
        self,
        xy: Sequence[Union[Tuple[float, float], complex]],
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
        relative: bool = False,
    ) -> Self: ...
    def rotate(self, angle: float, center: Union[Tuple[float, float], complex] = (0, 0)) -> Self: ...
    def scale(self, s: float, center: Union[Tuple[float, float], complex] = (0, 0)) -> Self: ...
    def segment(
        self,
        xy: Union[Sequence[Union[Tuple[float, float, complex]], Tuple[float, float]], complex],
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
        relative: bool = False,
    ) -> Self: ...
    def set_bend_function(
        self,
        functions: Optional[Callable[[float, float, float, float], Sequence[Tuple[float, float]]]],
    ) -> Self: ...
    def set_bend_radius(self, *radii: Optional[float]) -> Self: ...
    def set_datatypes(self, *datatypes: int) -> Self: ...
    def set_ends(
        self,
        *ends: Union[Literal["flush", "extended", "round", "smooth", Tuple[float, float]], Callable[[float, float, float, float], Sequence[float]]],
    ) -> Self: ...
    def set_gds_property(self, attr: int, value: str) -> Self: ...
    def set_joins(
        self,
        *joins: Union[Literal["natural", "miter", "bevel", "round", "smooth"], Callable[
            [float, float, float, float, float, float], Sequence[Union[Tuple[float, float], complex]]
        ]],
    ) -> Self: ...
    def set_layers(self, *layers: int) -> Self: ...
    def set_property(
        self, name: str, value: Union[str, bytes, float, Sequence[Union[str, bytes, float]]]
    ) -> Self: ...
    def spine(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def to_polygons(self) -> List[Polygon]: ...
    def translate(
        self, dx: Union[Union[float, Tuple[float, float]], complex], dy: Optional[float] = None
    ) -> Self: ...
    def turn(
        self,
        radius: float,
        angle: float,
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
    ) -> Self: ...
    def vertical(
        self,
        y: Union[float, Sequence[float]],
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
        relative: bool = False,
    ) -> Self: ...
    def widths(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...

class GdsWriter:
    def __init__(
        self,
        outfile: Union[str, pathlib.Path],
        name: str = "library",
        unit: float = 1e-6,
        precision: float = 1e-9,
        max_points: int = 199,
        timestamp: Optional[datetime.datetime] = None,
    ) -> None: ...
    def close(self) -> None: ...
    def write(self, *cells: Union[Cell, RawCell]) -> Self: ...

class Label:
    anchor: Literal["n", "s", "e", "w", "ne", "nw", "se", "sw", "o"]
    layer: int
    magnification: float
    origin: Tuple[float, float]
    properties: List[List[Union[str, bytes, float]]]
    repetition: Repetition
    rotation: float
    text: str
    texttype: int
    x_reflection: bool
    def __init__(
        self,
        text: str,
        origin: Union[Tuple[float, float], complex],
        anchor: Literal["n", "s", "e", "w", "ne", "nw", "se", "sw", "o"] = "o",
        rotation: float = 0,
        magnification: float = 1,
        x_reflection: bool = False,
        layer: int = 0,
        texttype: int = 0,
    ) -> None: ...
    def apply_repetition(self) -> List[Self]: ...
    def copy(self) -> Self: ...
    def delete_gds_property(self, attr: int) -> Self: ...
    def delete_property(self, name: str) -> Self: ...
    def get_gds_property(self, attr: int) -> Optional[str]: ...
    def get_property(self, name: str) -> Optional[List[List[Union[str, bytes, float]]]]: ...
    def set_gds_property(self, attr: int, value: str) -> Self: ...
    def set_property(
        self, name: str, value: Union[str, bytes, float, Sequence[Union[str, bytes, float]]]
    ) -> Self: ...

class Library:
    cells: List[Union[Cell, RawCell]]
    name: str
    precision: float
    properties: List[List[Union[str, bytes, float]]]
    unit: float
    def __init__(
        self, name: str = "library", unit: float = 1e-6, precision: float = 1e-9
    ) -> None: ...
    def add(self, *cells: Union[Cell, RawCell]) -> Self: ...
    def delete_property(self, name: str) -> Self: ...
    def get_property(self, name: str) -> Optional[List[List[Union[str, bytes, float]]]]: ...
    def layers_and_datatypes(self) -> Set[Tuple[int, int]]: ...
    def layers_and_texttypes(self) -> Set[Tuple[int, int]]: ...
    def new_cell(self, name: str) -> Cell: ...
    def remove(self, *cells: Union[Cell, RawCell]) -> Self: ...
    def rename_cell(self, old_name: str, new_name: str) -> Self: ...
    def replace(self, *cells: Union[Cell, RawCell]) -> Self: ...
    def set_property(
        self, name: str, value: Union[str, bytes, float, Sequence[Union[str, bytes, float]]]
    ) -> Self: ...
    def top_level(self) -> List[Union[Cell, RawCell]]: ...
    def write_gds(
        self,
        outfile: Union[str, pathlib.Path],
        max_points: int = 199,
        timestamp: Optional[datetime.datetime] = None,
    ) -> None: ...
    def write_oas(
        self,
        outfile: Union[str, pathlib.Path],
        compression_level: int = 6,
        detect_rectangles: bool = True,
        detect_trapezoids: bool = True,
        circletolerance: float = 0,
        standard_properties: bool = False,
        validation: Optional[Literal["crc32", "checksum32"]] = None,
    ) -> None: ...

class Polygon:
    datatype: int
    layer: int
    points: List[Tuple[float, float]]
    properties: List[List[Union[str, bytes, float]]]
    repetition: Repetition
    size: int
    def __init__(
        self, points: Sequence[Union[Tuple[float, float], complex]], layer: int = 0, datatype: int = 0
    )-> None: ...
    def apply_repetition(self) -> List[Self]: ...
    def area(self) -> float: ...
    def perimeter(self) -> float: ...
    def bounding_box(self) -> Tuple[Tuple[float, float], Tuple[float, float]]: ...
    def contain(self, *points: Union[Tuple[float, float], complex]) -> Union[bool, Tuple[bool, ...]]: ...
    def contain_all(self, *points: Union[Tuple[float, float], complex]) -> bool: ...
    def contain_any(self, *points: Union[Tuple[float, float], complex]) -> bool: ...
    def copy(self) -> Self: ...
    def delete_gds_property(self, attr: int) -> Self: ...
    def delete_property(self, name: str) -> Self: ...
    def fillet(self, radius: Union[float, Sequence[float]], tolerance: float = 0.01) -> Self: ...
    def fracture(self, max_points: int = 199, precision: float = 1e-3) -> List[Polygon]: ...
    def get_gds_property(self, attr: int) -> Optional[str]: ...
    def get_property(self, name: str) -> Optional[List[List[Union[str, bytes, float]]]]: ...
    def mirror(
        self, p1: Union[Tuple[float, float], complex], p2: Union[Tuple[float, float], complex] = (0, 0)
    ) -> Self: ...
    def rotate(self, angle: float, center: Union[Tuple[float, float], complex] = (0, 0)) -> Self: ...
    def scale(
        self, sx: float, sy: float = 0, center: Union[Tuple[float, float], complex] = (0, 0)
    ) -> Self: ...
    def set_gds_property(self, attr: int, value: str) -> Self: ...
    def set_property(
        self, name: str, value: Union[str, bytes, float, Sequence[Union[str, bytes, float]]]
    ) -> Self: ...
    def transform(
        self,
        magnification: float = 1,
        x_reflection: bool = False,
        rotation: float = 0,
        translation: Optional[Union[Tuple[float, float], complex]] = None,
        matrix: Optional[ArrayLike] = None, # type: ignore
    ) -> Self: ...
    def translate(
        self, dx: Union[Union[float, Tuple[float, float]], complex], dy: Optional[float] = None
    ) -> Self: ...

class RawCell:
    name: str
    size: int
    def __init__(self, name: str)-> None: ...
    def dependencies(self, recursive: bool = True) -> List[RawCell]: ...

class Reference:
    cell: Cell
    cell_name: str
    magnification: float
    origin: Tuple[float, float]
    properties: List[List[Union[str, bytes, float]]]
    repetition: Repetition
    rotation: float
    x_reflection: bool
    def __init__(
        self,
        cell: Cell,
        origin: Union[Tuple[float, float], complex] = (0, 0),
        rotation: float = 0,
        magnification: float = 1,
        x_reflection: bool = False,
        columns: int = 1,
        rows: int = 1,
        spacing: Optional[Sequence[float]] = ...,
    )-> None: ...
    def apply_repetition(self) -> List[Self]: ...
    def bounding_box(self) -> Tuple[Tuple[float, float], Tuple[float, float]]: ...
    def convex_hull(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def copy(self) -> Self: ...
    def delete_gds_property(self, attr: int) -> Self: ...
    def delete_property(self, name: str) -> Self: ...
    def get_gds_property(self, attr: int) -> Optional[str]: ...
    def get_labels(
        self,
        apply_repetitions: bool = True,
        depth: Optional[int] = None,
        layer: Optional[int] = None,
        texttype: Optional[int] = None,
    ) -> List[Label]: ...
    def get_paths(
        self,
        apply_repetitions: bool = True,
        depth: Optional[int] = None,
        layer: Optional[int] = None,
        datatype: Optional[int] = None,
    ) -> List[Union[RobustPath, FlexPath]]: ...
    def get_polygons(
        self,
        apply_repetitions: bool = True,
        include_paths: bool = True,
        depth: Optional[int] = None,
        layer: Optional[int] = None,
        datatype: Optional[int] = None,
    ) -> List[Polygon]: ...
    def get_property(self, name: str) -> Optional[List[List[Union[str, bytes, float]]]]: ...
    def set_gds_property(self, attr: int, value: str) -> Self: ...
    def set_property(
        self, name: str, value: Union[str, bytes, float, Sequence[Union[str, bytes, float]]]
    ) -> Self: ...

class Repetition:
    columns: Optional[int]
    offsets: Optional[numpy.ndarray[Any, numpy.dtype[numpy.float64]]]
    rows: Optional[int]
    size: int
    spacing: Optional[Tuple[float, float]]
    v1: Optional[Tuple[float, float]]
    v2: Optional[Tuple[float, float]]
    x_offsets: Optional[numpy.ndarray[Any, numpy.dtype[numpy.float64]]]
    y_offsets: Optional[numpy.ndarray[Any, numpy.dtype[numpy.float64]]]
    def __init__(
        self,
        columns: Optional[int] = None,
        rows: Optional[int] = None,
        spacing: Optional[Union[Tuple[float, float], complex]] = None,
        v1: Optional[Union[Tuple[float, float], complex]] = None,
        v2: Optional[Union[Tuple[float, float], complex]] = None,
        offsets: Optional[Sequence[Union[Tuple[float, float], complex]]] = None,
        x_offsets: Optional[Sequence[float]] = None,
        y_offsets: Optional[Sequence[float]] = None,
    )-> None: ...
    def get_offsets(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...

class RobustPath:
    datatypes: Tuple[int, ...]
    ends: Tuple[
        Union[Literal["flush", "extended", "round", "smooth", Tuple[float, float]], Callable[[float, float, float, float], Sequence[Union[complex, Tuple[float, float]]]]],
        ...]
    layers: Tuple[int, ...]
    max_evals: int
    num_paths: int
    properties: List[List[Union[str, bytes, float]]]
    repetition: Repetition
    scale_width: bool
    simple_path: bool
    size: int
    tolerance: float
    def __init__(
        self,
        initial_point: Union[Tuple[float, float], complex],
        width: Union[float, Sequence[float]],
        offset: Union[float, Sequence[float]] = 0,
        ends: Union[Union[Sequence[
            Union[Union[Literal["flush", "extended", "round", "smooth", Tuple[float, float]], Callable[[float, float, float, float], Sequence[Union[complex, Tuple[float, float]]]]]
        ], Literal["flush", "extended", "round", "smooth"]], Tuple[float, float]], Callable[[float, float, float, float], Sequence[Union[complex, Tuple[float, float]]]]] = "flush",
        tolerance: float = 1e-2,
        max_evals: int = 1000,
        simple_path: bool = False,
        scale_width: bool = True,
        layer: Union[int, List[int]] = 0,
        datatype: Union[int, List[int]] = 0,
    )->None: ...
    def apply_repetition(self) -> List[Self]: ...
    def arc(
        self,
        radius: Union[float, Tuple[float, float]],
        initial_angle: float,
        final_angle: float,
        rotation: float = 0,
        width: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        offset: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
    ) -> Self: ...
    def bezier(
        self,
        xy: Sequence[Union[Tuple[float, float], complex]],
        width: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        offset: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        relative: bool = False,
    ) -> Self: ...
    def commands(self, *args: Union[str, float]) -> Self: ...
    def copy(self) -> Self: ...
    def cubic(
        self,
        xy: Sequence[Tuple[float, float]],
        width: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        offset: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        relative: bool = False,
    ) -> Self: ...
    def cubic_smooth(
        self,
        xy: Sequence[Tuple[float, float]],
        width: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        offset: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        relative: bool = False,
    ) -> Self: ...
    def delete_gds_property(self, attr: int) -> Self: ...
    def delete_property(self, name: str) -> Self: ...
    def get_gds_property(self, attr: int) -> Optional[str]: ...
    def get_property(self, name: str) -> Optional[List[List[Union[str, bytes, float]]]]: ...
    def gradient(self, u: float, from_below: bool = True) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def horizontal(
        self,
        x: float,
        width: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        offset: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        relative: bool = False,
    ) -> Self: ...
    def interpolation(
        self,
        points: Sequence[Union[Tuple[float, float], complex]],
        angles: Optional[Sequence[float]] = None,
        tension_in: Union[float, Sequence[float]] = 1,
        tension_out: Union[float, Sequence[float]] = 1,
        initial_curl: float = 1,
        final_curl: float = 1,
        cycle: bool = False,
        width: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        offset: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        relative: bool = True,
    ) -> Self: ...
    def mirror(
        self, p1: Union[Tuple[float, float], complex], p2: Union[Tuple[float, float], complex] = (0, 0)
    ) -> Self: ...
    def offsets(self, u: float, from_below: bool = True) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def parametric(
        self,
        path_function: Callable[[float], Union[Tuple[float, float], complex]],
        path_gradient: Optional[Callable[[float], Union[Tuple[float, float], complex]]] = None,
        width: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        offset: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        relative: bool = True,
    ) -> Self: ...
    def path_spines(self) -> List[numpy.ndarray[Any, numpy.dtype[numpy.float64]]]: ...
    def position(self, u: float, from_below: bool = True) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def quadratic(
        self,
        xy: Sequence[Union[Tuple[float, float], complex]],
        width: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        offset: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        relative: bool = False,
    ) -> Self: ...
    def quadratic_smooth(
        self,
        xy: Union[Tuple[float, float], complex],
        width: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        offset: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        relative: bool = False,
    ) -> Self: ...
    def rotate(self, angle: float, center: Union[Tuple[float, float], complex] = (0, 0)) -> Self: ...
    def scale(self, s: float, center: Union[Tuple[float, float], complex] = (0, 0)) -> Self: ...
    def segment(
        self,
        xy: Union[Tuple[float, float], complex],
        width: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        offset: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        relative: bool = False,
    ) -> Self: ...
    def set_datatypes(self, *datatypes: int) -> Self: ...
    def set_ends(
        self,
        *ends: Union[Literal["flush", "extended", "round", "smooth", Tuple[float, float]], Callable[[float, float, float, float], float]],
    ) -> Self: ...
    def set_gds_property(self, attr: int, value: str) -> Self: ...
    def set_layers(self, *layers: int) -> Self: ...
    def set_property(
        self, name: str, value: Union[str, bytes, float, Sequence[Union[str, bytes, float]]]
    ) -> Self: ...
    def spine(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def to_polygons(self) -> List[Polygon]: ...
    def translate(
        self, dx: Union[Union[float, Tuple[float, float]], complex], dy: Optional[float] = None
    ) -> Self: ...
    def turn(
        self,
        radius: float,
        angle: float,
        width: Union[Optional[float], Sequence[float]] = None,
        offset: Union[Optional[float], Sequence[float]] = None,
    ) -> Self: ...
    def vertical(
        self,
        y: float,
        width: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        offset: Union[Optional[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]], Sequence[
            Union[float, Tuple[float, Literal["constant", "linear", "smooth"]], Callable[[float], float]]
        ]] = None,
        relative: bool = False,
    ) -> Self: ...
    def widths(self, u: float, from_below: bool = True) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...

def all_inside(
    points: Sequence[Union[Tuple[float, float], complex]],
    polygons: Union[Polygon, FlexPath, RobustPath, Reference, Sequence[Union[Polygon, FlexPath, RobustPath, Reference]]],
) -> bool: ...
def any_inside(
    points: Sequence[Union[Tuple[float, float], complex]],
    polygons: Union[Polygon, FlexPath, RobustPath, Reference, Sequence[Union[Polygon, FlexPath, RobustPath, Reference]]],
) -> bool: ...
def boolean(
    operand1: Union[Polygon, FlexPath, RobustPath, Reference, Sequence[Union[Polygon, FlexPath, RobustPath, Reference]]],
    operand2: Union[Polygon, FlexPath, RobustPath, Reference, Sequence[Union[Polygon, FlexPath, RobustPath, Reference]]],
    operation: Literal["or", "and", "xor", "not"],
    precision: float = 1e-3,
    layer: int = 0,
    datatype: int = 0,
) -> List[Polygon]: ...
def contour(
    data: ArrayLike, # type: ignore
    level: int = 0,
    length_scale: float = 1,
    precision: float = 0.01,
    layer: int = 0,
    datatype: int = 0,
) -> List[Polygon]: ...
def cross(
    center: Union[Tuple[float, float], complex],
    full_size: float,
    arm_width: float,
    layer: int = 0,
    datatype: int = 0,
) -> Polygon: ...
def ellipse(
    center: Union[Tuple[float, float], complex],
    radius: Union[float, Tuple[float, float]],
    inner_radius: Union[Optional[float], Tuple[float, float]] = None,
    initial_angle: float = 0,
    final_angle: float = 0,
    tolerance: float = 0.01,
    layer: int = 0,
    datatype: int = 0,
) -> Polygon: ...
def gds_info(infile: Union[str, pathlib.Path]) -> Dict[str, Any]: ...

# def gds_timestamp(filename: Union[str, pathlib.Path], timestamp:Optional[datetime.datetime]=None) -> datetime.datetime: ...
def gds_units(infile: Union[str, pathlib.Path]) -> Tuple[float, float]: ...
def inside(
    points: Sequence[Union[Tuple[float, float], complex]],
    polygons: Union[Polygon, FlexPath, RobustPath, Reference, Sequence[Union[Polygon, FlexPath, RobustPath, Reference]]],
) -> Tuple[bool, ...]: ...
def oas_precision(infile: Union[str, pathlib.Path]) -> float: ...
def oas_validate(infile: Union[str, pathlib.Path]) -> Tuple[bool, int]: ...
def offset(
    polygons: Union[Polygon, FlexPath, RobustPath, Reference, Sequence[Union[Polygon, FlexPath, RobustPath, Reference]]],
    distance: float,
    join: Literal["miter", "bevel", "round"] = "miter",
    tolerance: int = 2,
    precision: float = 1e-3,
    use_union: bool = False,
    layer: int = 0,
    datatype: int = 0,
) -> List[Polygon]: ...
def racetrack(
    center: Union[Tuple[float, float], complex],
    straight_length: float,
    radius: float,
    inner_radius: float = 0,
    vertical: bool = False,
    tolerance: float = 0.01,
    layer: int = 0,
    datatype: int = 0,
) -> Polygon: ...
def read_gds(
    infile: Union[str, pathlib.Path],
    unit: float = 0,
    tolerance: float = 0,
    filter: Optional[Iterable[Tuple[int, int]]] = None,
) -> Library: ...
def read_oas(infile: Union[str, pathlib.Path], unit: float = 0, tolerance: float = 0) -> Library: ...
def read_rawcells(infile: Union[str, pathlib.Path]) -> Dict[str, RawCell]: ...
def rectangle(
    corner1: Union[Tuple[float, float], complex],
    corner2: Union[Tuple[float, float], complex],
    layer: int = 0,
    datatype: int = 0,
) -> Polygon: ...
def regular_polygon(
    center: Union[Tuple[float, float], complex],
    side_length: float,
    sides: int,
    rotation: float = 0,
    layer: int = 0,
    datatype: int = 0,
) -> Polygon: ...
def slice(
    polygons: Union[Polygon, FlexPath, RobustPath, Reference, Sequence[Union[Polygon, FlexPath, RobustPath, Reference]]],
    position: Union[float, Sequence[float]],
    axis: Literal["x", "y"],
    precision: float = 1e-3,
) -> List[List[Polygon]]: ...
def text(
    text: str,
    size: float,
    position: Union[Tuple[float, float], complex],
    vertical: bool = False,
    layer: int = 0,
    datatype: int = 0,
) -> List[Polygon]: ...
