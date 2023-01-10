import numpy as np
import pyresample


def get_indices_at_coordinates(ds, lats_req, lons_req):
    """
    use a kdtree to find the nearest neighbours to the requested coordinates
    (lats_req,lon_req) on the (lat,lon) grid included in the nwp product. works for
    multiples (lat,lon). see also https://stackoverflow.com/a/40044540.

    for example, if you pass lats_req = [60,60] and lons_req = [10,10], you get
    back [387,387] and [328,328]

    :param ds: xarray NWP product dataset
    :param lats_req: ndarray/list of requested latitudes
    :param lons_req: ndarray/list of requested longitudes
    :returns: list of x and y indices into NWP array
    :rtype: tuple
    """

    # load grids
    lon_grid = ds["longitude"][:].data  # 2D array
    lat_grid = ds["latitude"][:].data  # 2D array

    grid = pyresample.geometry.GridDefinition(lons=lon_grid, lats=lat_grid)
    swath = pyresample.geometry.SwathDefinition(lons=lons_req, lats=lats_req)

    # nearest neighbours (wrt great circle distance) in the grid
    _, _, index_array, distance_array = pyresample.kd_tree.get_neighbour_info(
        source_geo_def=grid,
        target_geo_def=swath,
        radius_of_influence=50000,
        neighbours=1,
    )

    # unflatten the indices
    index_array_2d = np.unravel_index(index_array, grid.shape)
    # print(index_array_2d)
    # print(index_array_2d[0][0])
    # print(index_array_2d[1][0])
    # print(lon_grid[387, 328]) # correct
    # print(lon_grid[328, 387]) # wrong
    # print(lat_grid[387, 328]) # correct
    # print(lat_grid[328, 387]) # wrong
    # sys.exit()

    # return
    xindices = index_array_2d[0]
    yindices = index_array_2d[1]
    return xindices, yindices
