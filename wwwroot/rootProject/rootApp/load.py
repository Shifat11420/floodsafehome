from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from rootApp.models import JeffersonbuildingdataFSH


JeffersonbuildingdataFSH_mapping = {
    'FID_1' : 'FID_1',
    'BLDG_ID' : 'BLDG_ID',
    'HEIGHT' : 'HEIGHT',
    'FOOTPRINT' : 'FOOTPRINT_',         #
    'address' : 'ADDRESS',
    'street' : 'STREET',
    'no_floors' : 'NO_FLOORS',
    'DATA_YEAR' : 'DATA_YEAR',
    'SFT' : 'SFT',
    'Area_SqMet' : 'Area_SqMet',
    'FloodDepth' : 'FloodDepth',
    'FloodDep_1' : 'FloodDep_1',
    'FloodDep_2' : 'FloodDep_2',
    'FloodDep_3' : 'FloodDep_3',
    'ElevationU' : 'ElevationU',
    'Elevation' : 'Elevation_',                #
    'Elevatio_1' : 'Elevatio_1',
    'FID_2' : 'FID_2',
    'Source' : 'Source',
    'u_intercept' : 'u_intercep',
    'a_slope' : 'a_slope',
    'Latitude' : 'Latitude',
    'Longitude' : 'Longitude',
    'FloodZone' : 'FloodZone',
    'Parish' : 'Parish',
    'mpoint' : 'MULTIPOINT',
}

JeffersonbuildingdataFSH_shp = Path(__file__).resolve().parent / 'data' / 'JeffersonParishBuildingData.shp'

def run(verbose=True):
    lm = LayerMapping(JeffersonbuildingdataFSH, JeffersonbuildingdataFSH_shp, JeffersonbuildingdataFSH_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)