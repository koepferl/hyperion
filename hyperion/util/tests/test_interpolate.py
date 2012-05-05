import pytest
import numpy as np
from numpy.testing import assert_array_almost_equal_nulp

from ..interpolate import *


class GenericTests(object):

    def setup_class(self):
        raise Exception("This class should not be used directly")

    def test_interp_linear_array(self):
        x = np.linspace(1., 10., 10)
        y = self.f(x)
        xval = np.linspace(1., 10., 100)
        assert_array_almost_equal_nulp(self.interp(x, y, xval), self.f(xval), 10)

    def test_interp_linear_scalar(self):
        x = np.linspace(1., 10., 10)
        y = self.f(x)
        xval = 4.
        assert_array_almost_equal_nulp(self.interp(x, y, xval), self.f(xval), 10)

    def test_interp_linear_array_invalid(self):
        x = np.linspace(1., 10., 10)
        y = self.f(x)
        xval = np.linspace(0., 10., 100)
        with pytest.raises(Exception) as exc:
            self.interp(x, y, xval)
        assert exc.value.args[0] == 'x values are out of interpolation bounds'

    def test_interp_linear_scalar_invalid(self):
        x = np.linspace(1., 10., 10)
        y = self.f(x)
        xval = 11.
        with pytest.raises(Exception) as exc:
            self.interp(x, y, xval)
        assert exc.value.args[0] == 'x value is out of interpolation bounds'

    def test_interp_linear_array_fill(self):
        x = np.linspace(1., 10., 10)
        y = self.f(x)
        xval = np.linspace(0., 10., 100)
        ref = self.f(xval)
        ref[xval < x[0]] = -2.
        assert_array_almost_equal_nulp(self.interp(x, y, xval, bounds_error=False, fill_value=-2.), ref, 10)

    def test_interp_linear_scalar_fill(self):
        x = np.linspace(1., 10., 10)
        y = self.f(x)
        xval = 11.
        ref = -2.
        print self.interp(x, y, xval, bounds_error=False, fill_value=-2.)
        assert_array_almost_equal_nulp(self.interp(x, y, xval, bounds_error=False, fill_value=-2.), ref, 10)


class TestLinear(GenericTests):

    def setup_class(self):
        self.f = lambda self, x: 2 * x - 1
        self.interp = interp1d_fast


class TestLogLog(GenericTests):

    def setup_class(self):
        self.f = lambda self, x: 4. * x ** 3
        self.interp = interp1d_fast_loglog


class TestLogLin(GenericTests):

    def setup_class(self):
        self.f = lambda self, x: np.log(2. * x)
        self.interp = interp1d_fast_loglin


class TestLinLog(GenericTests):

    def setup_class(self):
        self.f = lambda self, x: np.exp(0.5 * x)
        self.interp = interp1d_fast_linlog