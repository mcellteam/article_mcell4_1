import os
import sys
import copy

MCELL_PATH = os.environ.get('MCELL_PATH', '')
lib_path = os.path.join(MCELL_PATH, 'lib')
sys.path.append(lib_path)


import mcell as m


# set recursively region to all nodes of type m.ExprNodeType.LEAF
def set_region_to_all_count_term_leaf_nodes(count_term_node, region):
    if not count_term_node:
        return

    if count_term_node.node_type != m.ExprNodeType.LEAF:
        set_region_to_all_count_term_leaf_nodes(count_term_node.left_node, region)
        set_region_to_all_count_term_leaf_nodes(count_term_node.right_node, region)
    else:
        count_term_node.region = region


def load_bngl_observables_and_create_psd_and_spine_variants(model, file_name, spine, psd, sampling_periodicity, seed):

    # create a helper object just to load the observables from BNGL,
    observables = m.Observables()
    observables.load_bngl_observables(file_name)

    for base_count in observables.counts:
        # count in psd
        count_psd = copy.deepcopy(base_count)
        count_psd.name = str(count_psd.name + '_psd') 
        count_psd.file_name = str('./react_data/seed_' + str(seed).zfill(5) + '/' + count_psd.name + '.dat')
        count_psd.every_n_timesteps = sampling_periodicity
        set_region_to_all_count_term_leaf_nodes(count_psd.expression, psd)
        model.add_count(count_psd)

        # count everything that is in spine but not in psd
        count_reg_spine_minus_psd = copy.deepcopy(base_count)
        count_reg_spine_minus_psd.name = str(count_reg_spine_minus_psd.name + '_reg_spine_minus_psd') 
        count_reg_spine_minus_psd.file_name = str('./react_data/seed_' + str(seed).zfill(5) + '/' + count_reg_spine_minus_psd.name + '.dat')
        count_reg_spine_minus_psd.every_n_timesteps = sampling_periodicity
        set_region_to_all_count_term_leaf_nodes(count_reg_spine_minus_psd.expression, spine - psd)
        model.add_count(count_reg_spine_minus_psd)
        

if __name__ == '__main__':
    
    # some geometry and model, just so that we are able to run this example
    Cube = m.geometry_utils.create_box('Cube', 1)
    psd = m.geometry_utils.create_box('psd', 0.5)
    
    ITERATIONS = 1000
    SEED = 1
    SAMPLING_PERIODICITY = ITERATIONS/10
    model = m.Model()
    
    load_bngl_observables_and_create_psd_and_spine_variants(
        model, '../NMDA_and_PSD/add_NMDAR.bngl',
        Cube, psd, SAMPLING_PERIODICITY, SEED
    )
    
    for count in model.counts:
        print(count.name)