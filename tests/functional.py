import unittest
import sys
import io

import findpydeps


class MyTestCase(unittest.TestCase):
    def test_something(self):
        old_stdout = sys.stdout
        sys.stdout = output = io.StringIO()
        args = findpydeps.parser.parse_args(["--help"])
        findpydeps.run(vars(args))
        sys.stdout = old_stdout
        with open("functional/help-message", "r") as f:
            expected = f.read()
        self.assertEqual(output.getvalue(), expected)


if __name__ == '__main__':
    unittest.main()
