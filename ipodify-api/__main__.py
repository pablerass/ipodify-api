# -*- coding: utf-8 -*-
import sys

from .app import app


def main(args=None):
    app.run()


if __name__ == "__main__":
    sys.exit(main(sys.argv))