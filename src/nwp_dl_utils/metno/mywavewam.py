import glob
import logging
import os
import subprocess
import sys

import xarray as xr

from ..utils import get_indices_at_coordinates, get_indices_at_time


def download_hourly_for_single_day(
    date, region="midtnorge", basedir=".", force=False, quiet=False
):
    year = int(date.split("-")[0])
    month = int(date.split("-")[1])
    day = int(date.split("-")[2])
    product_string_with_region = "mywavewam800"
    if region == "midtnorge":
        product_string_with_region += "mhf"
    elif region == "skagerak":
        product_string_with_region += "shf"
    else:
        logging.critical("Invalid Region. Skipping Download. Terminating.")
        sys.exit(1)
    url = (
        "https://thredds.met.no/thredds/fileServer/fou-hi/%s/mywavewam800_%s.an.%04d%02d%02d18.nc"  # noqa: E501
        % (product_string_with_region, region, year, month, day)
    )
    fname = url.split("/")[-1]
    if os.path.exists(fname):
        logging.warning("File Exists: %s" % fname)
        if force is True:
            logging.warning("Forcing Download.")
            if quiet is True:
                subprocess.run(["wget", "--quiet", "-O", fname, url])
            else:
                subprocess.run(["wget", "-O", fname, url])
        else:
            logging.warning("Skipping Download.")
    else:
        if quiet is True:
            subprocess.run(["wget", "--quiet", "-O", fname, url])
        else:
            subprocess.run(["wget", "-O", fname, url])

    return fname


def _construct_url(product_id="mywavewam800m_skagerrak_hourly"):
    if product_id == "mywavewam800m_skagerrak_hourly":
        url = "https://thredds.met.no/thredds/dodsC/fou-hi/mywavewam800s_be"
    return url


def _construct_filelist(local_cache_dir, region="skagerak"):
    flist = sorted(glob.glob("%s/mywavewam800_%s.an.*.nc" % (local_cache_dir, region)))
    logging.debug("Local NetCDF4 Files: %s" % flist)
    return sorted(glob.glob("%s/mywavewam800_%s.an.*.nc" % (local_cache_dir, region)))


def load_to_sequence(ts, lats, lons, local_cache_dir=None):
    """
    given a sequence of timestamps (`ts`), latitudes (`lats`), and longitudes (`lons`),
    load the requested NWP variables for each triple of (ts,lat,lon). for testing, you
    can call the function as

    ts = [pd.to_datetime('2017-12-21T00:00:00Z'), pd.to_datetime('2017-12-23T00:00:00Z')]
    lats = [58.8806,58.12]
    lons = [10.2103,10.01]
    nwp_dl_utils.metno.mywavewam.load_to_sequence(ts, lats, lons)

    :param ts: ndarray/list of timestamps
    :param lats: ndarray/list of latitudes (EPSG 4326)
    :param lons: ndarray/list of longitudes (EPSG 4326)
    :return: sequence of NWP data
    :rtype: dict
    """

    # define variables of interest
    variables_standard_name = [
        "wind_speed",
        "wind_to_direction",
        "sea_surface_wave_significant_height",
        "sea_surface_wave_to_direction",
        "sea_surface_wave_peak_period_from_variance_spectral_density",
    ]
    variables_short_name = {
        "wind_speed": "ff",
        "wind_to_direction": "dd",
        "sea_surface_wave_significant_height": "hs",
        "sea_surface_wave_to_direction": "thq",
        "sea_surface_wave_peak_period_from_variance_spectral_density": "tp",
    }

    # now go through the sequence of (ts,lats,lons) and extract the variables above
    # print(ts)
    # print(lats)
    # print(lons)

    if local_cache_dir is None:
        logging.info("Opening Remote Dataset at %s" % _construct_url())
        ds = xr.open_dataset(_construct_url())
    else:
        logging.info("Opening Local Dataset at %s" % local_cache_dir)
        # https://docs.xarray.dev/en/stable/user-guide/io.html#reading-multi-file-datasets
        # https://docs.xarray.dev/en/stable/generated/xarray.open_mfdataset.html
        ds = xr.open_mfdataset(
            _construct_filelist(local_cache_dir),
            combine="by_coords",
            data_vars="minimal",
            coords="minimal",
            compat="override",
        )

    logging.debug("Getting Spatial Indices")
    xindices, yindices = get_indices_at_coordinates(ds, lats, lons)
    logging.debug("Getting Temporal Indices")
    tindices = get_indices_at_time(ds, ts)
    data = {}
    for variable in variables_standard_name:
        data[variable] = []
    for kk in range(len(ts)):
        logging.debug("Timeslice %i/%i (%s))" % (kk + 1, len(ts), ts[kk]))
        tidx = tindices[kk]
        xidx = xindices[kk]
        yidx = yindices[kk]
        for variable in variables_standard_name:
            logging.debug("Variable %s" % variable)
            data[variable].append(
                float(ds[variables_short_name[variable]][tidx, xidx, yidx].data)
            )

    logging.info("Closing Dataset")
    ds.close()

    return data
