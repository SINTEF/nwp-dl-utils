# NWP Downloading Utilities

Contains utilities for downloading (relevant parts) of NWP products.

Currently focussing on [MetNo](https://thredds.met.no/thredds/catalog.html).

| Product | Remote Access (OPeNDAP) | Local Access (NetCDF4) | Comment |
| ---- | ---- | ---- | ---- |
| [MEPS](https://thredds.met.no/thredds/metno.html) | Yes | No | |
| [MyWaveWAM](https://thredds.met.no/thredds/fou-hi/fou-hi.html) | Yes | Yes | Broken |
| [NorKyst800m](https://thredds.met.no/thredds/fou-hi/norkyst800v2.html) | Yes | No | |

The package is pre-Alpha software. It does what we need it to do and not much more.

## Development

We'll assume you're using [Miniforge](https://github.com/conda-forge/miniforge).

Setting up a development space

```sh
conda create --name nwpdl-dev
conda activate nwpdl-dev
mamba install numpy xarray pandas pytest pyresample netCDF4 dask
conda deactivate nwpdl-dev
conda activate nwpdl-dev
```

To run the tests, simply run `pytest` in the base directory.

## Development Mode

You can use development mode to make the current version of the code available to other packages. To proceed, enter the virtual environment of whatever program you're working on, navigate to the `./nwp_dl_utils` root directory, remove the existing installation of `nwp-dl-utils` (if it exists), and install it in development mode, viz.

```sh
pip uninstall nwp-dl-utils
pip install --editable .
```

When done, remove, and reinstall the version from `PyPI`, viz.

```sh
pip uninstall nwl-dl-utils
pip install --ugrade nwp-dl-utils
```

This needs `pip>=21.3`, see [here](https://stackoverflow.com/a/69711730) and [here](https://pip.pypa.io/en/stable/news/#v21-3). You can upgrade Pip via `pip install --upgrade pip`.

## Build and Distribute

Setup environment

```sh
conda create --name nwpdl-build
conda activate nwpdl-build
pip install --upgrade pip
pip install --upgrade build
pip install --upgrade twine
```

Build and upload

```sh
python -m build
python -m twine upload --repository testpypi dist/* 
```

Drop `--repository testpypi` to upload to real PyPI.

Test build

```sh
conda create --name nwpdl-test
conda activate nwpdl-test
pip install --index-url https://test.pypi.org/simple/ --no-deps nwp-dl-utils
```

Drop `--index-url https://test.pypi.org/simple/ --no-deps` to download from real PyPI.

## References

1. https://packaging.python.org/en/latest/tutorials/packaging-projects/.
2. https://setuptools.pypa.io/en/latest/userguide/development_mode.html

## Blame and Contact

- Volker Hoffmann (volker.hoffmann@sintef.no)
