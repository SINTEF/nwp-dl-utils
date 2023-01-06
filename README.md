# NWP Downloading Utilities

Contains utilities for downloading (relevant parts) of NWP products.

Currently limited to [MEPS product from the Norwegian Meteorological Office][https://thredds.met.no/thredds/metno.html].

Products are accessed remotely using OPeNDAP and only specifically requested data is downloaded.

## Development

Setting up a development space

```sh
conda create --name nwpdl-dev python=3.9
conda activate nwpdl-dev
conda install numpy xarray pandas
conda install -c conda-forge pyresample
conda install -c conda-forge netCDF4
conda deactivate nwpdl-dev
conda activate nwpdl-dev
```

## Blame and Contact

- Volker Hoffmann (volker.hoffmann@sintef.no)
