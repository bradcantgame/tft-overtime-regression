import unittest

from overtime import EffectTrace, resolve_cast


class OvertimeRegressionTest(unittest.TestCase):
    def test_cast_uses_overtime_stack_at_resolution(self):
        cases = (
            EffectTrace(1_499_999, 0, 5, 5, 100, 100),
            EffectTrace(1_500_000, 1, 5, 4.5, 100, 90),
            EffectTrace(1_500_001, 1, 5, 4.5, 100, 90),
        )
        for expected in cases:
            with self.subTest(time_us=expected.time_us):
                self.assertEqual(resolve_cast(expected.time_us), expected)
