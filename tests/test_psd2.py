import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from psd2 import psd2

FS = 10e3


def _sine_in_noise(seed=0, n=100000):
    """2 Vrms sine at 1234 Hz with 0.001 V**2/Hz of white noise (scipy example)."""
    t = np.arange(n) / FS
    noise = np.random.default_rng(seed).normal(scale=np.sqrt(0.001*FS/2), size=n)
    return 2*np.sqrt(2)*np.sin(2*np.pi*1234.0*t) + noise


def test_sine_in_noise():
    fpcntile, mpf, fmax, Ptotal, f, P = psd2(_sine_in_noise(), fs=FS, nperseg=1024,
                                             show=False)
    assert fmax == pytest.approx(1234, abs=FS/1024)
    # total power = sine power (2**2) + noise power (0.001*FS/2)
    assert Ptotal == pytest.approx(4 + 5, rel=0.02)
    assert f.size == P.size == 1024//2 + 1


def test_white_noise_frequencies():
    # flat spectrum from 0 to FS/2: mean and median frequencies are FS/4
    x = np.random.default_rng(1).normal(size=100000)
    fpcntile, mpf, fmax, Ptotal, f, P = psd2(x, fs=FS, nperseg=1024, show=False)
    assert mpf == pytest.approx(FS/4, rel=0.02)
    assert fpcntile[50] == pytest.approx(FS/4, rel=0.02)
    assert Ptotal == pytest.approx(np.var(x), rel=0.02)


def test_frequency_percentiles():
    fpcntile, *_ = psd2(_sine_in_noise(), fs=FS, nperseg=1024, show=False)
    assert fpcntile.size == 101
    assert (np.diff(fpcntile) >= 0).all()
    assert fpcntile[0] == 0
    assert fpcntile[100] <= FS/2


def test_default_segment_length_is_half_of_data():
    x = _sine_in_noise(n=1000)
    *_, f, P = psd2(x, fs=FS, show=False)
    assert f.size == 500//2 + 1


def test_default_window_is_hann():
    x = _sine_in_noise(n=4096)
    r0 = psd2(x, fs=FS, nperseg=512, show=False)
    r1 = psd2(x, fs=FS, nperseg=512, window='hann', show=False)
    assert r0[1] == r1[1] and (r0[5] == r1[5]).all()


@pytest.mark.parametrize("scales, xscale, yscale", [('linear', 'linear', 'linear'),
                                                    ('semilogy', 'linear', 'log'),
                                                    ('semilogx', 'log', 'linear'),
                                                    ('loglog', 'log', 'log')])
def test_plot_scales(scales, xscale, yscale):
    _, ax = plt.subplots()
    psd2(_sine_in_noise(n=4096), fs=FS, nperseg=512, show=True, ax=ax, scales=scales,
         xlim=[10, 2000])
    assert (ax.get_xscale(), ax.get_yscale()) == (xscale, yscale)
    assert ax.get_xlim() == (10, 2000)
    plt.close('all')
