import asyncio
import logging
from typing import List, Tuple, Type

logger = logging.getLogger("nibe").getChild(__name__)


class TooManyTriesException(Exception):
    pass


def retry(retry_delays: List[float], exeptions: Tuple[Type[Exception]]):
    def func_wrapper(f):
        async def wrapper(*args, **kwargs):
            delays = retry_delays.copy()
            while True:
                try:
                    return await f(*args, **kwargs)
                except Exception as e:
                    if not isinstance(e, exeptions):
                        raise

                    logger.warning(
                        f"Attempt failed ({len(delays)} left). Exception: {e}"
                    )

                    if delays:
                        delay = delays.pop(0)
                        if delay > 0:
                            logger.debug(f"Sleeping {delay} before retry")
                            await asyncio.sleep(delay)
                    else:
                        raise TooManyTriesException() from e

        return wrapper

    return func_wrapper
