import os, sys
from satpy.utils import debug_on
import pyninjotiff
debug_on()
from satpy import Scene
from mpop.projector import get_area_def
import argparse
import yaml

parser = argparse.ArgumentParser(description='Turn an image into a NinjoTiff.')
parser.add_argument('--cfg', dest='cfg', action="store", help="YAML configuration as an alternative to the command line input for NinJo metadata.")
parser.add_argument('--input_dir', dest='input_dir', action="store", help="Directory with input data, that must contain a timestamp in the filename.")
parser.add_argument('--chan_id', dest='chan_id', action="store", help="Channel ID", default="9999")
parser.add_argument('--sat_id', dest='sat_id', action="store", help="Satellite ID", default="8888")
parser.add_argument('--data_cat', dest='data_cat', action="store", help="Category of data (one of GORN, GPRN, PORN)", default="GORN")
parser.add_argument('--area', dest='areadef', action="store", help="Area name, the definition must exist in your areas.def configuration file.", default="nrEURO1km_NPOL_COALeqc")
parser.add_argument('--ph_unit', dest='ph_unit', action="store", help="Physical unit.", default="CELSIUS")
parser.add_argument('--data_src', dest='data_src', action="store", help="Data source", default="EUMETCAST")
args = parser.parse_args()

if (args.input_dir != None):
    os.chdir(args.input_dir)

cfg = vars(args)
if (args.cfg != None):
    with open(args.cfg, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

narea = get_area_def(args.areadef)
global_data = Scene(sensor="images", reader="generic_image", area=narea)
global_data.load(['image'])
print(global_data['image'].info)
global_data['image'].info['area'] = narea
fname = global_data['image'].info['filename']
ofname = fname[:-3] + "tif"
#print(global_data)
#global_data.save_dataset('image', filename="out.png", writer="simple_image")
global_data.save_dataset('image', filename=ofname, writer="ninjotiff",
                      sat_id=cfg['sat_id'],
                      chan_id=cfg['chan_id'],
                      data_cat=cfg['data_cat'],
                      data_source=cfg['data_src'],
                      physic_unit=cfg['ph_unit'])
