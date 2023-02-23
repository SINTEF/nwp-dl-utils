import logging
import os
import subprocess


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
