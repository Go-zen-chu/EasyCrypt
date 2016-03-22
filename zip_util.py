# coding:utf-8
import os, sys, zipfile, shutil
from unicodedata import normalize

class ZipUtil:
	"""Utility class to perform zip/unzip using python."""
	
	if os.name == 'nt': # for windows
		import win32api, win32con
	
	@staticmethod
	def is_hidden(path):
		if os.name == 'nt': # for windows
			attribute = win32api.GetFileAttributes(path)
			return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
		else:
			dirname, filename = os.path.split(path)
			return filename.startswith('.') #linux, mac

	@staticmethod
	def utf8mac_to_sjis(mac_path_str):
		"""
		A method for handling japanese "濁点" of mac string and convert it to shift-jis.
		If you didn't handle, it will raise an exception that you can't convert "濁点" to sjis.
		"""
		norm_path = normalize('NFC', unicode(mac_path_str,'utf8'))
		return norm_path.encode('sjis')

	@staticmethod
	def sjis_to_utf8mac(sjis_path_str):
		"""
		Vice versa method of utf8mac_to_sjis.
		"""
		uni_path = unicode(sjis_path_str, 'sjis')
		return uni_path.encode('utf8')

	@staticmethod
	def zip_dir_conv(src_dir_path, path_sanitize_func = lambda path_str: path_str, ignore_hidden_files = False):
		""" 
		This method is for converting an encode of files' name and zip them.
		path_sanitize_func is a method for sanitizing (converting encode) a path (Do nothing for default).
		"""
		if os.path.exists(src_dir_path) == False: return False
		# remove final slash that is included in src_dir_path if exists.
		if src_dir_path.endswith(os.sep): src_dir_path = src_dir_path[0:-1]
		src_parent_path, src_dirname = os.path.split(src_dir_path)
		# IMPORTANT : change directory fot not creating zip file with full path files.
		os.chdir(src_parent_path)

		with zipfile.ZipFile(src_dirname + '.zip', 'w') as zip_file:
			for parent_path, dirs, files in os.walk(src_dirname):
				conv_dir_path = path_sanitize_func(parent_path)
				if os.path.exists(conv_dir_path) == False:
					os.makedirs(conv_dir_path)
				for fname in files:
					if ignore_hidden_files and ZipUtil.is_hidden(fname): continue
					file_path = os.sep.join((parent_path, fname)) # path of original file
					if sys.flags.debug: print 'zipping : {0}'.format(file_path)
					conv_file_path = path_sanitize_func(file_path)
					if file_path == conv_file_path:
						# file name does not need to be sanitized
						zip_file.write(file_path)
					else:
						shutil.copyfile(file_path, conv_file_path) # copy file in sjis file name
						zip_file.write(conv_file_path)
						os.remove(conv_file_path) # remove tmp file for sanitation
				# path is converted if it is not same
				if conv_dir_path != parent_path:
					# remove temporary parent folder for sanitation
					shutil.rmtree(conv_dir_path)
		return True

	@staticmethod
	def zip_dir(src_dir_path, ignore_hidden_files = True):
		"""Zip specified directory's path and return True if succeeded."""
		return ZipUtil.zip_dir_conv(src_dir_path, ignore_hidden_files=ignore_hidden_files)

	@staticmethod
	def unzip_dir(zip_file_path, dst_dir_path = None):
		"""Unzip (extract) specified zip_file_path to dst_dir_path. Returns True if succeeded."""
		if os.path.exists(zip_file_path) == False: return False
		if dst_dir_path != None and os.path.exists(dst_dir_path): return False
		if dst_dir_path == None:
			dirname, filename = os.path.split(zip_file_path)
			dst_dir_path = dirname # extract in the same folder

		with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
			for member in zip_file.infolist(): # list all zipped files path
				zip_file.extract(member, dst_dir_path)
		return True

