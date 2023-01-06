import numpy as np
import pyresample


def get_indices_at_coordinates(ds, latitude, longitude):
    """
    use a kdtree to find the nearest neighbours to the requested lon,lat
    on the lat,lon grid included in the nwp product
    cf. https://stackoverflow.com/a/40044540
    """

    # requested coordinates
    lon_req = [longitude]
    lat_req = [latitude]
    # lon_req = [config["location"]["lon"]]
    # lat_req = [config["location"]["lat"]]

    # load grids
    lon_grid = ds["longitude"][:].data  # 2D array
    lat_grid = ds["latitude"][:].data  # 2D array

    grid = pyresample.geometry.GridDefinition(lons=lon_grid, lats=lat_grid)
    swath = pyresample.geometry.SwathDefinition(lons=lon_req, lats=lat_req)

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
    yidx = index_array_2d[0][0]  # should be 387
    xidx = index_array_2d[1][0]  # should be 328
    return xidx, yidx
