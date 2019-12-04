#!/usr/bin/env python
import dispatcher as dsp
import architecture as arc
import utils
# d = dsp.dispatcher()
# d.dispatch_projects()

aleth_arc = arc.architecture()

for p in [0.3, 0.4, 0.5, 0.6, 0.7]:

	split_list = utils.generate_splitted_exclusive(40, p)
	split_set = {'pass': split_list[0], 'fail_wrong_numbers': split_list[1]}

	print(split_set)

	SUPERVISED_TRAIN_LENGTH = [0.05, 0.1, 0.15, 0.2, 0.3]

	for tr_l in SUPERVISED_TRAIN_LENGTH:

		aleth_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "aleth", split_trace_sets = split_set,
											trace_name = "DifficultyTest", save_training_log = True, save_model_specs = True, save_model = True,
											model_path = "000000/splittedMut_p{}_trl{}".format(str(int(100*p)), str(int(100*tr_l))), epochs = 40, training_length = tr_l,
											excluded_labels = ["fail_bin_ops", "fail_inverted_minus", 
																"fail_inverted_plus", "fail_swapped_args"])