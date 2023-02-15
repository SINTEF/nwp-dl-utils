import numpy as np
import nwp_dl_utils.utils as utils
import xarray as xr


def test_get_indices_at_coordinates():
    url = "https://thredds.met.no/thredds/dodsC/mepslatest/meps_lagged_6_h_latest_2_5km_latest.nc"  # noqa: E501
    with xr.open_dataset(url) as ds:
        xindices, yindices = utils.get_indices_at_coordinates(
            ds, [60.0, 61.0], [10.0, 9.0]
        )
        np.testing.assert_array_equal(xindices, np.array([390, 437]))
        np.testing.assert_array_equal(yindices, np.array([313, 295]))
