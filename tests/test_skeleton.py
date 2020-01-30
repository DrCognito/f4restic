# -*- coding: utf-8 -*-

import pytest
from f4restic.skeleton import fib

__author__ = "Matt Chadwick"
__copyright__ = "Matt Chadwick"
__license__ = "gpl3"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
