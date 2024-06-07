import logging
import pprint
from typing import Dict, List

import pandas as pd
import xarray as xr

from ..utils import get_indices_at_coordinates, get_indices_at_time

URL_NORKYST800M = "https://thredds.met.no/thredds/dodsC/sea/norkyst800m/1h/aggregate_be"


def load_to_dataframe(
    timestamps: List[pd.Timestamp],
    latitudes: List[float],
    longitudes: List[float],
) -> pd.DataFrame:
    """
    Given lists of timestamps (`timestamps`), latitudes (`lats`), and longitudes (`lons`), do
    an outer loop over all timestamps and an inner loop over all locations.

    for testing, you can call the function as

    timestamps = [ pd.to_datetime('2023-10-21T00:00:00Z', utc=True),
                   pd.to_datetime('2023-12-23T00:00:00Z', utc=True),
                   pd.to_datetime('2024-01-02T00:00:00Z', utc=True) ]
    latitudes = [ 59.371235, 69.70953 ]
    longitudes = [ 5.216333, 18.363983 ]

    viz.

    >>> nwp_dl_utils.metno.norkyst800m.load_to_dataframe(timestamps, latitudes, longitudes)
    timestamp   latitude  longitude  temperature   salinity
    0 2023-10-21 00:00:00+00:00  59.371235   5.216333    12.009999  33.139999
    1 2023-10-21 00:00:00+00:00  69.709530  18.363983     8.460000  33.721001
    2 2023-12-23 00:00:00+00:00  59.371235   5.216333     8.360000  34.042000
    3 2023-12-23 00:00:00+00:00  69.709530  18.363983     5.060000  33.946999
    4 2024-01-02 00:00:00+00:00  59.371235   5.216333     7.200000  33.073002
    5 2024-01-02 00:00:00+00:00  69.709530  18.363983     4.460000  33.970001

    :param ts: ndarray/list of timestamps
    :param lats: ndarray/list of latitudes (EPSG 4326)
    :param lons: ndarray/list of longitudes (EPSG 4326)
    :return: pandas dataframe with data from model
    :rtype: pandas dataframe
    """

    # define variables of interest
    variables_of_interest = [
        "temperature",
        "salinity",
    ]

    # now go through the sequence of (ts,lats,lons) and extract the variables above
    # print(ts)
    # print(lats)
    # print(lons)

    logging.info("Opening Remote Dataset at %s" % URL_NORKYST800M)
    ds = xr.open_dataset(URL_NORKYST800M)

    logging.debug("Querying Indices")
    xindices, yindices = get_indices_at_coordinates(
        ds, latitudes, longitudes, fields="latlon_short"
    )
    tindices = get_indices_at_time(ds, timestamps)
    logging.debug("Retrieved %i Spatial Indices (x): %s" % (len(xindices), xindices))
    logging.debug("Retrieved %i Spatial Indices (y): %s" % (len(yindices), yindices))
    logging.debug("Retrieved %i Time Indices: %s" % (len(tindices), tindices))

    data = {}
    data["timestamp"] = []
    data["latitude"] = []
    data["longitude"] = []
    for variable in variables_of_interest:
        data[variable] = []
    logging.info("Sweeping Timestamps")
    for kk_ts, ts in enumerate(timestamps):
        tidx = tindices[kk_ts]
        logging.info("Timestamp (Index) = %s (%i)" % (ts, tidx))
        for kk_spatial in range(len(xindices)):
            xidx = xindices[kk_spatial]
            yidx = yindices[kk_spatial]
            logging.debug("(tidx,xidx,yidx) = (%i,%i,%i)" % (tidx, xidx, yidx))
            logging.debug(
                "(Timestamp,Lat/Req,Lon/Req) = (%s,%.3f,%.3f)"
                % (ts, latitudes[kk_spatial], longitudes[kk_spatial])
            )
            logging.debug(
                "(Timestamp,Lat/Rcv,Lon/Rcv) = (%s,%.3f,%.3f)"
                % (ts, ds["lat"][xidx, yidx].data, ds["lon"][xidx, yidx].data)
            )
            for variable in variables_of_interest:
                variable_value = float(ds[variable][tidx, 0, xidx, yidx].data)
                logging.debug("Variable %s = %.2f" % (variable, variable_value))
                data[variable].append(variable_value)
            data["timestamp"].append(ts)
            data["latitude"].append(latitudes[kk_spatial])
            data["longitude"].append(longitudes[kk_spatial])

    logging.info("Closing Dataset")
    ds.close()

    logging.info("Constructing Dataframe")
    df = pd.DataFrame(data=data)

    logging.debug(data)
    logging.debug(df)

    return df
