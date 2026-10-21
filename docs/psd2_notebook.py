# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "numpy",
#     "psd2",
#     "scipy",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # [psd2](https://pypi.org/project/psd2)

    A Python module for estimation of power spectral density characteristics using Welch's method

    [https://pypi.org/project/psd2](https://pypi.org/project/psd2)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The function `psd2.py` ([source code](https://github.com/demotu/psd2/blob/master/psd2/psd2.py)) from Python module `psd2` estimates power spectral density characteristics using Welch's method. This function is just a wrap of the scipy.signal.welch function with estimation of some frequency characteristics and a plot.
    The `psd2.py` returns power spectral density data, frequency percentiles of the power spectral density (for example, Fpcntile[50] gives the median power frequency in Hz); mean power frequency; maximum power frequency; total power, and plots power spectral density data.

    Let's exemplify the use of `psd2.py`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Installation

    ```bash
    pip install "psd2[plot]"
    ```

    Or

    ```bash
    conda install -c duartexyz psd2
    ```

    To run this [marimo](https://marimo.io) notebook in an isolated environment with all its dependencies:

    ```bash
    uvx marimo edit --sandbox psd2_notebook.py
    ```
    """)
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import fft, integrate, signal

    from psd2 import psd2

    return fft, integrate, mo, np, plt, psd2, signal


@app.cell
def _(mo, psd2):
    mo.doc(psd2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sine wave in noise

    Generate a test signal, a 2 Vrms sine wave at 1234 Hz, corrupted by 0.001 V²/Hz of white noise sampled at 10 kHz, and calculate the PSD:
    """)
    return


@app.cell
def _(np, plt):
    fs = 10e3
    N = 100000
    _rng = np.random.default_rng(42)
    amp = 2*np.sqrt(2)
    noise_power = 0.001 * fs / 2
    time = np.arange(N) / fs
    x = amp*np.sin(2*np.pi*1234.0*time)
    x += _rng.normal(scale=np.sqrt(noise_power), size=time.shape)

    _fig, _ax = plt.subplots(figsize=(10, 5))
    _ax.plot(time[:500], x[:500], linewidth=2)
    _ax.set_xlabel('Time [s]')
    _ax.set_ylabel('Amplitude [V]')
    _ax.set_title('First 50 ms of the signal')
    _fig
    return fs, x


@app.cell
def _(fs, psd2, x):
    fpcntile, mpf, fmax, Ptotal, f, P = psd2(x, fs=fs, nperseg=1024, scales='semilogy')
    return (Ptotal,)


@app.cell(hide_code=True)
def _(Ptotal, mo):
    mo.md(rf"""
    The total power is {Ptotal:.2f} V², the power of the sine wave (2² = 4 V²) plus the power of the noise (0.001 V²/Hz × 5000 Hz = 5 V²).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Periodogram and Welch's method

    A signal with two sine waves (5 Hz and 20 Hz) and white noise, sampled at 100 Hz, and its power spectral density estimated by the periodogram, by Welch's method with a single segment, and by a quick and simple use of the FFT:
    """)
    return


@app.cell
def _(fft, np, signal):
    freq = 100.0
    t = np.arange(0, 5, .01)
    y = 2*np.sin(5*np.pi*2*t) + np.sin(2*np.pi*20*t) + np.random.default_rng(1).standard_normal(t.size)
    n = y.size

    fp, Pp = signal.periodogram(y, freq, window='boxcar', nfft=n)
    fw, Pw = signal.welch(y, freq, window='hann', nperseg=n, noverlap=0, nfft=n)
    # quick and simple PSD
    Pf = np.abs(fft.fft(y - np.mean(y), n))[:n//2]**2/n/freq
    Pf[1:-1] = 2*Pf[1:-1]
    ff = np.linspace(0, freq/2, len(Pf))
    return ff, fp, fw, freq, n, t, y, Pf, Pp, Pw


@app.cell
def _(Pf, Pp, Pw, ff, fp, fw, plt, t, y):
    _fig, (_ax1, _ax2, _ax3, _ax4) = plt.subplots(4, 1, figsize=(12, 10))
    _ax1.set_title('Temporal domain', fontsize=18)
    _ax1.plot(t, y, 'b', linewidth=2)
    _ax1.set_xlabel('Time [s]')
    _ax1.set_ylabel('y [V]')
    for _ax, _f, _P, _title in [(_ax2, fp, Pp, 'Periodogram'),
                                (_ax3, fw, Pw, "Welch's method (one segment, hann window)"),
                                (_ax4, ff, Pf, 'FFT')]:
        _ax.set_title(_title, fontsize=18)
        _ax.plot(_f, _P, 'r', linewidth=2)
        _ax.set_xlabel('Frequency [Hz]')
        _ax.set_ylabel('PSD(y) $[V^2/Hz]$')
    for _ax in (_ax1, _ax2, _ax3, _ax4):
        _ax.locator_params(axis='both', nbins=5)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The frequency characteristics can be calculated from the power spectral density, for example, the mean power frequency:

    $$ F_{mean} = \frac{ \sum_{i=1}^{N} F_i P_i }{ \sum_{i=1}^{N} P_i } $$

    and the median (50%) and 95% power frequencies, the frequencies below which there are 50% and 95% of the total power:
    """)
    return


@app.cell
def _(freq, integrate, n, np, signal, y):
    _F, _P = signal.welch(y, fs=freq, window='hann', nperseg=n//2, noverlap=n//4, nfft=n//2)
    _A = integrate.cumulative_trapezoid(_P, _F, initial=0)
    fm = integrate.trapezoid(_F*_P, _F)/integrate.trapezoid(_P, _F)
    f50 = _F[np.nonzero(_A >= 0.5*_A[-1])[0][0]]
    f95 = _F[np.nonzero(_A >= .95*_A[-1])[0][0]]
    print('Mean: %.2f Hz, median: %.2f Hz, 95%%: %.2f Hz' % (fm, f50, f95))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Which is what the function `psd2` calculates (with the same parameters for Welch's method):
    """)
    return


@app.cell
def _(freq, n, psd2, y):
    fp2, mf2, fmax2, Ptot2, F2, P2 = psd2(y, fs=freq, nperseg=n//2, noverlap=n//4,
                                          nfft=n//2, scales='linear', units='V')
    print('Mean: %.2f Hz, median: %.2f Hz, 95%%: %.2f Hz' % (mf2, fp2[50], fp2[95]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Interactive example

    Change the length of the segments for Welch's method (`nperseg`): longer segments give a finer frequency resolution, but a noisier estimate of the power spectral density:
    """)
    return


@app.cell
def _(mo):
    nperseg = mo.ui.slider(steps=[64, 128, 256, 512, 1024, 2048, 4096], value=1024,
                           label='nperseg', show_value=True)
    scales = mo.ui.dropdown(['linear', 'semilogy', 'semilogx', 'loglog'], value='semilogy',
                            label='scales')
    mo.hstack([nperseg, scales], justify='start', gap=4)
    return nperseg, scales


@app.cell
def _(fs, nperseg, psd2, scales, x):
    psd2(x, fs=fs, nperseg=nperseg.value, scales=scales.value,
         xlim=[10, fs/2] if scales.value in ('semilogx', 'loglog') else None)
    return


if __name__ == "__main__":
    app.run()
