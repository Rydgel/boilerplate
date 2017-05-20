import pytest
import os
import shutil
import sys

basedir = os.path.abspath(os.path.dirname(__file__))


def main():
    argv = []
    argv.extend(sys.argv[1:])
    pytest.main(argv)

    try:
        os.remove(os.path.join(basedir, '.coverage'))
    except OSError:
        pass

    try:
        shutil.rmtree(os.path.join(basedir, '.cache'))
    except OSError:
        pass

    try:
        shutil.rmtree(os.path.join(basedir, 'tests/.cache'))
    except OSError:
        pass


if __name__ == '__main__':
    main()
