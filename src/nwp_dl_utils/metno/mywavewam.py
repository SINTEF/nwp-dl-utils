import logging
import os
import subprocess

import xarray as xr

from ..utils import get_indices_at_coordinates, get_indices_at_time


def download_hourly_for_single_day(
    date, region="midtnorge", basedir=".", force=False, quiet=False
):
    year = int(date.split("-")[0])
    month = int(date.split("-")[1])
    day = int(date.split("-")[2])
    url = (
        "https://thredds.met.no/thredds/fileServer/fou-hi/mywavewam800mhf/mywavewam800_%s.an.%04d%02d%02d18.nc"  # noqa: E501
        % (region, year, month, day)
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


def load_to_sequence(ts, lats, lons):
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

    logging.debug("Constructing URL")
    url = _construct_url()
    logging.info("Opening Dataset at %s" % url)
    with xr.open_dataset(url) as ds:
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
    return data
