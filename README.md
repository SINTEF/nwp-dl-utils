# NWP Downloading Utilities

Contains utilities for downloading (relevant parts) of NWP products.

Currently limited to [MEPS product from the Norwegian Meteorological Office](https://thredds.met.no/thredds/metno.html).

Products are accessed remotely using OPeNDAP and only specifically requested data is downloaded.

## Development

Setting up a development space

```sh
conda create --name nwpdl-dev python=3.9
conda activate nwpdl-dev
conda install numpy xarray pandas
conda install pytest
conda install -c conda-forge pyresample
conda install -c conda-forge netCDF4
conda deactivate nwpdl-dev
conda activate nwpdl-dev
```

To run the tests, simply run `pytest` in the base directory.

## Build and Distribute

Setup environment

```sh
conda create --name nwpdl-build python=3.9
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
conda create --name nwpdl-test python=3.9
conda activate nwpdl-test
pip install --index-url https://test.pypi.org/simple/ --no-deps nwp-dl-utils
```

Drop `--index-url https://test.pypi.org/simple/ --no-deps` to download from real PyPI.

## References

1. https://packaging.python.org/en/latest/tutorials/packaging-projects/.

## Blame and Contact

- Volker Hoffmann (volker.hoffmann@sintef.no)
