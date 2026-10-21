# [psd2](https://pypi.org/project/psd2/)

[![PyPI version](https://badge.fury.io/py/psd2.svg)](https://badge.fury.io/py/psd2)
[![DOI](https://zenodo.org/badge/250857887.svg)](https://zenodo.org/badge/latestdoi/250857887)

Estimation of power spectral density characteristics using Welch's method

The function psd2.py from Python module psd2 estimates power spectral density characteristics using Welch's method. This function is just a wrap of the scipy.signal.welch function with estimation of some frequency characteristics and a plot.
The psd2.py returns power spectral density data, frequency percentiles of the power spectral density (for example, Fpcntile[50] gives the median power frequency in Hz); mean power frequency; maximum power frequency; total power, and plots power spectral density data.

## Installation

```bash
pip install psd2
```

The plots (parameter `show=True`, the default) require matplotlib, which can be installed together with:

```bash
pip install "psd2[plot]"
```

Or

```bash
conda install -c duartexyz psd2
```

## Examples

```python
>>> import numpy as np
>>> from psd2 import psd2
# Generate a test signal, a 2 Vrms sine wave at 1234 Hz, corrupted by
# 0.001 V**2/Hz of white noise sampled at 10 kHz and calculate the PSD:
>>> fs = 10e3
>>> N = 100000
>>> amp = 2*np.sqrt(2)
>>> freq = 1234.0
>>> noise_power = 0.001 * fs / 2
>>> time = np.arange(N) / fs
>>> x = amp*np.sin(2*np.pi*freq*time)
>>> x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
>>> fpcntile, mpf, fmax, Ptotal, f, P = psd2(x, fs=fs, nperseg=1024)
```

More examples are in a [marimo](https://marimo.io) notebook in the [docs](https://github.com/demotu/psd2/tree/master/docs) directory. Run it in your browser, no installation needed:

| Notebook | molab | marimo.app |
|---|---|---|
| [psd2](https://molab.marimo.io/github/demotu/psd2/blob/master/docs/psd2_notebook.py) | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/demotu/psd2/blob/master/docs/psd2_notebook.py/wasm) | [![Open with marimo](https://marimo.io/shield.svg)](https://marimo.app/github.com/demotu/psd2/blob/master/docs/psd2_notebook.py) |

The notebook name links to a static preview with the outputs; the badges run the notebook in your browser with [WebAssembly](https://docs.marimo.io/guides/wasm/).

Or run it locally:

```bash
uvx marimo edit --sandbox docs/psd2_notebook.py
```

## How to cite this work

Here is a suggestion to cite this GitHub repository:

> Marcos Duarte. (2021). psd2: A Python module for estimation of power spectral density characteristics using Welch's method (Version v0.0.4). Zenodo. http://doi.org/10.5281/zenodo.4599105

And a possible BibTeX entry:

```tex
@software{marcos_duarte_2021_4599105,
  author       = {Marcos Duarte},
  title        = {{psd2: A Python module for estimation of power spectral density characteristics using Welch's method}},
  month        = mar,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {v0.0.4},
  doi          = {10.5281/zenodo.4599105},
  url          = {https://doi.org/10.5281/zenodo.4599105}
}
```

## License

The non-software content of this project is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/), and the software code is licensed under the [MIT license](https://opensource.org/licenses/mit-license.php).
