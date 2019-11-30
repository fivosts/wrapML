#!/usr/bin/env python
import preprocessor as pre
import architecture as arc
import cluster_classifier as clc

ROOT_FOLDER = "/home/fivosts/"
BASE_FOLDER = "trace_classification/"

SUPERVISED_TRAIN_LENGTH = [0.05, 0.1, 0.15, 0.2, 0.3]




def classify_biguint():

	### Object initialization
	biguint_pr = pre.preprocessor()
	biguint_arc = arc.architecture()
	biguint_cl = clc.cluster_classifier()

	### Generic parameters
	project_name = "SEAL/Biguint"
	trace_name = "trace"

	### Supervised learning parameters
	model = "ase_model.pymodel"
	superv_epochs = 80
	abl_epochs = 65
	abl_tr_length = 0.15
	
	### Clustering parameters
	linkages = ["single", "average", "complete", "ward"]
	cluster_count = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25]
	criteria = ["distinct_ave_threshold", "distinct_largest"]
	
	### Biguint Supervised
	biguint_pr.preprocess_traces(project_name = project_name, trace_name = trace_name,
								below_keyword = "",
								excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
														"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"])
	for tr_l in SUPERVISED_TRAIN_LENGTH:
		biguint_arc.initialize_architecture(model_file = model, project_name = project_name,
											trace_name = trace_name, save_training_log = True, save_model_specs = True, save_model = True,
											model_path = "full_{}".format(str(int(tr_l*100))), epochs = 80, training_length = tr_l)

	# Clustering
	biguint_pr.preprocess_traces(project_name = project_name, trace_name = trace_name,
													below_keyword = "",
													excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
																			"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"],
													preprocess_roper = True)

	for crit in criteria:
		for linkage in linkages:
			for count in cluster_count:
				# for label in bin_labels:
				print("Linkage: {} Cluster count: {}%\n--------------------------------\n".format(linkage, int(100 * count)))
				biguint_cl.initialize_architecture(project_name, trace_name = trace_name, linkage = linkage, 
														n_clusters = count, criterion = crit, plot_binary = True,
														plot_clusters = True, save_cluster_bars = True, write_cluster_log = True,
														analyze_results = True, write_analysis_to_file = True,
														print_analysis = False, make_new_folder = "full_traces", bit_feature_encoding = True)

	biguint_cl.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/SEAL/Biguint/clustering_logs/full_traces/",
										exclude_keys = ["ward", "distinct_largest"], write_to_file = True,
										print_optimals = True, plot_optimals = True, show_plots = False)

	biguint_cl.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/SEAL/Biguint/clustering_logs/full_traces/",
										write_to_file = True, print_optimals = True, 
										plot_optimals = True, show_plots = False)

	## Biguint ablation study

	biguint_pr.preprocess_traces(project_name = project_name, trace_name = trace_name,
								below_keyword = "",
								excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
														"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"], 
								encode_callee = False,
								encode_caller = False)

	biguint_arc.initialize_architecture(model_file = model, project_name = project_name,
										trace_name = trace_name, save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "{}_no_funcs_new".format(abl_tr_length), epochs = abl_epochs, training_length = abl_tr_length)


	biguint_pr.preprocess_traces(project_name = project_name, trace_name = trace_name,
								below_keyword = "",
								excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
														"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"], 
								encode_ret = False)

	biguint_arc.initialize_architecture(model_file = model, project_name = project_name,
										trace_name = trace_name, save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "{}_no_ret_new".format(abl_tr_length), epochs = abl_epochs, training_length = abl_tr_length)


	biguint_pr.preprocess_traces(project_name = project_name, trace_name = trace_name,
								below_keyword = "",
								excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
														"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"], 
								encode_args = False)

	biguint_arc.initialize_architecture(model_file = model, project_name = project_name,
										trace_name = trace_name, save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "{}_no_args_new".format(abl_tr_length), epochs = abl_epochs, training_length = abl_tr_length)

	biguint_pr.preprocess_traces(project_name = project_name, trace_name = trace_name,
								below_keyword = "",
								excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
														"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"], 
								discard_half = True)

	biguint_arc.initialize_architecture(model_file = model, project_name = project_name,
										trace_name = trace_name, save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "{}_no_half".format(abl_tr_length), epochs = abl_epochs, training_length = abl_tr_length)


	biguint_pr.preprocess_traces(project_name = project_name, trace_name = trace_name,
								below_keyword = "",
								excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
														"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"], 
								encode_callee = False,
								encode_caller = False,
								encode_args = False)

	biguint_arc.initialize_architecture(model_file = model, project_name = project_name,
										trace_name = trace_name, save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "{}_no_funcs_no_args".format(abl_tr_length), epochs = abl_epochs, training_length = abl_tr_length)


	biguint_pr.preprocess_traces(project_name = project_name, trace_name = trace_name,
								below_keyword = "",
								excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
														"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"], 
								encode_ret = False,
								encode_args = False)

	biguint_arc.initialize_architecture(model_file = model, project_name = project_name,
										trace_name = trace_name, save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "{}_no_ret_no_args".format(abl_tr_length), epochs = abl_epochs, training_length = abl_tr_length)


	biguint_pr.preprocess_traces(project_name = project_name, trace_name = trace_name,
								below_keyword = "",
								excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
														"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"], 
								encode_callee = False,
								encode_caller = False,
								encode_ret = False)

	biguint_arc.initialize_architecture(model_file = model, project_name = project_name,
										trace_name = trace_name, save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "{}_no_func_no_ret".format(abl_tr_length), epochs = abl_epochs, training_length = abl_tr_length)


	return

def classify_encryptor():

	encryptor_arc = arc.architecture()
	encryptor_pr = pre.preprocessor()
	encryptor_cl = clc.cluster_classifier()

	# Supervised

	encryptor_pr.preprocess_traces(project_name = "SEAL/Encryptor", trace_name = "trace",
									below_keyword = "_ZN4seal9Decryptor7decryptERKNS_10CiphertextERNS_9PlaintextE _ZNK4seal10Ciphertext12is_valid_forESt10shared_ptrIKNS_11SEALContextEE",
									excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
															"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"])

	for tr_l in SUPERVISED_TRAIN_LENGTH:

		encryptor_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "SEAL/Encryptor",
											trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
											model_path = "full_{}".format(str(int(100*tr_l))), epochs = 80, training_length = tr_l,
											excluded_labels = ["fail_bin_bool", "fail_bin_bool_2", "fail_bin_eq", 
																"fail_bin_op", "fail_bin_op_2", "fail_loop_length",
																"fail_swapped_args"])

	# Clustering
	encryptor_pr.preprocess_traces(project_name = "SEAL/Encryptor", trace_name = "trace",
									below_keyword = "_ZN4seal9Decryptor7decryptERKNS_10CiphertextERNS_9PlaintextE _ZNK4seal10Ciphertext12is_valid_forESt10shared_ptrIKNS_11SEALContextEE",
									excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
															"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"],
									preprocess_roper = True)	

	linkages = ["single", "average", "complete", "ward"]
	cluster_count = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25]
	# bin_labels = [True, False]
	criteria = ["distinct_ave_threshold", "distinct_largest"]
	# mk_new_folder = "bit_feature_no_reducing"

	for crit in criteria:
		for linkage in linkages:
			for count in cluster_count:
				# for label in bin_labels:
				print("Linkage: {} Cluster count: {}%\n--------------------------------\n".format(linkage, int(100 * count)))
				encryptor_cl.initialize_architecture("SEAL/Encryptor", trace_name = "trace", linkage = linkage, 
														n_clusters = count, criterion = crit, plot_binary = True, 
														plot_clusters = True, save_cluster_bars = True, write_cluster_log = True,
														analyze_results = True, write_analysis_to_file = True,
														print_analysis = False, make_new_folder = "full_traces", bit_feature_encoding = True,
														excluded_labels = ["fail_bin_bool", "fail_bin_bool_2", "fail_bin_eq", 
														"fail_bin_op", "fail_bin_op_2", "fail_loop_length",
														"fail_swapped_args"])

	encryptor_cl.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/SEAL/Encryptor/clustering_logs/full_traces/",
										exclude_keys = ["ward", "distinct_largest"], write_to_file = True,
										print_optimals = True, plot_optimals = True, show_plots = False)


	encryptor_cl.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/SEAL/Encryptor/clustering_logs/full_traces/",
										write_to_file = True, print_optimals = True, 
										plot_optimals = True, show_plots = False)

	# Ablation study

	encryptor_pr.preprocess_traces(project_name = "SEAL/Encryptor", trace_name = "trace",
								below_keyword = "_ZN4seal9Decryptor7decryptERKNS_10CiphertextERNS_9PlaintextE _ZNK4seal10Ciphertext12is_valid_forESt10shared_ptrIKNS_11SEALContextEE",
								excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
														"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"],
								discard_half = True)

	encryptor_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "SEAL/Encryptor",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "{}_no_half".format(0.1), epochs = 66, training_length = 0.1,
										excluded_labels = ["fail_bin_bool", "fail_bin_bool_2", "fail_bin_eq", 
															"fail_bin_op", "fail_bin_op_2", "fail_loop_length",
															"fail_swapped_args"])

	encryptor_pr.preprocess_traces(project_name = "SEAL/Encryptor", trace_name = "trace",
									below_keyword = "_ZN4seal9Decryptor7decryptERKNS_10CiphertextERNS_9PlaintextE _ZNK4seal10Ciphertext12is_valid_forESt10shared_ptrIKNS_11SEALContextEE",
									excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
															"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"],
									encode_callee = False,
									encode_caller = False)

	encryptor_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "SEAL/Encryptor",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "{}_no_funcs".format(0.1), epochs = 66, training_length = 0.1,
										excluded_labels = ["fail_bin_bool", "fail_bin_bool_2", "fail_bin_eq", 
															"fail_bin_op", "fail_bin_op_2", "fail_loop_length",
															"fail_swapped_args"])




	encryptor_pr.preprocess_traces(project_name = "SEAL/Encryptor", trace_name = "trace",
									below_keyword = "_ZN4seal9Decryptor7decryptERKNS_10CiphertextERNS_9PlaintextE _ZNK4seal10Ciphertext12is_valid_forESt10shared_ptrIKNS_11SEALContextEE",
									excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
															"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"],
									encode_args = False)

	encryptor_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "SEAL/Encryptor",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "{}_no_args".format(0.1), epochs = 66, training_length = 0.1,
										excluded_labels = ["fail_bin_bool", "fail_bin_bool_2", "fail_bin_eq", 
															"fail_bin_op", "fail_bin_op_2", "fail_loop_length",
															"fail_swapped_args"])



	encryptor_pr.preprocess_traces(project_name = "SEAL/Encryptor", trace_name = "trace",
									below_keyword = "_ZN4seal9Decryptor7decryptERKNS_10CiphertextERNS_9PlaintextE _ZNK4seal10Ciphertext12is_valid_forESt10shared_ptrIKNS_11SEALContextEE",
									excluded_keywords = ["_ZN4seal14IntegerEncoder14decode_biguintERKNS_9PlaintextE _ZNK4seal14IntegerEncoder13plain_modulusEv", 
															"_ZN4seal9Decryptor11bfv_decryptERKNS_10CiphertextERNS_9PlaintextENS_16MemoryPoolHandleE"],
									encode_ret = False)

	encryptor_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "SEAL/Encryptor",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "{}_no_ret".format(0.1), epochs = 66, training_length = 0.1,
										excluded_labels = ["fail_bin_bool", "fail_bin_bool_2", "fail_bin_eq", 
															"fail_bin_op", "fail_bin_op_2", "fail_loop_length",
															"fail_swapped_args"])

	return

def classify_fsm():

	fsm_pr = pre.preprocessor()
	fsm_arc = arc.architecture()
	fsm_cl = clc.cluster_classifier()

	fsm_folders = ["Ares", "BGP", "Biff", 
					"Finger", "FTP", "Rlogin", 	
					"Teamspeak", "Telnet", "TSP", "Whois"]

	# Supervised

	for fsm in fsm_folders:
		fsm_pr.preprocess_traces(project_name = "FSM/{}".format(fsm), starting_folder = "reduced_traces",
									trace_name = "r_trace", trace_reduce = False,
									 preprocess_roper = False)

		for tr_l in SUPERVISED_TRAIN_LENGTH:

			fsm_arc.initialize_architecture(model_file = "ase_model_fsm.pymodel", project_name = "FSM/{}".format(fsm),
												trace_name = "r_trace", save_training_log = True, save_model_specs = True, save_model = True,
												model_path = "full_{}".format(str(int(100*tr_l))), epochs = 40, training_length = tr_l)


	linkages = ["single", "average", "complete", "ward"]
	cluster_count = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25]
	# bin_labels = [True, False]
	criteria = ["distinct_ave_threshold", "distinct_largest"]

	for fsm in fsm_folders:
		fsm_pr.preprocess_traces(project_name = "FSM/{}".format(fsm), starting_folder = "reduced_traces",
									trace_name = "r_trace", trace_reduce = False,
									 preprocess_roper = True)
		for crit in criteria:
			for linkage in linkages:
				for count in cluster_count:
					# for label in bin_labels:
					print("Linkage: {} Cluster count: {}%\n--------------------------------\n".format(linkage, int(100 * count)))
					fsm_cl.initialize_architecture("FSM/{}".format(fsm), trace_name = "r_trace", linkage = linkage, 
															n_clusters = count, criterion = crit, plot_binary = True, 
															write_cluster_log = True, save_cluster_bars = False, show_cluster_bars = False,
															analyze_results = False, write_analysis_to_file = True,
															print_analysis = True, make_new_folder = "full_traces", bit_feature_encoding = False)

		fsm_cl.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/FSM/{}/clustering_logs/full_traces/".format(fsm),
											exclude_keys = ["ward", "distinct_largest"], write_to_file = True,
											print_optimals = True, plot_optimals = True, show_plots = False)


		fsm_cl.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/FSM/{}/clustering_logs/full_traces/".format(fsm),
											write_to_file = True, print_optimals = True, 
											plot_optimals = True, show_plots = False)

	## Fsms ablation study


	for fsm in fsm_folders:

		print("--------------------\nStarting {}\n--------------------\n".format(fsm))

		fsm_pr.preprocess_traces(project_name = "FSM/{}".format(fsm), starting_folder = "reduced_traces",
									trace_name = "r_trace", trace_reduce = False,
									 encode_caller = False,
									 encode_callee = False)


		fsm_arc.initialize_architecture(model_file = "ase_model_fsm.pymodel", project_name = "FSM/{}".format(fsm),
											trace_name = "r_trace", save_training_log = True, save_model_specs = True, save_model = True,
											model_path = "{}_no_funcs_new".format(0.1), epochs = 40, training_length = 0.1)


		fsm_pr.preprocess_traces(project_name = "FSM/{}".format(fsm), starting_folder = "reduced_traces",
									trace_name = "r_trace", trace_reduce = False,
									 encode_ret = False)



		fsm_arc.initialize_architecture(model_file = "ase_model_fsm.pymodel", project_name = "FSM/{}".format(fsm),
											trace_name = "r_trace", save_training_log = True, save_model_specs = True, save_model = True,
											model_path = "{}_no_ret_new".format(0.1), epochs = 40, training_length = 0.1)


		fsm_pr.preprocess_traces(project_name = "FSM/{}".format(fsm), starting_folder = "reduced_traces",
									trace_name = "r_trace", trace_reduce = False,
									 encode_args = False)


		fsm_arc.initialize_architecture(model_file = "ase_model_fsm.pymodel", project_name = "FSM/{}".format(fsm),
											trace_name = "r_trace", save_training_log = True, save_model_specs = True, save_model = True,
											model_path = "{}_no_args_new".format(0.1), epochs = 40, training_length = 0.1)

		fsm_pr.preprocess_traces(project_name = "FSM/{}".format(fsm), starting_folder = "reduced_traces",
									trace_name = "r_trace", trace_reduce = False,
									 discard_half = True)


		fsm_arc.initialize_architecture(model_file = "ase_model_fsm.pymodel", project_name = "FSM/{}".format(fsm),
											trace_name = "r_trace", save_training_log = True, save_model_specs = True, save_model = True,
											model_path = "{}_no_half".format(0.1), epochs = 40, training_length = 0.1)


	return

def classify_aleth():

	aleth_pr = pre.preprocessor()
	aleth_arc = arc.architecture()
	aleth_cl = clc.cluster_classifier()

	## Supervised learning

	# aleth_pr.preprocess_traces(project_name = "aleth", trace_name = "DifficultyTest",
	# 												below_keyword = "_ZN3dev3eth25calculateEthashDifficultyERKNS0_20ChainOperationParamsERKNS0_11BlockHeaderES6_",
	# 												excluded_keywords = ["difficultyByzantium_invokerEv _ZNSt6localeD1Ev"],
	# 												post_call_key = ["testDifficultyRKN5boost10filesystem4pathERN3dev3e", "calculateEthashDifficulty"],
	# 												start_size = 0, end_size = 20)

	# for tr_l in SUPERVISED_TRAIN_LENGTH:

	# 	aleth_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "aleth",
	# 										trace_name = "DifficultyTest", save_training_log = True, save_model_specs = True, save_model = True,
	# 										model_path = "{}_postorder".format(str(int(100*tr_l))), epochs = 40, training_length = tr_l,
	# 										excluded_labels = ["fail_bin_ops", "fail_inverted_minus", 
	# 															"fail_inverted_plus", "fail_swapped_args"])
	## Ethereum clustering

	# aleth_pr.preprocess_traces(project_name = "aleth", trace_name = "DifficultyTest",
	# 												below_keyword = "_ZN3dev3eth25calculateEthashDifficultyERKNS0_20ChainOperationParamsERKNS0_11BlockHeaderES6_",
	# 												excluded_keywords = ["difficultyByzantium_invokerEv _ZNSt6localeD1Ev"],
	# 												post_call_key = ["testDifficultyRKN5boost10filesystem4pathERN3dev3e", "calculateEthashDifficulty"],
	# 												preprocess_roper = True, start_size = 0, end_size = 20)


	# linkages = ["single", "average", "complete", "ward"]
	# cluster_count = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25]
	# # bin_labels = [True, False]
	# criteria = ["distinct_ave_threshold", "distinct_largest"]

	# for crit in criteria:
	# 	for linkage in linkages:
	# 		for count in cluster_count:
	# 			# for label in bin_labels:
	# 			print("Linkage: {} Cluster count: {}%\n--------------------------------\n".format(linkage, int(100 * count)))
	# 			aleth_cl.initialize_architecture("aleth", trace_name = "DifficultyTest", linkage = linkage,
	# 													n_clusters = count, criterion = crit, plot_binary = True,
	# 													plot_clusters = True, save_cluster_bars = True, write_cluster_log = True,
	# 													analyze_results = False, write_analysis_to_file = True,
	# 													excluded_labels = ["fail_bin_ops", "fail_inverted_minus", "fail_inverted_plus", "fail_swapped_args"],
	# 													print_analysis = False, make_new_folder = "postorder", bit_feature_encoding = True)


	# aleth_cl.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/aleth/clustering_logs/postorder/",
	# 									exclude_keys = ["ward", "distinct_largest"], write_to_file = True,
	# 									print_optimals = True, plot_optimals = True, show_plots = False)


	# aleth_cl.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/aleth/clustering_logs/postorder/",
	# 									write_to_file = True, print_optimals = True, 
	# 									plot_optimals = True, show_plots = False)

	## Ethereum ablation study

	aleth_pr.preprocess_traces(project_name = "aleth", trace_name = "DifficultyTest",
													below_keyword = "_ZN3dev3eth25calculateEthashDifficultyERKNS0_20ChainOperationParamsERKNS0_11BlockHeaderES6_",
													excluded_keywords = ["difficultyByzantium_invokerEv _ZNSt6localeD1Ev"],
													post_call_key = ["testDifficultyRKN5boost10filesystem4pathERN3dev3e", "calculateEthashDifficulty"],
														start_size = 0, end_size = 20,
													encode_caller = False,
													encode_callee = False)


	aleth_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "aleth",
										trace_name = "DifficultyTest", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "5_no_funcs_postorder", epochs = 40, training_length = 0.05,
										excluded_labels = ["fail_bin_ops", "fail_inverted_minus", 
															"fail_inverted_plus", "fail_swapped_args"])


	aleth_pr.preprocess_traces(project_name = "aleth", trace_name = "DifficultyTest",
													below_keyword = "_ZN3dev3eth25calculateEthashDifficultyERKNS0_20ChainOperationParamsERKNS0_11BlockHeaderES6_",
													excluded_keywords = ["difficultyByzantium_invokerEv _ZNSt6localeD1Ev"],
													post_call_key = ["testDifficultyRKN5boost10filesystem4pathERN3dev3e", "calculateEthashDifficulty"],
													start_size = 0, end_size = 20,
													encode_args = False)

	aleth_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "aleth",
										trace_name = "DifficultyTest", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "5_no_args_postorder", epochs = 40, training_length = 0.05,
										excluded_labels = ["fail_bin_ops", "fail_inverted_minus", 
															"fail_inverted_plus", "fail_swapped_args"])


	aleth_pr.preprocess_traces(project_name = "aleth", trace_name = "DifficultyTest",
													below_keyword = "_ZN3dev3eth25calculateEthashDifficultyERKNS0_20ChainOperationParamsERKNS0_11BlockHeaderES6_",
													excluded_keywords = ["difficultyByzantium_invokerEv _ZNSt6localeD1Ev"],
													post_call_key = ["testDifficultyRKN5boost10filesystem4pathERN3dev3e", "calculateEthashDifficulty"],
													start_size = 0, end_size = 20,
													encode_ret = False)

	aleth_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "aleth",
										trace_name = "DifficultyTest", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "5_no_ret_postorder", epochs = 40, training_length = 0.05,
										excluded_labels = ["fail_bin_ops", "fail_inverted_minus", 
															"fail_inverted_plus", "fail_swapped_args"])

	aleth_pr.preprocess_traces(project_name = "aleth", trace_name = "DifficultyTest",
													below_keyword = "_ZN3dev3eth25calculateEthashDifficultyERKNS0_20ChainOperationParamsERKNS0_11BlockHeaderES6_",
													excluded_keywords = ["difficultyByzantium_invokerEv _ZNSt6localeD1Ev"],
													post_call_key = ["testDifficultyRKN5boost10filesystem4pathERN3dev3e", "calculateEthashDifficulty"],
													start_size = 0, end_size = 20,
													discard_half = True)

	aleth_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "aleth",
										trace_name = "DifficultyTest", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "5_no_half_postorder", epochs = 40, training_length = 0.05,
										excluded_labels = ["fail_bin_ops", "fail_inverted_minus", 
															"fail_inverted_plus", "fail_swapped_args"])


	aleth_pr.preprocess_traces(project_name = "aleth", trace_name = "DifficultyTest",
													below_keyword = "_ZN3dev3eth25calculateEthashDifficultyERKNS0_20ChainOperationParamsERKNS0_11BlockHeaderES6_",
													excluded_keywords = ["difficultyByzantium_invokerEv _ZNSt6localeD1Ev"],
													post_call_key = ["testDifficultyRKN5boost10filesystem4pathERN3dev3e", "calculateEthashDifficulty"],
														start_size = 0, end_size = 20,
													encode_caller = False,
													encode_callee = False,
													encode_ret = False)


	aleth_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "aleth",
										trace_name = "DifficultyTest", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "5_no_funcs_no_ret_postorder", epochs = 40, training_length = 0.05,
										excluded_labels = ["fail_bin_ops", "fail_inverted_minus", 
															"fail_inverted_plus", "fail_swapped_args"])

	aleth_pr.preprocess_traces(project_name = "aleth", trace_name = "DifficultyTest",
													below_keyword = "_ZN3dev3eth25calculateEthashDifficultyERKNS0_20ChainOperationParamsERKNS0_11BlockHeaderES6_",
													excluded_keywords = ["difficultyByzantium_invokerEv _ZNSt6localeD1Ev"],
													post_call_key = ["testDifficultyRKN5boost10filesystem4pathERN3dev3e", "calculateEthashDifficulty"],
														start_size = 0, end_size = 20,
													encode_caller = False,
													encode_callee = False,
													encode_args = False)


	aleth_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "aleth",
										trace_name = "DifficultyTest", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "5_no_funcs_no_args_postorder", epochs = 40, training_length = 0.05,
										excluded_labels = ["fail_bin_ops", "fail_inverted_minus", 
															"fail_inverted_plus", "fail_swapped_args"])

	aleth_pr.preprocess_traces(project_name = "aleth", trace_name = "DifficultyTest",
													below_keyword = "_ZN3dev3eth25calculateEthashDifficultyERKNS0_20ChainOperationParamsERKNS0_11BlockHeaderES6_",
													excluded_keywords = ["difficultyByzantium_invokerEv _ZNSt6localeD1Ev"],
													post_call_key = ["testDifficultyRKN5boost10filesystem4pathERN3dev3e", "calculateEthashDifficulty"],
														start_size = 0, end_size = 20,
													encode_ret = False,
													encode_args = False)


	aleth_arc.initialize_architecture(model_file = "ase_model.pymodel", project_name = "aleth",
										trace_name = "DifficultyTest", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "5_no_ret_no_args_postorder", epochs = 40, training_length = 0.05,
										excluded_labels = ["fail_bin_ops", "fail_inverted_minus", 
															"fail_inverted_plus", "fail_swapped_args"])

	return

def classify_valueptr():

	## Supervised Learning technique

	vptr_pr = pre.preprocessor()
	vptr_ar = arc.architecture()
	vptr_clr = clc.cluster_classifier()

	vptr_pr.preprocess_traces(project_name = "value_ptr", trace_name = "trace", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 0, end_size = 80)

	for tr_l in SUPERVISED_TRAIN_LENGTH:

		vptr_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "value_ptr",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "full_{}".format(str(int(100*tr_l))), epochs = 40, training_length = tr_l)


	# # Roper clustering technique

	vptr_pr.preprocess_traces(project_name = "value_ptr", trace_name = "trace", below_keyword = "Trace Function",
								preprocess_roper = True, start_size = 0, end_size = 80)


	linkages = ["single", "average", "complete", "ward"]
	cluster_count = [0.05, 0.1, 0.15, 0.2, 0.25]
	bin_labels = [True, False]
	criteria = ["distinct_ave_threshold", "distinct_largest"]


	for crit in criteria:
		for linkage in linkages:
			for count in cluster_count:
				# for label in bin_labels:
				print("Linkage: {} Cluster count: {}%\n--------------------------------\n".format(linkage, int(100 * count)))
				vptr_clr.initialize_architecture("value_ptr", trace_name = "trace", linkage = linkage,
														n_clusters = count, criterion = crit, plot_binary = True,
														plot_clusters = True, save_cluster_bars = True, write_cluster_log = True,
														analyze_results = False, write_analysis_to_file = True,
														print_analysis = False, bit_feature_encoding = True, 
														make_new_folder = "full_traces")


	vptr_clr.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/value_ptr/clustering_logs/full_traces/",
										exclude_keys = ["ward", "distinct_largest"], write_to_file = True,
										print_optimals = True, plot_optimals = True, show_plots = False)


	vptr_clr.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/value_ptr/clustering_logs/full_traces/",
										write_to_file = True, print_optimals = True, 
										plot_optimals = True, show_plots = False)

	# Valueptr ablation study

	vptr_pr.preprocess_traces(project_name = "value_ptr", trace_name = "trace", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 0, end_size = 80,
								encode_caller = False, encode_callee = False)


	vptr_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "value_ptr",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "no_funcs_new", epochs = 40, training_length = 0.15)


	vptr_pr.preprocess_traces(project_name = "value_ptr", trace_name = "trace", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 0, end_size = 80,
								encode_ret = False)

	vptr_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "value_ptr",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "no_ret_new", epochs = 40, training_length = 0.15)



	vptr_pr.preprocess_traces(project_name = "value_ptr", trace_name = "trace", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 0, end_size = 80,
								encode_args = False)


	vptr_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "value_ptr",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "no_args_new", epochs = 40, training_length = 0.15)


	vptr_pr.preprocess_traces(project_name = "value_ptr", trace_name = "trace", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 0, end_size = 80,
								discard_half = True)


	vptr_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "value_ptr",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "no_half", epochs = 40, training_length = 0.15)

	return

def classify_sed():

	sed_pr = pre.preprocessor()
	sed_ar = arc.architecture()
	sed_clr = clc.cluster_classifier()

	# Supervised technique

	sed_pr.preprocess_traces(project_name = "sed", trace_name = "trace_", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 100, end_size = 100)

	for tr_l in SUPERVISED_TRAIN_LENGTH:

		sed_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "sed",
										trace_name = "trace_", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "full_{}".format(str(int(100*tr_l))), epochs = 40, training_length = tr_l,
										excluded_labels = ["fail_old", "pass_old"])

	# Clustering technique

	sed_pr.preprocess_traces(project_name = "sed", trace_name = "trace_", below_keyword = "Trace Function",
								preprocess_roper = True, start_size = 10, end_size = 10)


	linkages = ["single", "average", "complete", "ward"]
	cluster_count = [0.05, 0.1, 0.15, 0.2, 0.25]
	bin_labels = [True, False]
	criteria = ["distinct_ave_threshold", "distinct_largest"]

	for crit in criteria:
		for linkage in linkages:
			for count in cluster_count:
				# for label in bin_labels:
				print("Linkage: {} Cluster count: {}%\n--------------------------------\n".format(linkage, int(100 * count)))
				sed_clr.initialize_architecture("sed", trace_name = "trace_", linkage = linkage,
														n_clusters = count, criterion = crit, plot_binary = True,
														plot_clusters = True, save_cluster_bars = True, write_cluster_log = True,
														analyze_results = False, write_analysis_to_file = True,
														print_analysis = False, bit_feature_encoding = True, 
														make_new_folder = "full_traces",
														excluded_labels = ["fail_old", "pass_old"])


	sed_clr.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/sed/clustering_logs/full_traces/",
										exclude_keys = ["ward", "distinct_largest"], write_to_file = True,
										print_optimals = True, plot_optimals = True, show_plots = False)


	sed_clr.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/sed/clustering_logs/full_traces/",
										write_to_file = True, print_optimals = True, 
										plot_optimals = True, show_plots = False)


	# Ablation study

	sed_pr.preprocess_traces(project_name = "sed", trace_name = "trace_", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 100, end_size = 100,
								encode_caller = False, encode_callee = False)


	sed_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "sed",
										trace_name = "trace_", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "no_funcs_new", epochs = 40, training_length = 0.1,
										excluded_labels = ["fail_old", "pass_old"])


	sed_pr.preprocess_traces(project_name = "sed", trace_name = "trace_", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 100, end_size = 100,
								encode_ret = False)

	sed_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "sed",
										trace_name = "trace_", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "no_ret_new", epochs = 40, training_length = 0.1,
										excluded_labels = ["fail_old", "pass_old"])



	sed_pr.preprocess_traces(project_name = "sed", trace_name = "trace_", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 100, end_size = 100,
								encode_args = False)


	sed_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "sed",
										trace_name = "trace_", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "no_args_new", epochs = 40, training_length = 0.1,
										excluded_labels = ["fail_old", "pass_old"])

	sed_pr.preprocess_traces(project_name = "sed", trace_name = "trace_", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 100, end_size = 100,
								discard_half = True)


	sed_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "sed",
										trace_name = "trace_", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "no_half", epochs = 40, training_length = 0.1,
										excluded_labels = ["fail_old", "pass_old"])

	return


def classify_pytorch():

	pytorch_pr = pre.preprocessor()
	pytorch_ar = arc.architecture()
	pytorch_clr = clc.cluster_classifier()

	# Supervised technique

	pytorch_pr.preprocess_traces(project_name = "Pytorch", trace_name = "trace", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 0, end_size = 30)


	for tr_l in SUPERVISED_TRAIN_LENGTH:

		pytorch_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "Pytorch",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "full_{}".format(str(int(100*tr_l))), epochs = 50, training_length = tr_l)

	# Clustering technique

	pytorch_pr.preprocess_traces(project_name = "Pytorch", trace_name = "trace", below_keyword = "Trace Function",
								preprocess_roper = True, start_size = 0, end_size = 40)


	linkages = ["single", "average", "complete", "ward"]
	cluster_count = [0.05, 0.1, 0.15, 0.2, 0.25]
	bin_labels = [True, False]
	criteria = ["distinct_ave_threshold", "distinct_largest"]

	for crit in criteria:
		for linkage in linkages:
			for count in cluster_count:
				# for label in bin_labels:
				print("Linkage: {} Cluster count: {}%\n--------------------------------\n".format(linkage, int(100 * count)))
				pytorch_clr.initialize_architecture("Pytorch", trace_name = "trace", linkage = linkage,
														n_clusters = count, criterion = crit, plot_binary = True,
														plot_clusters = True, save_cluster_bars = True, write_cluster_log = True,
														analyze_results = False, write_analysis_to_file = True,
														print_analysis = False, bit_feature_encoding = True, 
														make_new_folder = "full_traces",
														excluded_labels = ["fail_old", "pass_old"])


	pytorch_clr.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/Pytorch/clustering_logs/full_traces/",
										exclude_keys = ["ward", "distinct_largest"], write_to_file = True,
										print_optimals = True, plot_optimals = True, show_plots = False)


	pytorch_clr.analyze_clustering_results(base_path = ROOT_FOLDER + "/trace_classification/Pytorch/clustering_logs/full_traces/",
										write_to_file = True, print_optimals = True, 
										plot_optimals = True, show_plots = False)


	# Ablation study
	# It was 0-30. Don't forget to change the training length
	pytorch_pr.preprocess_traces(project_name = "Pytorch", trace_name = "trace", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 0, end_size = 30,
								encode_caller = False, encode_callee = False)


	pytorch_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "Pytorch",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "3_no_funcs", epochs = 50, training_length = 0.03)


	pytorch_pr.preprocess_traces(project_name = "Pytorch", trace_name = "trace", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 0, end_size = 30,
								encode_ret = False)

	pytorch_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "Pytorch",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "3_no_ret", epochs = 50, training_length = 0.03)



	pytorch_pr.preprocess_traces(project_name = "Pytorch", trace_name = "trace", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 0, end_size = 30,
								encode_args = False)


	pytorch_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "Pytorch",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "3_no_args", epochs = 50, training_length = 0.03)

	pytorch_pr.preprocess_traces(project_name = "Pytorch", trace_name = "trace", below_keyword = "Trace Function",
								preprocess_roper = False, start_size = 0, end_size = 30,
								discard_half = True)


	pytorch_ar.initialize_architecture(model_file = "ase_model.pymodel", project_name = "Pytorch",
										trace_name = "trace", save_training_log = True, save_model_specs = True, save_model = True,
										model_path = "3_no_half", epochs = 50, training_length = 0.03)

	return

# FUNCTION_LIST = [classify_aleth, classify_pytorch, classify_biguint,
# 				classify_encryptor, classify_sed, classify_valueptr,
# 				classify_fsm]

FUNCTION_LIST = [classify_pytorch, classify_biguint,
				classify_encryptor, classify_sed, classify_valueptr,
				classify_fsm]


def list_project_functions():
	return FUNCTION_LIST

