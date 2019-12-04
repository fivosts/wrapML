#!/usr/bin/env python
import dispatcher as dsp
import architecture as arc
import utils
# d = dsp.dispatcher()
# d.dispatch_projects()

aleth_arc = arc.architecture()
remake = True

for p in [0.3, 0.4, 0.5, 0.6, 0.7]:

	split_list = utils.generate_splitted_exclusive(2254, p)
	split_set = {'pass': split_list[0], 'fail_wrong_numbers': split_list[1]}
	remake = True

	print("DBG: [" + ', '.join(split_set) + ']')
	
	for tr_l in [0.05, 0.1, 0.15, 0.2, 0.3]:

		print("DBG: " + str(tr_l))
		aleth_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "aleth", split_trace_sets = split_set, remake_dataset = remake,
											trace_name = "DifficultyTest", save_training_log = True, save_model_specs = True, save_model = False,
											model_path = "only_mutated/passperc{}_trl{}".format(str(int(100*p)), str(int(100*tr_l))), epochs = 40, training_length = tr_l,
											excluded_labels = ["fail_bin_ops", "fail_inverted_minus", 
																"fail_inverted_plus", "fail_swapped_args"])
		remake = False