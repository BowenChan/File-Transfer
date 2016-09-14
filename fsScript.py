from filecmp import dircmp
import argparse
import os
import sys
import json
import codecs
import readline
import glob
import re


def set_home_directory():
	"""
		Sets the working directory to /Users/{Current User}
	"""
	home = os.path.expanduser("~")
	os.chdir(home)

def script_path():
	"""
		Returns the path of the script
	"""
	pathname = os.path.dirname(sys.argv[0])	
	return os.path.abspath(pathname)

def set_completer():
	"""
		Sets up the folders autocompletion

		Code taken from http://stackoverflow.com/questions/6656819/filepath-autocompletion-using-users-input
	"""
	set_home_directory()
	readline.set_completer_delims(' \t\n;')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(complete)

def modify_path(option):
	"""
		Changes either the end or start path of the file
	"""

	def debug_path():
		"""
			DEBUGGING PURPOSES: Determines the paths of the program currently
		"""
		print
		print "Script path is "
		print script_path()
		print "File Path is "
		print file_path
		print "New Path is "
		print return_path(path)
		print

	def path_exist(path):
		"""
			Method path_exist

			returns whether the path exist in your folder structure

		"""
		set_home_directory()
		return os.path.lexists(path)

	def return_path(path):
		return os.path.abspath(path)

	def set_start_path(path):
		"""
		Method set_start_path

		modifies the global variable START_PATH to the path of the file

		"""	
		"""
		if path_exist():
			global start_path
			start_path = path
		"""

		if path_exist(path):
			paths_configs['start_path'] = return_path(path)
			
			debug_path()

			jsonFile = codecs.open('%s/config.json' % file_path, 'w+', 'utf-8')
			
			jsonFile.write(json.dumps(paths_configs))
			jsonFile.close()

	def set_end_path(path):
		"""
		Method set_end_path

		modifies the global variable END_PATH to the location the file
		will be placed
		"""
		if path_exist(path):
			paths_configs['end_path'] = return_path(path)

			debug_path()
			jsonFile = codecs.open('%s/config.json' % file_path, 'w+', 'utf-8')
			jsonFile.write(json.dumps(paths_configs))
			jsonFile.close()
	
	

	set_completer()

	if option == 'start':
		print "What would you like the new path to be: "
		path = raw_input()
		set_start_path(path)

	elif option == 'end':
		print "What would you like the new path to be: "
		path = raw_input()
		set_end_path(path)

def compare_files(dcmp):
	"""	
		compare_file

		Return the parts that are different between the two files
	"""
	def print_diff_files(dcmp):
		
		#checks for all the names that are different and prints them out ignoring hidden files
		for name in dcmp.diff_files:
			#if re.match("^\.", name) is None:
			print "diff_file %s found in %s and %s" % (name,dcmp.left,dcmp.right)
		#for sub_dcmp in dcmp.subdirs.values():
		#	print_diff_files(sub_dcmp)

	def determines_missing_files(dcmp):
		"""
			Checks and prints out any missing files from the test folder(Right)
		"""
		flag = True
		for names in dcmp.left_list:
			if names not in dcmp.right_list:
				print "Missing files %s from %s" % (names, dcmp.right)
				flag = False
		
		return flag

	def check_list(dcmp):
		"""
			DEBUGGING PURPOSE: Determine the files in both directory
		"""
		print dcmp.left_list
		print
		print dcmp.right_list


	#print check_list(dcmp)
	#print
	#print dcmp.same_files
	print
	print "------------------- Determining out-of-date files -------------------"
	print
	print_diff_files(dcmp)
	
	print "------------------- Determining missing files -----------------------"
	print
	if determines_missing_files(dcmp):
		print "There are no missing files"

def replace_or_add_files(dcmp):
	"""
		Checks and modifies the directory on the right wi thte directory on the right
	"""
	def path_exist(path):
		"""
			Method path_exist

			returns whether the path exist in your folder structure

		"""
		set_home_directory()
		return os.path.lexists(path)

	
	def add(name, flag):
		"""
			Replaces the files from LEft to right
		"""
		os.system("cp %s/%s %s/%s"  % (paths_configs['start_path'], name, paths_configs['end_path'], name))
		if flag == False:
			print "File has been added"
		elif flag == True:
			print "File has been replaced"
		print


	def permission_to_add(dcmp):
		"""
			Interate through each file to ensure that the user would like to add the files
		"""
		for names in dcmp.left_list:
			if names not in dcmp.right_list:
				print "Would you like to add %s" % names
				answer = raw_input()
				if answer == "y":
					add(names, False)

	def permission_to_replace(dcmp):
		"""
			Iterate through the folder to see which ones have been modified and if you would like to replace
		"""
		for name in dcmp.diff_files:
			print "Would you like to replace %s" % name
			answer = raw_input()
			if answer == "y":
				add(name, True)

	permission_to_add(dcmp)
	permission_to_replace(dcmp)

def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


if __name__ == "__main__":

	list_of_ignore = ['.DS_Store', '.git', 'README.md']


	file_path = script_path()

	with codecs.open('%s/config.json' % file_path, 'r', 'utf-8') as config_file:
		paths_configs = json.loads(config_file.read())

	print paths_configs
	print "What would you like to do"
	input_response = raw_input()
	while True:
		if input_response == "start" or input_response == "end":
			modify_path(input_response)
		elif input_response == "q":
			break
		else:
			print "----------------Comparing The Directories %s and %s ---------------------------" % (paths_configs['start_path'], paths_configs['end_path'])
			print
			dcmp = dircmp(paths_configs['start_path'], paths_configs['end_path'], ignore = list_of_ignore)
			compare_files(dcmp)
			replace_or_add_files(dcmp)

		print
		print "What would you like to do"
		input_response = raw_input()


