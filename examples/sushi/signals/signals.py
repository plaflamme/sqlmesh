import typing as t
from sqlmesh.core.scheduler import signal_factory, Batch, Signal


class AlwaysReadySignal(Signal):
    def check_intervals(self, batch: Batch) -> t.Union[bool, Batch]:
        return True


@signal_factory
def my_signal_factory(
    signal_metadata: t.Dict[str, t.Union[str, int, float, bool]],
) -> Signal:
    signal_kind = signal_metadata.get("kind", None)
    if signal_kind == "AlwaysReady":
        return AlwaysReadySignal()
    raise ValueError(f"unknown signal kind {signal_kind}")
