#!/usr/bin/env python
import dispatcher as dsp
import architecture as arc
import utils
# d = dsp.dispatcher()
# d.dispatch_projects()

aleth_arc = arc.architecture()

split_list = utils.generate_splitted_exclusive(60, 0.5)
split_set = {'pass': split_list[0], 'fail_wrong_numbers': split_list[1]}

print(split_set)

aleth_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "aleth", mode = "inference", split_trace_sets = split_set,
									trace_name = "DifficultyTest", model_path = "{}_postorder/pymodel/epoch_16".format(str(int(100*0.3))), 
									excluded_labels = ["fail_bin_ops", "fail_inverted_minus", 
														"fail_inverted_plus", "fail_swapped_args"])