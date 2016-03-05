# coding:utf-8
import os, sys, zipfile, shutil
from unicodedata import normalize

def utf8mac_to_sjis(mac_path_str):
	u"""
	A method for handling japanese "濁点" in mac.
	If you didn't handle, it will raise an exception that you can't convert "濁点" to sjis.
	"""
	norm_path = normalize('NFC', unicode(mac_path_str,'utf8'))
	return norm_path.encode('sjis')

def sjis_to_utf8mac(sjis_path_str):
	"""
	Vice versa method of utf8mac_to_sjis.
	"""
	uni_path = unicode(sjis_path_str, 'sjis')
	return uni_path.encode('utf8')

def check_yes_no(message):
	"""Method for requiring user to answer yes or no. True if yes, False if no."""
	yes = set(['yes','y'])
	no = set(['no','n'])
	while True:
		# raw_input returns the empty string for "enter"
		choice = raw_input(message + os.linesep).lower()
		if choice in yes:
			return True
		elif choice in no:
			return False
		else:
			print "Please respond with 'y(es)' or 'n(o)'"

def zip_dir_conv(src_dir_path, conv_func = lambda path_str: path_str):
	''' 
	This method is converting encode of file names and then zip.
	conv_func is a method for converting encode of a file name.
	'''
	src_parent_path, in_dirname = os.path.split(src_dir_path)
	os.chdir(src_parent_path)
	with zipfile.ZipFile(in_dirname + '.zip', 'w') as zip_file:
		for parent_path, dirs, files in os.walk(in_dirname):
			conv_dir_path = conv_func(parent_path)
			if os.path.exists(conv_dir_path) == False:
				os.makedirs(conv_dir_path)
			for fname in files:
				if fname[0] == '.': continue # ignore all secret file
				file_path = os.sep.join((parent_path, fname)) # path of original file
				if sys.flags.debug: print 'zipping : {0}'.format(file_path)
				conv_file_path = conv_func(file_path)
				if file_path == conv_file_path:
					zip_file.write(file_path) # file name is all alphabet
				else:
					shutil.copyfile(file_path, conv_file_path) # copy file in sjis file name
					zip_file.write(conv_file_path)
					os.remove(conv_file_path) # remove sjis format file
			# remove parent folder in sjis format
			os.removedirs(conv_dir_path)

def zip_dir(src_dir_path):
	"""Zip specified directory's path and return True if succeeded."""
	if os.path.exists(src_dir_path) == False: return False
	# remove final slash that is included in src_dir_path if exists.
	if src_dir_path.endswith(os.pathsep): src_dir_path = src_dir_path[0:-1]
	src_parent_path, in_dirname = os.path.split(src_dir_path)
	os.chdir(src_parent_path) # change directory fot not creating zip file with full path files.
	with zipfile.ZipFile(in_dirname + '.zip', 'w') as zip_file:
		for parent_path, dirs, files in os.walk(in_dirname):
			for fname in files:
				file_path = os.sep.join((parent_path, fname)) # path of original file
				if sys.flags.debug: print 'zipping : {0}'.format(file_path)
				zip_file.write(file_path)
	return True

def unzip_dir(zip_file_path, dst_dir_path):
	"""Unzip (extract) specified zip_file_path to dst_dir_path. """
	with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
		for member in zip_file.infolist(): # list all zipped files path
			zip_file.extract(member, dst_dir_path)
	return True

if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.exit('Only 1 argument(path of directory) has to be specified as argument!')
	zip_target_path = sys.argv[1]
	if os.path.exists(zip_target_path) == False:
		sys.exit('Directory {0} does not exists!'.format(zip_target_path))
	if zip_target_path.endswith(os.sep):
		zip_target_path = zip_target_path[0:-1] # remove seperator
	zip_path = zip_target_path + '.zip'
	if os.path.exists(zip_path):
		if check_yes_no('Zip file already exists. Do you want to replace? [y/n]') == False:
			print 'Bye'
			sys.exit()
	zip_dir_conv(zip_target_path, utf8mac_to_sjis) # give mac -> win conversion method


