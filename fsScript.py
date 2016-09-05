import filecmp
import argparse
import os
import sys
import json
import codecs

def script_path():
	pathname = os.path.dirname(sys.argv[0])	
	return os.path.abspath(pathname)

def modify_path(option):
	"""
		Changes either the end or start path of the file
	"""

	def path_exist(path):
		"""
			Method path_exist

			returns whether the path exist in your folder structure

		"""
		home = os.path.expanduser("~")
		
		os.chdir(home)

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
			print
			print
			print "Script path is "
			print script_path()
			print "File Path is "
			print file_path
			
			
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

			jsonFile = codecs.open('%s/config.json' % file_path, 'w+', 'utf-8')
			jsonFile.write(json.dumps(paths_configs))
			jsonFile.close()
	
	if option is 'start':
		print "What would you like the new path to be: "
		path = raw_input()
		set_start_path(path)

def compare_files():
	"""	
		compare_file

		Return the parts that are different between the two files
	"""


if __name__ == "__main__":




	file_path = script_path()

	with codecs.open('%s/config.json' % file_path, 'r', 'utf-8') as config_file:
		paths_configs = json.loads(config_file.read())

	print paths_configs

	modify_path('start')



