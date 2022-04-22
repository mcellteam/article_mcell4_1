import os
import sys

MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

import mcell as m
# ---- customization and argument processing ----
# import the customization.py module if it exists
if os.path.exists(os.path.join(MODEL_PATH, 'customization.py')):
    import customization
else:
    customization = None


model = m.Model()
# specify that this model uses BioNetGen units (see Table 1)

model.config.use_bng_units = True
model.load_bngl('./Scene_model.bngl')
# load the information on species (diffusion constants),
# reaction rules, also creates compartment CP as a box with
# volume 1um^3 and creates release sites for molecules A and B model.load_bngl(’example.bngl’)

model.initialize()
model.run_iterations(1e6)
model.end_simulation()

# initialize simulation state # simulate 10 iterations
# final simulation step
