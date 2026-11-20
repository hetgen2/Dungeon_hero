import os
import sys
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    suite = unittest.defaultTestLoader.discover(os.path.join(ROOT, "tests"), top_level_dir=ROOT)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("\nВСЕ ТЕСТЫ ПРОШЛИ" if result.wasSuccessful() else "\nНЕ ВСЕ ТЕСТЫ ПРОШЛИ")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
