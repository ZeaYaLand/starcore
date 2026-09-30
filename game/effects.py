from dataclasses import dataclass


@dataclass(frozen=True)
class Effect:
    effect_id: str
    stat: str
    amount: int
    remaining_turns: int = 0

    @property
    def temporary(self) -> bool:
        return self.remaining_turns > 0


class EffectService:
    def __init__(self, base_stats: dict[str, int] | None = None):
        self.base_stats = dict(base_stats or {})
        self.effects: dict[str, Effect] = {}

    def apply(self, effect: Effect) -> None:
        if not effect.effect_id or not effect.stat:
            raise ValueError("effect id and stat are required")
        if effect.amount == 0:
            raise ValueError("effect amount must not be zero")
        if effect.remaining_turns < 0:
            raise ValueError("remaining turns cannot be negative")
        self.effects[effect.effect_id] = effect

    def stat(self, name: str) -> int:
        value = self.base_stats.get(name, 0)
        value += sum(effect.amount for effect in self.effects.values() if effect.stat == name)
        return value

    def tick(self) -> tuple[str, ...]:
        expired = []
        updated = {}
        for effect_id, effect in self.effects.items():
            if not effect.temporary:
                updated[effect_id] = effect
                continue
            remaining = effect.remaining_turns - 1
            if remaining <= 0:
                expired.append(effect_id)
            else:
                updated[effect_id] = Effect(effect.effect_id, effect.stat, effect.amount, remaining)
        self.effects = updated
        return tuple(expired)

    def remove(self, effect_id: str) -> bool:
        return self.effects.pop(effect_id, None) is not None
