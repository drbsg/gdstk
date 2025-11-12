# Python 3.8 Compatibility Report for gdstk

## Executive Summary

This report identifies all language features and library dependencies that prevent the gdstk Python library from being built for Python 3.8. The analysis reveals **three major categories** of incompatibilities that would need to be addressed to support Python 3.8.

## 1. Type Annotation Syntax (PEP 585 & PEP 604)

### 1.1 PEP 585: Type Hinting Generics In Standard Collections (Python 3.9+)

**Issue**: The type stub file `gdstk/_gdstk.pyi` uses Python 3.9+ syntax for generic types from standard collections instead of importing from the `typing` module.

**Incompatible Syntax**:
- `list[Type]` instead of `typing.List[Type]`
- `dict[Key, Value]` instead of `typing.Dict[Key, Value]`
- `tuple[Type, ...]` instead of `typing.Tuple[Type, ...]`
- `set[Type]` instead of `typing.Set[Type]`

**Occurrences in `gdstk/_gdstk.pyi`**:
- `list[...]`: **48 occurrences**
- `dict[...]`: **5 occurrences**
- `tuple[...]`: **161 occurrences**

**Examples from the code**:
```python
# Line 21-26 in gdstk/_gdstk.pyi
class Cell:
    labels: list[Label]
    name: str
    paths: list[FlexPath | RobustPath]
    polygons: list[Polygon]
    properties: list[list[str | bytes | float]]
    references: list[Reference]
```

**Fix Required**: Replace all builtin generic type syntax with `typing` module equivalents:
```python
# Python 3.8 compatible
from typing import List, Dict, Tuple, Set

class Cell:
    labels: List[Label]
    paths: List[Union[FlexPath, RobustPath]]
    polygons: List[Polygon]
    properties: List[List[Union[str, bytes, float]]]
```

### 1.2 PEP 604: Union Operator (Python 3.10+)

**Issue**: The type stub file extensively uses the `|` operator for type unions, which was introduced in Python 3.10.

**Incompatible Syntax**:
- `Type1 | Type2` instead of `typing.Union[Type1, Type2]`

**Occurrences**: **306 uses of the `|` union operator** in `gdstk/_gdstk.pyi`

**Examples from the code**:
```python
# Line 28 in gdstk/_gdstk.pyi
def add(self, *elements: Polygon | FlexPath | RobustPath | Label | Reference) -> Self: ...

# Line 29
def area(self, by_spec: bool = False) -> float | dict[tuple[int, int], float]: ...

# Line 39
translation: tuple[float, float] | complex = (0, 0),

# Line 84
shape_style: Optional[dict[tuple[int, int], dict[str, str]]] = None,
```

**Fix Required**: Replace all `|` union operators with `typing.Union`:
```python
# Python 3.8 compatible
from typing import Union

def add(self, *elements: Union[Polygon, FlexPath, RobustPath, Label, Reference]) -> Self: ...
def area(self, by_spec: bool = False) -> Union[float, Dict[Tuple[int, int], float]]: ...
translation: Union[Tuple[float, float], complex] = (0, 0)
```

### 1.3 typing_extensions.Self (Python 3.11+)

**Issue**: The code already handles this correctly with a version check, but it's worth noting.

**Current handling** (lines 12-15 in `gdstk/_gdstk.pyi`):
```python
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
```

**Status**: ✅ **Already compatible** - The code correctly uses `typing_extensions.Self` for Python versions < 3.11.

### 1.4 typing_extensions.Literal (Python 3.8+)

**Current handling** (lines 7-10 in `gdstk/_gdstk.pyi`):
```python
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
```

**Status**: ✅ **Already compatible** - `Literal` is available in Python 3.8's standard `typing` module.

## 2. NumPy Version Dependency

### 2.1 NumPy 2.0 Requirement

**Issue**: The build system requires NumPy >= 2.0, which does **not support Python 3.8**.

**Location**: `pyproject.toml` lines 2-5:
```toml
[build-system]
requires = [
    "scikit_build_core",
    "numpy >= 2.0"
]
```

**NumPy 2.0 Compatibility**:
- NumPy 2.0.0 was released in June 2024
- **Minimum Python version**: Python 3.9
- NumPy 2.0 dropped support for Python 3.8
- Last NumPy version supporting Python 3.8: NumPy 1.24.x

**Fix Required**: Use a conditional numpy requirement:
```toml
[build-system]
requires = [
    "scikit_build_core",
    "numpy >= 2.0; python_version >= '3.9'",
    "numpy >= 1.20, < 2.0; python_version < '3.9'"
]
```

**Additional Considerations**:
- Need to verify that the C++ Python bindings don't use NumPy 2.0-specific APIs
- May need to test binary compatibility with different NumPy versions
- Runtime dependency in `pyproject.toml` line 30-32 is already flexible (`"numpy"` without version constraint)

## 3. Project Configuration

### 3.1 requires-python Setting

**Issue**: The project explicitly declares it requires Python >= 3.9.

**Location**: `pyproject.toml` line 34:
```toml
requires-python = ">=3.9"
```

**Fix Required**: Change to:
```toml
requires-python = ">=3.8"
```

### 3.2 CI/CD Configuration

**Issue**: GitHub Actions workflows explicitly skip Python 3.8 builds.

**Locations**:
- `.github/workflows/publish-packages.yml`:
  - Line 18: `CIBW_SKIP: "cp38-* pp* gp*"`
  - Line 42: `CIBW_SKIP: "cp38-* pp* gp*"`
  - Line 68: `CIBW_SKIP: "cp38-* pp* gp*"`
  - Line 89: `CIBW_SKIP: "cp38-* pp* gp*"`

**Fix Required**: Remove `cp38-*` from the skip patterns:
```yaml
CIBW_SKIP: "pp* gp*"  # Remove cp38-* to enable Python 3.8 builds
```

**Note**: The test workflow (`.github/workflows/run-tests.yml`) only tests Python 3.9 and 3.14, so Python 3.8 should be added to the test matrix:
```yaml
matrix:
  python-version: ['3.8', '3.9', '3.14']
```

## Summary of Required Changes

### Critical Changes (Must Fix)

1. **Type stub file (`gdstk/_gdstk.pyi`)**: ~515+ changes needed
   - Replace all `list[...]` with `List[...]` (48 occurrences)
   - Replace all `dict[...]` with `Dict[...]` (5 occurrences)
   - Replace all `tuple[...]` with `Tuple[...]` (161 occurrences)
   - Replace all `Type1 | Type2` with `Union[Type1, Type2]` (306 occurrences)
   - Add imports: `from typing import List, Dict, Tuple, Set, Union`

2. **Build dependencies (`pyproject.toml`)**:
   - Update NumPy requirement to support both 1.x and 2.x based on Python version
   - Change `requires-python = ">=3.9"` to `requires-python = ">=3.8"`

3. **CI/CD configuration (`.github/workflows/`)**:
   - Remove `cp38-*` from `CIBW_SKIP` in `publish-packages.yml` (4 locations)
   - Add Python 3.8 to test matrix in `run-tests.yml`

### Verification Steps

After making these changes, the following should be verified:

1. **Type checking**: Run `mypy` or similar type checker with Python 3.8 to verify type annotations
2. **Build testing**: Attempt to build wheels for Python 3.8 on all platforms
3. **Runtime testing**: Run the full test suite with Python 3.8
4. **NumPy compatibility**: Test with both NumPy 1.24.x (for Python 3.8) and NumPy 2.x (for Python 3.9+)

## Technical Background

### Why These Features Don't Work in Python 3.8

1. **PEP 585** (Builtin generic types): Introduced in Python 3.9, allowing `list[int]` instead of `typing.List[int]`
2. **PEP 604** (Union operator): Introduced in Python 3.10, allowing `int | str` instead of `Union[int, str]`
3. **NumPy 2.0**: Dropped Python 3.8 support to modernize the codebase and remove legacy compatibility layers

### Impact Assessment

- **Type stub changes**: Large number of mechanical changes (~515+) but straightforward to automate
- **Runtime impact**: None - type stubs only affect static type checking, not runtime behavior
- **NumPy dependency**: May require conditional logic or version-specific handling in build system
- **Maintenance burden**: Supporting Python 3.8 adds complexity as it reached EOL in October 2024

## Recommendations

1. **If Python 3.8 support is critical**: Implement all changes listed above
2. **If not critical**: Consider that Python 3.8 reached End of Life (EOL) in October 2024 and most projects have moved on to newer versions
3. **Hybrid approach**: Document the incompatibilities and provide clear error messages for Python 3.8 users directing them to use an older version of gdstk if needed

## Conclusion

The gdstk library cannot currently be built for Python 3.8 due to:
1. Modern type annotation syntax (PEP 585 & PEP 604) requiring Python 3.9+/3.10+
2. NumPy 2.0 dependency requiring Python 3.9+
3. Explicit configuration excluding Python 3.8

All issues are fixable but require substantial changes to the type stub file (~515+ modifications) and updates to build configuration. Given that Python 3.8 reached EOL in October 2024, the cost-benefit of adding Python 3.8 support should be carefully considered.
