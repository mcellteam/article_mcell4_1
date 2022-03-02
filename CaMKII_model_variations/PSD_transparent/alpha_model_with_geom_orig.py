#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.join('..', 'shared'))

MCELL_PATH = os.environ.get('MCELL_PATH', '')
#MCELL_PATH = "/home/ahusar/mariam/Blender-2.79-CellBlender/2.79/scripts/addons/cellblender/extensions/mcell/"
os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)

import mcell as m
import numpy as np

from create_counts import load_bngl_observables_and_create_psd_and_spine_variants

# ---- define parameters for Ca pulse ----
n_pulses = 1 #get_parameter_value(n_pulses)
dt = 0.0001
#V_true = 1.51e-16 #1
V_true = 0.018822e-15
NA = 6.022e23/1e6 #1e-6

Volume_ratio = V_true/1.51e-16

tauR = 0.002 #time constant for Ca decay
tauF = 0.01

t1 = 0
t0 = 0.01
# Define the shape of the pulse (alpha function)
x=np.array(np.arange(0,0.08,dt))
alpha = 2000*(NA*V_true)*((x-t1)/tauR)*np.exp(-(x-t1)/tauF)*dt
params = m.bngl_utils.load_bngl_parameters('CorrectConc.bngl')

ITERATIONS = int(params['ITERATIONS'])

species_file = False
species_dict = dict([
    ("Ca", NA*V_true*0.1),
    ("CaM(C~0,N~0,ng,camkii)",NA*V_true*30),#NA*V_true*30,
    ("dummy", 1000),
    ("CaMKII(docked~y,r!1,l!6,c!13,Y286~0,S306~0,cam,u~1).CaMKII(docked~y,r!2,l!1,c!14,Y286~0,S306~0,cam,u~1).\
CaMKII(docked~y,r!3,l!2,c!15,Y286~0,S306~0,cam,u~1).CaMKII(docked~y,r!4,l!3,c!16,Y286~0,S306~0,cam,u~1).\
CaMKII(docked~y,r!5,l!4,c!17,Y286~0,S306~0,cam,u~1).CaMKII(docked~y,r!6,l!5,c!18,Y286~0,S306~0,cam,u~1).\
CaMKII(docked~y,r!7,l!12,c!13,Y286~0,S306~0,cam,u~0).CaMKII(docked~y,r!8,l!7,c!14,Y286~0,S306~0,cam,u~0).\
CaMKII(docked~y,r!9,l!8,c!15,Y286~0,S306~0,cam,u~0).CaMKII(docked~y,r!10,l!9,c!16,Y286~0,S306~0,cam,u~0).\
CaMKII(docked~y,r!11,l!10,c!17,Y286~0,S306~0,cam,u~0).CaMKII(docked~y,r!12,l!11,c!18,Y286~0,S306~0,cam,u~0)", NA*V_true*80/12),
    ("PP1(camkii)", NA*V_true*0.1)]
)

if len(sys.argv) >= 3 and (sys.argv[1] == '-s' or sys.argv[1] == '-seed'):
    # overwrite value SEED defined in module parameters
    SEED = int(sys.argv[2])
else:
    SEED = 2


if len(sys.argv) >= 5 and sys.argv[3] == '-species':
    # overwrite value SEED defined in module parameters
    INITIAL_SEED_SPECIES_FILE = sys.argv[4]
    species_file = True
# else:
#     INITIAL_SEED_SPECIES_FILE = 'sample.species'



if 'MCELL_TIME_STEP' in params:
    TIME_STEP = float(params['MCELL_TIME_STEP'])
else:
    TIME_STEP = 1e-6

DUMP = False#True
EXPORT_DATA_MODEL = True

#import geometry_spine_psd as geometry
#import sphs48_export_geom as geometry

import spine133_geometry as geometry
model = m.Model()


spine = geometry.d000p_sp133_cut
model.add_geometry_object(spine)
PSD = geometry.d000p_sp133_PSD
model.add_geometry_object(PSD)



# viz_output = m.VizOutput(
#    mode=m.VizMode.CELLBLENDER,
#    output_files_prefix='./viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
#    #all_species=True,
#    every_n_timesteps=ITERATIONS/100000#viz_every_n_timesteps
# )
# model.add_viz_output(viz_output)

# ---- load bngl file ----

model.load_bngl('CorrectConc.bngl', './react_data_wm/seed_' + str(SEED).zfill(5) + '/', spine)

for c in model.counts:
    c.every_n_timesteps = ITERATIONS/100000


if species_file:
    with open(INITIAL_SEED_SPECIES_FILE, 'r') as f_species:
        for line in f_species:
            # skip empty lines
            if not line:
                continue

            name_count = line.split()
            if len(name_count) != 2:
                print("Could not read .species file line:" + line)
                sys.exit(1)

            name = name_count[0]
            if name == 'time_counter' or name == 'time_counter()' in name:
                continue

            try:
                count = int(int(name_count[1]))
            except ValueError:
                print("Could not convert .species count to integer:" + name_count[1])
                sys.exit(1)

            # create the actual release site
            rel_site = m.ReleaseSite(
                name='Release of ' + name,
                complex=m.Complex(name),
                region=spine,  # box_no_compartment,
                number_to_release=count
            )
            model.add_release_site(rel_site)


else:
    for name in species_dict.keys():
        rel_site = m.ReleaseSite(
            name = 'Release_of_' + name,
            complex = m.Complex(name),
            region = spine,
            number_to_release = (int)(species_dict[name])
        )
        model.add_release_site(rel_site)

###Add the Ca signals
for rel in range(len(x)):
    if alpha[rel] > 0:
        new_rel = m.ReleaseSite(
            name = 'rel_%i' % rel,
            complex = m.Complex('Ca'),
            ## This location for spine048
            #location = [0.009,-0.045,-0.1],
            ## This location for spine133
            location = [5.868,5.62319,5.88514],
            number_to_release =alpha[rel],
            release_time = t0+x[rel]
        )
        model.add_release_site(new_rel)


# ---- configuration ----
#model.notifications.rxn_and_species_report = True

### Define PSD surface class

tp = m.SurfaceClass(
    name = 'transparent',
    type = m.SurfacePropertyType.TRANSPARENT,
    affected_complex_pattern = m.AllMolecules
)

# Molec__CaM___Orient__Ignore___Type_Transparent = m.SurfaceProperty(
#     type = m.SurfacePropertyType.TRANSPARENT,
#     affected_complex_pattern = m.Complex('CaM')
# )

# Molec__Ca___Orient__Ignore___Type_Transparent = m.SurfaceProperty(
#     type = m.SurfacePropertyType.TRANSPARENT,
#     affected_complex_pattern = m.Complex('Ca')
# )

# Molec__PP1___Orient__Ignore___Type_Transparent = m.SurfaceProperty(
#     type = m.SurfacePropertyType.TRANSPARENT,
#     affected_complex_pattern = m.Complex('PP1')
# )
## PSD is reflective to CaMKII
# Molec__CaMKII___Orient__Ignore___Type_Transparent = m.SurfaceProperty(
#     type = m.SurfacePropertyType.TRANSPARENT,
#     affected_complex_pattern = m.Complex('CaMKII')
# )


# PSD_SC = m.SurfaceClass(
#     name = 'PSD',
#     properties = [Molec__CaM___Orient__Ignore___Type_Transparent, Molec__Ca___Orient__Ignore___Type_Transparent, Molec__PP1___Orient__Ignore___Type_Transparent]
# )
model.add_surface_class(tp)
PSD.surface_class = tp


model.config.time_step = TIME_STEP
model.config.seed = SEED
model.config.total_iterations = ITERATIONS

model.config.partition_dimension = 20#1
model.config.subpartition_dimension = 0.05

load_bngl_observables_and_create_psd_and_spine_variants(
    model, 'CorrectConc.bngl', spine, PSD, ITERATIONS/100000, SEED) 


model.initialize()

if DUMP:
    model.dump_internal_state()

if EXPORT_DATA_MODEL and model.viz_outputs:
    ## Export entire data model:
    model.export_data_model()
    ## Use to export only viz parts:
    #model.export_viz_data_model()
model.run_iterations(ITERATIONS)
model.end_simulation()
