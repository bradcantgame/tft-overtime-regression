"""Standalone reproduction of the simulator's overtime sustain rule."""

from dataclasses import asdict, dataclass
import json


ONSET_US = 1_500_000
STACK_INTERVAL_US = 1_000_000


@dataclass(frozen=True)
class EffectTrace:
    time_us: int
    overtime_stacks: int
    healing_requested: float
    healing_applied: float
    shield_requested: float
    shield_granted: float


def resolve_cast(time_us: int) -> EffectTrace:
    # The synthetic target has 20 HP missing, so the health cap won't mask the penalty.
    missing_health = 20
    healing_requested = 5
    shield_requested = 100
    stacks = max(0, 1 + (time_us - ONSET_US) // STACK_INTERVAL_US)
    multiplier = max(0.30, 1 - 0.10 * stacks)
    return EffectTrace(
        time_us=time_us,
        overtime_stacks=stacks,
        healing_requested=healing_requested,
        healing_applied=min(healing_requested * multiplier, missing_health),
        shield_requested=shield_requested,
        shield_granted=shield_requested * multiplier,
    )


if __name__ == "__main__":
    for timestamp in (ONSET_US - 1, ONSET_US, ONSET_US + 1):
        print(json.dumps(asdict(resolve_cast(timestamp))))
