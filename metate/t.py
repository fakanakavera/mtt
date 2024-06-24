
from fnkutils.funcs.yaml import load_yaml
import os
# get local path using os
DIR = os.path.dirname(__file__)

print(load_yaml(DIR+'/yaml/stone_handling_choices.yaml'))