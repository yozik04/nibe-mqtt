import asyncio
import unittest
from unittest.mock import AsyncMock

from nibe.exceptions import CoilReadTimeoutException

from nibe_mqtt.utils import TooManyTriesException, retry


class RetryTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop_policy().get_event_loop()

    def test_retry(self):
        coro = AsyncMock(side_effect=CoilReadTimeoutException("I failed this attempt"))
        fn = retry(retry_delays=[0], exeptions=(CoilReadTimeoutException,))(coro)

        with self.assertRaises(TooManyTriesException):
            self.loop.run_until_complete(fn("a"))

        self.assertEqual(2, coro.call_count)
        coro.assert_called_with("a")

        with self.assertRaises(TooManyTriesException):
            self.loop.run_until_complete(fn("b"))

        self.assertEqual(4, coro.call_count)
        coro.assert_called_with("b")


if __name__ == "__main__":
    unittest.main()
