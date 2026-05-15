"""Vega-Lite specification traversal helpers."""

from __future__ import annotations

from typing import Any, Iterator


COMPOSITE_KEYS = ("layer", "hconcat", "vconcat", "concat")


def iter_transforms(spec: Any) -> Iterator[dict[str, Any]]:
    if not isinstance(spec, dict):
        return
    transforms = spec.get("transform")
    if isinstance(transforms, list):
        for item in transforms:
            if isinstance(item, dict):
                yield item
    for key in COMPOSITE_KEYS:
        children = spec.get(key)
        if isinstance(children, list):
            for child in children:
                yield from iter_transforms(child)
    child_spec = spec.get("spec")
    if isinstance(child_spec, dict):
        yield from iter_transforms(child_spec)


def iter_encodings(spec: Any) -> Iterator[dict[str, Any]]:
    if not isinstance(spec, dict):
        return
    encodings = spec.get("encoding")
    if isinstance(encodings, dict):
        for value in encodings.values():
            if isinstance(value, dict):
                yield value
    for key in COMPOSITE_KEYS:
        children = spec.get(key)
        if isinstance(children, list):
            for child in children:
                yield from iter_encodings(child)
    child_spec = spec.get("spec")
    if isinstance(child_spec, dict):
        yield from iter_encodings(child_spec)


def has_filter(spec: Any) -> bool:
    return any("filter" in transform for transform in iter_transforms(spec))


def has_sort(spec: Any) -> bool:
    if any("sort" in encoding for encoding in iter_encodings(spec)):
        return True
    return any("sort" in transform or "window" in transform for transform in iter_transforms(spec))


def has_aggregate(spec: Any) -> bool:
    if any("aggregate" in encoding for encoding in iter_encodings(spec)):
        return True
    return any(
        "aggregate" in transform or "joinaggregate" in transform
        for transform in iter_transforms(spec)
    )
