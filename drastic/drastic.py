import stimela
import json
import re

INPUT = "input"
OUTPUT = "output"
MSDIR = "msdir"

MANUAL = False
CONFIG = ''

if MANUAL:
    recipe = stimela.Recipe('Make Pipeline', ms_dir=MSDIR)
    stimela.register_globals()


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    def atoi(text):
         return int(text) if text.isdigit() else text
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def json_dump(data_dict, filename='recipes.json', root='output'):
    """Dumps the computed dictionary into a json file.
    Parameters
    ----------
    data_dict : dict
        Dictionary with output results to save.
    filename : file
        Name of file to dump recipes for later runs
    root : str
        Directory to save output json file (default is current directory).
    Note
    ----
    If the `filename` file exists, it will be append, and only
    repeated recipes will be replaced.
    """
    filename = ('{:s}/{:s}'.format(root, filename))
    num = int(data_dict.keys()[0].split('_')[0])
    try:
        # Extract data from the json data file
        with open(filename) as data_file:
            data_existing = json.load(data_file)
            counter = 0
            data_keys = data_existing.keys()
            data_keys.sort(key=natural_keys)
            for d in data_keys:
                counter+=1
                cab_num = int(d.split('_')[0])
                cab_name = d.split('_')[-1]
                if cab_num >= num:
                    if d in data_dict.keys():
                        break
                    else:
                        old_recipe = data_existing.pop(d)
                        recipe_name = d.split('_')[-1]
                        data_existing['{:d}_{:s}'.format(counter+1, recipe_name)] = old_recipe
            data_existing.update(data_dict)
            data = data_existing
    except IOError:
        data = data_dict
    if data:
        with open(filename, 'w') as f:
            json.dump(data, f)


def get_data(filename='', root='output'):
    "Extracts data from the json data file"
    if filename:
        pass
    else:
       filename = 'recipes.json'
    filename = '{:s}/{:s}'.format(root, filename)
    with open(filename) as f:
        data = json.load(f)
    return data


def get_cab_num(num, recipes_file=''):
    if not num:
        try:
            data = get_data(recipes_file)
            data_keys = data.keys()
            data_keys.sort(key=natural_keys)
            for d in data_keys:
                cab_num = int(d.split('_')[0])
                num = cab_num+1
        except IOError:
            num = 1
    return num


# 1: Create a telescope measurement set

def simms(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_simulated_ms".format(num)
    cab = '{}_simms'.format(num)
    recipe.add("cab/simms",
               step,
               parameters,
               input=INPUT,
               output=OUTPUT,
               label="{}_Simulated_MS:: simulate ms".format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


# 2: Simulate visibility data with noise and calibration (propagation) effects

def simulator(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_generate_data".format(num)
    cab = '{}_simulator'.format(num)
    recipe.add("cab/simulator",
               step,
               parameters,
               input=INPUT,
               output=OUTPUT,
               label="{}_Generate_data:: simulating data".format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


# 3: Calibration

def meqtrees(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_meq_cal".format(num)
    cab = '{}_calibrator'.format(num)
    recipe.add('cab/calibrator',
               step,
               parameters,
               input=INPUT,
               output=OUTPUT,
               label="{}_meq_cal:: Calibrate".format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


def cubical(recipe, num, parameters):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_cub_cal".format(num)
    cab = '{}_cubical'.format(num)
    recipe.add('cab/cubical',
               step,
               parameters,
               input=INPUT,
               output=OUTPUT,
               shared_memory='150Gb',
               label="{}_cub_cal:: Calibrate".format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


# 7: Imaging

def wsclean(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_image_wsclean".format(num)
    cab = '{}_wsclean'.format(num)
    recipe.add('cab/wsclean',
               step,
               parameters,
               input=INPUT,
               output=OUTPUT,
               label='{}_image_wsclean:: image data'.format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


def casa_tclean(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_image_tclean".format(num)
    cab = '{}_casa_tclean'.format(num)
    recipe.add('cab/casa_tclean',
               step,
               parameters,
               input=INPUT,
               output=OUTPUT,
               label='{}_image_tclean:: image data'.format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


def casa_clean(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_image_clean".format(num)
    cab = '{}_casa_clean'.format(num)
    recipe.add('cab/casa_clean',
               step,
               parameters,
               input=INPUT,
               output=OUTPUT,
               label='{}_image_ddfacet:: image data'.format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


def ddfacet(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_image_ddfacet".format(num)
    cab = '{}_ddfacet'.format(num)
    recipe.add('cab/ddfacet',
               step,
               parameters,
               input=INPUT,
               output=OUTPUT,
               shared_memory="150gb",
               label='image_ddfacet:: image data'.format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


def lwimager(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_image_lwimager".format(num)
    cab = '{}_lwimager'.format(num)
    recipe.add('cab/lwimager',
               step,
               parameters,
               input=INPUT,
               output=OUTPUT,
               label='{}_image_lwimager:: image data'.format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


# 9: Make mask to use during deconvolution

def casa_makemask(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_MakeMask".format(num)
    cab = '{}_casa_makemask'.format(num)
    recipe.add('cab/casa_makemask',
               '{}_MakeMask'.format(num),
               parameters,
               input=INPUT,
               output=OUTPUT,
               label='{}_CASA_MakeMask:: make casa mask'.format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


def cleanmask(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_CleanMask".format(num)
    cab = '{}_cleanmask'.format(num)
    recipe.add('cab/cleanmask',
               '{}_CleanMask'.format(num),
               parameters,
               input=INPUT,
               output=OUTPUT,
               label='{}_CleanMask:: make clean mask'.format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


# 8: Stack images to create cubes

def fitstools(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_make_cubes".format(num)
    cab = '{}_fitstool'.format(num)
    recipe.add('cab/fitstool',
               step,
               parameters,
               input=INPUT,
               output=OUTPUT,
               label='{}_image_cubes:: make image cube'.format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


# 9: Source Finders

def pybdsm(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_pybdsm_finder".format(num)
    cab = '{}_pybdsm'.format(num)
    recipe.add('cab/pybdsm',
               step,
               parameters,
               input=INPUT,
               output=OUTPUT,
               label='{}_pybdsf_src_finder:: pybdsm finder'.format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


def aegean(recipe, num, parameters, recipes_file=''):
    recipe_params = {}
    num = get_cab_num(num, recipes_file)
    step = "{}_aegean_finder".format(num)
    cab = '{}_aegean'.format(num)
    recipe.add('cab/aegean',
               '{}_aegean_finder'.format(num),
               parameters,
               input=INPUT,
               output=OUTPUT,
               label='{}_aegean_src_finders:: aegean finder'.format(num))
    recipe_params[cab] = parameters
    if recipes_file:
        json_dump(recipe_params, recipes_file)
    else:
        json_dump(recipe_params)


def run_all(recipe):
    recipe.run()
    recipe.jobs = []
