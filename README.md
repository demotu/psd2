# [psd2](https://pypi.org/project/psd2/)

Estimation of power spectral density characteristics using Welch's method

The function psd2.py from Python module psd2 estimates power spectral density characteristics using Welch's method. This function is just a wrap of the scipy.signal.welch function with estimation of some frequency characteristics and a plot.
The psd2.py returns power spectral density data, frequency percentiles of the power spectral density (for example, Fpcntile[50] gives the median power frequency in Hz); mean power frequency; maximum power frequency; total power, and plots power spectral density data.

## Installation

```bash
pip install psd2
```

Or

```bash
conda install -c duartexyz psd2
```

## Examples

```python
#Generate a test signal, a 2 Vrms sine wave at 1234 Hz, corrupted by
# 0.001 V**2/Hz of white noise sampled at 10 kHz and calculate the PSD:
>>> fs = 10e3
>>> N = 1e5
>>> amp = 2*np.sqrt(2)
>>> freq = 1234.0
>>> noise_power = 0.001 * fs / 2
>>> time = np.arange(N) / fs
>>> x = amp*np.sin(2*np.pi*freq*time)
>>> x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
>>> psd2(x, fs=freq);
```

- [psd2.ipynb](https://github.com/demotu/psd2/blob/master/docs/psd2.ipynb)

## How to cite this work

Here is a suggestion to cite this GitHub repository:

> Duarte, M. (2020) psd2: A Python module for estimation of power spectral density characteristics using Welch's method. GitHub repository, <https://github.com/demotu/psd2>.

And a possible BibTeX entry:

```tex
@misc{Duarte2020,  
    author = {Duarte, M.},
    title = {psd2: A Python module for estimation of power spectral density characteristics using Welch's method},  
    year = {2020},  
    publisher = {GitHub},  
    journal = {GitHub repository},  
    howpublished = {\url{https://github.com/demotu/psd2}}  
}
```

## License

The non-software content of this project is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/), and the software code is licensed under the [MIT license](https://opensource.org/licenses/mit-license.php).
