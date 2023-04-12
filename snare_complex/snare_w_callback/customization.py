# This file contains hooks to override default MCell4 model
# code behavior for models generated from CellBlender
import sys
import os
import numpy as np
import mcell as m


# Class to hold metadata (aka the "context") for the release event callback
class ReleaseEventCallbackContext():

  def __init__(self, name='release_event', model=None, mol_rel_info=None):
    self.name = name  # Optional name to associate with the release event
    self.model = model  # The mcell model 
    self.mol_rel_info = mol_rel_info  # metadata about the molecules to release
    self.count = 0   # counter to track number of occurences
    self.event_log = []  # log to track other metadata about this release event


# This is our callback function to handle the release of neurotransmitter
# The function is called upon the occurence of the reactions we've 
# associated the function with.
# The function is passed information about the rxn, and the metadata context associated with it.
def release_event_callback(rxn_info, context):
  context.count += 1  # increment the counter

  # Print the time and x,y,z location of the rxn event
  print('rxn at t: ', rxn_info.time)
  print('rxn at pos: ', rxn_info.pos3d)
  print('object: ',rxn_info.geometry_object.name,'  wall: ',rxn_info.wall_index)

  g = rxn_info.geometry_object  # The geometry object involved
  widx = rxn_info.wall_index    # The wall index number on the object
  tri = np.array(g.vertex_list)[g.wall_list[widx]]  # The vertices of the wall
  n = np.cross((tri[1]-tri[0]),(tri[2]-tri[0]))  # Normal vector of the wall
  n = n/np.linalg.norm(n)  # The unit normal vector

  # Now release the molecules:
  for mol_info in context.mol_rel_info:
    species = mol_info['species']  # The species to release
    number = mol_info['number']    # The number to release
    z_offset = mol_info['z_offset'] # The relative location for the release

    # Place the molecules at the location of the rxn
    #   but offset by "z_offset" in the direction of the normal vector
    loc = list(z_offset*n+np.array(rxn_info.pos3d))

    # Create a release site to release the molecules right now
    rel = m.ReleaseSite(
      name = context.name,
      complex = species,
      location = loc,
      number_to_release = number,
      release_time = rxn_info.time
    )
    context.model.release_molecules(rel)  # Release the molecules now

  # Log this event in the metadata context
  context.event_log.append((rxn_info.time, list(rxn_info.pos3d), rxn_info.reaction_rule.name))


"""
def custom_argparse_and_parameters():
    # When uncommented, this function is called to parse
    # custom commandline arguments.
    # It is executed before any of the automatically generated
    # parameter values are set so one can override the parameter
    # values here as well.
    # To override parameter values, add or overwrite an item in dictionary
    # shared.parameter_overrides, e.g. shared.parameter_overrides['SEED'] = 10
    pass
"""

"""
def custom_config(model):
    # When uncommented, this function is called to set custom
    # model configuration.
    # It is executed after basic parameter setup is done and
    # before any components are added to the model.
    pass
"""


def custom_init_and_run(model):
    # When uncommented, this function is called after all the model
    # components defined in CellBlender were added to the model.
    # It allows to add additional model components before initialization
    # is done and then to customize how simulation is ran.
    # The module parameters must be imported locally otherwise
    # changes to shared.parameter_overrides done elsewhere won't be applied.
    import parameters
    import re

    model.initialize()

    # list to hold information about molecules to be released during callback
    #   species: which species to release
    #   number:  how many to release
    #   z_offset: surface normal vector offset relative to
    #     the individual SNARE complex causing the release event
    mol_rel_info = [
        {  'species': m.Complex('glu'),
            'number': parameters.n_glu,
            'z_offset': 0.001
        }
    ]

    # create instance of context metadata for our callback
    rel_evnt_ctx = ReleaseEventCallbackContext(
        name='rel_evnt',
        model=model,
        mol_rel_info=mol_rel_info,
    )

    #when these reactions occur glutamate should be released
    rel_rxns = ['sync','async']

    for rxn_name in rel_rxns:
        rxn = model.find_reaction_rule(rxn_name)
        print(rxn.name)

        # tell our model to execute our callback function "release_event_callback" 
        #   when the rxn occurs, and pass the metadata context to the function
        model.register_reaction_callback(
            release_event_callback,
            rel_evnt_ctx,
            rxn
        )

    # Now run the model:
    model.run_iterations(parameters.ITERATIONS)
    model.end_simulation()


    output_path = './react_data/seed_%05d/' % (model.config.seed)

    try:
        os.makedirs(output_path)
    except FileExistsError:
        # directory already exists
        pass

    # Now save the glutamate release time and location
    outf = open(os.path.join(output_path,'sync_rel.dat'),'a')

    for rel_e in rel_evnt_ctx.event_log:
        outf.write('%.15g %.9g %.9g %.9g %s\n' % (rel_e[0], rel_e[1][0], rel_e[1][1], rel_e[1][2], rel_e[2]))

    outf.close()
