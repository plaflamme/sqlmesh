import typing as t
import logging
from sqlmesh.core.scheduler import signal_factory, Batch, Signal

logger = logging.getLogger("signals")


class AlwaysReadySignal(Signal):
    def check_intervals(self, batch: Batch) -> t.Union[bool, Batch]:
        logger.info("AlwaysReady")
        return True


class NeverReadySignal(Signal):
    def check_intervals(self, batch: Batch) -> t.Union[bool, Batch]:
        logger.info("NeverReady")
        return False


@signal_factory
def sf(
    signal_metadata: t.Dict[str, t.Union[str, int, float, bool]],
) -> Signal:
    match signal_metadata["kind"]:
        case "always":
            return AlwaysReadySignal()
        case "never":
            return NeverReadySignal()
        case _:
            raise ValueError(signal_metadata["kind"])
