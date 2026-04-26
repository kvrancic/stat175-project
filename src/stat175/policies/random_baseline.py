"""Random edge removal — Outline policy 1, the trivial baseline.

Picks edges uniformly at random until the cost budget is exhausted. Useful as
a sanity floor: every other policy must beat this.
"""

from __future__ import annotations

import numpy as np

from .base import Policy, PolicyInput


class RandomEdgeRemoval:
    name = "random"

    def select(self, inputs: PolicyInput) -> np.ndarray:
        if inputs.budget <= 0:
            return np.empty(0, dtype=np.int64)
        rng = np.random.default_rng(inputs.seed)
        order = rng.permutation(inputs.edges.shape[0])
        cumulative = np.cumsum(inputs.costs[order])
        return order[cumulative <= inputs.budget].astype(np.int64)


_: Policy = RandomEdgeRemoval()
