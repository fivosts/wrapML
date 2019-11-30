#!/usr/bin/env python
import dispatcher as dsp
import architecture as arc
# d = dsp.dispatcher()
# d.dispatch_projects()

aleth_arc = arc.architecture()



aleth_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "aleth", mode = "inference",
									trace_name = "DifficultyTest", model_path = "{}_postorder/pymodel/epoch_16".format(str(int(100*0.3))), 
									excluded_labels = ["fail_bin_ops", "fail_inverted_minus", 
														"fail_inverted_plus", "fail_swapped_args"])