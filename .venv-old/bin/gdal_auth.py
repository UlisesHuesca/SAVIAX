#!/home/savia/SAVIAX/venv/bin/python3.10

import sys
# import osgeo.utils.gdal_auth as a convenience to use as a script
from osgeo.utils.gdal_auth import *  # noqa
from osgeo.utils.gdal_auth import main
from osgeo.gdal import deprecation_warn


deprecation_warn('gdal_auth', 'utils')
sys.exit(main(sys.argv))
