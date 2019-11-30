#!/usr/bin/env python
import architecture as arc
import preprocessor as pre
import cluster_classifier as clc
import utils as ut
import plotter as plt
import projects

class dispatcher:

	def __init__(this, base_path = "/home/fivosts/trace_classification/"):
		this.base_path = base_path
		this.project_folders = ["aleth/", "SEAL/Biguint/", "SEAL/Encryptor/"]#, "FSM/Ares/", "FSM/BGP/", "FSM/Biff/", "FSM/FTP/", "FSM/Finger/", "FSM/Rlogin/", "FSM/Teamspeak/", "FSM/Telnet/", "FSM/TSP/", "FSM/Whois/"]
		return

	def dispatch_projects(this):

		for proj in projects.list_project_functions():
			proj()

		return

	def analyze_clustering_results(this, result_subfolder, search = [], exclude_keys = [], write_results = False, print_results = True, plot_project_optimals = True, save_plot = False, write_log = False):

		c = clc.cluster_classifier()
		project_results = {}
		for index, project in enumerate(this.project_folders):
			print("Project: {}\n".format(project))
			project_result = c.analyze_clustering_results(this.base_path + project + "clustering_logs/" + result_subfolder, "/clustering_results.json",
															search_only = search, exclude_keys = exclude_keys, 
															write_to_file = write_results, print_optimals = print_results)
			if project_result is not None:
				project_results[project] = (sorted(project_result, key = lambda x : float(x['precision'].replace("%", "")) + float(x['recall'].replace("%", "")), reverse = True ))[0]
				print("{} {}\n".format(project_results[project]['precision'], project_results[project]['recall']))

		# datapoints = []
		# pr_list = []
		# rec_list = []

		# for index, item in enumerate(project_results):
		# 	pr_list.append(float(project_results[item]['precision'].replace("%", "")))
		# 	rec_list.append(float(project_results[item]['recall'].replace("%", "")))

		# datapoints.append({'label': ['Precision', 'Recall'], 'x': [this.project_folders, this.project_folders], 'y': [pr_list, rec_list]})

		# if plot_project_optimals == True:
		# 	pl = plt.plotter()
		# 	pl.plot_bars(datapoints, file_path = this.base_path + "{}_prec_rec".format(result_subfolder), legend = True, show_xlabels = True, show_file = True, save_file = save_plot)

		# if write_log == True:
		# 	with open(this.base_path + "{}_prec_rec.log".format(result_subfolder), 'w') as out:
		# 		for item in project_results:
		# 			for key in item:
		# 				print(project_results)
		# 				out.write(project_results[item][key] + "\n")
		return

	def cleardirs(this, delete_folders = [], delete_files = False):

		for project in this.project_folders:
			ut.cleardirs(this.base_path + project + "clustering_logs/", delete_folders = delete_folders, delete_files = delete_files)
		return

	def help(this):

		print("Project dispatcher class")
		print("Methods and functionalities:\n\n")
		print("init: Constructs the dispatcher object\n\n\tbase_path = \"/home/fivosts/trace_classification/\" \t Sets the base path where all the projects are found\n")
		print("preprocess_projects: Call the preprocessor to reduce and encode traces\n\n\tmode = \"default\"\tSets the preprocessing mode (Choices: \"default\", \"no_reducing\")\n")
		print("cluster_projects: Perform clustering on every project of the base path\n\n")
		print("analyze_clustering_results: Explore optimal configurations by reading the clustering results for all projects\n\n \
				\tresult_subfolder\tSet the subfolder of the results that you want to compare (e.g. \"no_clustering\")\n \
				search = []\tSet a list of specific parameters to search (e.g. 'single' looks only for single linkage combos)\n \
				exclude_keys = []\tList of keywords to be excluded from the results (e.g. 'single' excludes all single linkage combos)\n \
				write = False\tWrite the optimal results to a file in the result subfolder\n \
				print = True\tPrint the optimal results to the terminal\n\n")
		print("help: Show this message\n\n")
		return

