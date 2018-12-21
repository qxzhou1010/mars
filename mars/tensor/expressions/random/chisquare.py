#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 1999-2018 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np

from .... import operands
from .core import TensorRandomOperandMixin, handle_array


class TensorChisquare(operands.Chisquare, TensorRandomOperandMixin):
    __slots__ = '_df', '_size'
    _input_fields_ = ['_df']

    def __init__(self, state=None, size=None, dtype=None, gpu=None, **kw):
        dtype = np.dtype(dtype) if dtype is not None else dtype
        super(TensorChisquare, self).__init__(_state=state, _size=size,
                                              _dtype=dtype, _gpu=gpu, **kw)

    def __call__(self, df, chunks=None):
        return self.new_tensor([df], self._size, raw_chunks=chunks)


def chisquare(random_state, df, size=None, chunks=None, gpu=None, **kw):
    r"""
    Draw samples from a chi-square distribution.

    When `df` independent random variables, each with standard normal
    distributions (mean 0, variance 1), are squared and summed, the
    resulting distribution is chi-square (see Notes).  This distribution
    is often used in hypothesis testing.

    Parameters
    ----------
    df : float or array_like of floats
         Number of degrees of freedom, should be > 0.
    size : int or tuple of ints, optional
        Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
        ``m * n * k`` samples are drawn.  If size is ``None`` (default),
        a single value is returned if ``df`` is a scalar.  Otherwise,
        ``mt.array(df).size`` samples are drawn.
    chunks : int or tuple of int or tuple of ints, optional
        Desired chunk size on each dimension
    gpu : bool, optional
        Allocate the tensor on GPU if True, False as default

    Returns
    -------
    out : Tensor or scalar
        Drawn samples from the parameterized chi-square distribution.

    Raises
    ------
    ValueError
        When `df` <= 0 or when an inappropriate `size` (e.g. ``size=-1``)
        is given.

    Notes
    -----
    The variable obtained by summing the squares of `df` independent,
    standard normally distributed random variables:

    .. math:: Q = \sum_{i=0}^{\mathtt{df}} X^2_i

    is chi-square distributed, denoted

    .. math:: Q \sim \chi^2_k.

    The probability density function of the chi-squared distribution is

    .. math:: p(x) = \frac{(1/2)^{k/2}}{\Gamma(k/2)}
                     x^{k/2 - 1} e^{-x/2},

    where :math:`\Gamma` is the gamma function,

    .. math:: \Gamma(x) = \int_0^{-\infty} t^{x - 1} e^{-t} dt.

    References
    ----------
    .. [1] NIST "Engineering Statistics Handbook"
           http://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm

    Examples
    --------
    >>> import mars.tensor as mt

    >>> mt.random.chisquare(2,4).execute()
    array([ 1.89920014,  9.00867716,  3.13710533,  5.62318272])
    """
    if 'dtype' not in kw:
        kw['dtype'] = np.random.RandomState().chisquare(
            handle_array(df), size=(0,)).dtype
    size = random_state._handle_size(size)
    op = TensorChisquare(state=random_state._state, size=size, gpu=gpu, **kw)
    return op(df, chunks=chunks)
