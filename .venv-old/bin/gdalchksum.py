#!/home/savia/SAVIAX/venv/bin/python3.10

import sys
# import osgeo.utils.gdalchksum as a convenience to use as a script
from osgeo.utils.gdalchksum import *  # noqa
from osgeo.utils.gdalchksum import main
from osgeo.gdal import deprecation_warn


deprecation_warn('gdalchksum', 'utils')
sys.exit(main(sys.argv))
