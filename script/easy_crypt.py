# coding:utf-8
from __future__ import print_function # using Python3 print for lambda, forward compatibility
import os, sys, getpass, random, string, json
import subprocess as sps
import zip_util as zu

class EasyCrypt:
	"""
	Python script for en/decrypting file using openssl command.
	Aim of this script is to make en/decryption of files and dirs easier, nothing more, nothing less.

	Since this script uses openssl command be aware if you are Windows user
	(Mac and Linux distributions have openssl commands by default).
	If you want to use this script on Windows, please install OpenSSL via 
	https://www.openssl.org/source/
	or 
	https://wiki.openssl.org/index.php/Binaries
	and make sure the command properly works from command prompt.

	If you use python debug flag (-d), some of the outputs are printed.
	"""
	# This script uses AES 256bit by default and encrypted files are exported in Base64 format.
	OPENSSL_CMD = 'openssl aes-256-cbc {0} -base64 -in "{1}" -k "{2}"'
	OPENSSL_CMD_WITH_OUTPUT = OPENSSL_CMD + ' -out "{3}"'
	OPENSSL_CHECK_CMD = 'openssl -h'
	# Extension for encrypted files. Change if any.
	ENCRYPTED_EXT = '.enc'
	# password file that created for encrypting directory
	MASTER_PASS_TXT = 'master_pass.txt'
	HEADER_VERSION = 0.1

	@staticmethod
	def create_header(master_pswd, version_dbl = HEADER_VERSION):
		"""Create header which has json format as info storer of encryption."""
		header_json_dict = {'master_password' : master_pswd, 'version' : version_dbl }
		return json.dumps(header_json_dict)

	@staticmethod
	def read_header(header_str):
		"""Load json str and returns in python object. If it is not a valid json string, returns None."""
		try:
			json_dict = json.loads(header_str)
		except ValueError, e:
			return None
		return json_dict

	@staticmethod
	def read_header_of_file(raw_file_path):
		"""Read header of raw text file and returns in python object. If there is a problem, returns None."""
		if os.path.exists(raw_file_path) == False: return None
		with open(raw_file_path, 'r') as raw_file:
			header_str = raw_file.readline()
		return EasyCrypt.read_header(header_str)

	@staticmethod
	def read_master_pswd(raw_file_path):
		"""Read header of text file and returns master password. If there is a problem, returns None."""
		header_dict = EasyCrypt.read_header_of_file(raw_file_path)
		if header_dict == None or 'master_password' not in header_dict:
			return None
		else:
			return header_dict['master_password']

	@staticmethod
	def rm_ext_from_path(abs_path):
		"""Remove extension from absolute path and return absolute path without extension."""
		dirname, filename = os.path.split(abs_path)
		basename, ext = os.path.splitext(filename)
		return os.path.join(dirname, basename)

	@staticmethod
	def exec_command(cmd_str, failed_act=None):
		"""Execute shell command, returns True if succeeded otherwise returns False."""
		try:
			proc = sps.Popen(cmd_str, shell=True, stderr=sps.PIPE, stdout=sps.PIPE) # these are for getting output strings
			result_code = proc.wait()
			if result_code != 0:
				if failed_act != None: failed_act()
				if sys.flags.debug: print('[error]: ' + ''.join(proc.stderr))
				return False
			else:
				return True
		except sps.CalledProcessError:
			print('Failed Unexpectedly. Try again.')

	@staticmethod
	def exec_command_get_result(cmd_str, failed_act=None):
		"""Execute shell command, returns stdout of result if succeeded otherwise return None or raise exception."""
		try:
			proc = sps.Popen(cmd_str, shell=True, stderr=sps.PIPE, stdout=sps.PIPE) # these are for getting output strings
			result_code = proc.wait()
			if result_code != 0:
				if failed_act != None: failed_act()
				if sys.flags.debug: print('[error]: ' + ''.join(proc.stderr))
				return None
			else:
				std = ''.join(proc.stdout)
				if sys.flags.debug: print('[success]: ' + decrypted_txt)
				return decrypted_txt # returns decrypted text
		except sps.CalledProcessError:
			print('Failed Unexpectedly. Try again.')

	@staticmethod
	def confirm_pswd(message='Please type new password', confirmed_act=None, rejected_act=None):
		"""
		Function for confirming password input by a user.
		Arguments .*_act are for passing methods that have no return value which are used for 
		like showing messages or popups.
		"""
		pass_same_flg = False
		confirmed_pass = None
		while pass_same_flg == False:
			first_pass 	= getpass.getpass(message + '         : ')
			second_pass = getpass.getpass(message + '[Confirm]: ')
			if first_pass == second_pass:
				pass_same_flg = True
				confirmed_pass = second_pass
				if confirmed_act != None: confirmed_act()
			else:
				if rejected_act != None: rejected_act()
		return confirmed_pass

	@staticmethod
	def confirm_pswd_print(message='Please type new password'):
		"""	Function that passing printing message method to confirm_pswd function."""
		confirm_pswd(message, lambda: print('Confirmed.'), lambda: print('Password did not match. Try again.'))

	@staticmethod
	def encrypt_file(raw_file_path, master_pswd, encrypted_file_path=None):
		"""
		Encrypt file using openssl command.
		Returns True if success, otherwise raises exception.
		If encrypted_file_path is None, new file is generated in same directory.
		"""
		if os.path.exists(raw_file_path) == False: return False
		if encrypted_file_path == None: encrypted_file_path = raw_file_path + ENCRYPTED_EXT
		cmd = OPENSSL_CMD_WITH_OUTPUT.format('-e', raw_file_path, master_pswd, encrypted_file_path)
		exec_command(cmd) # if error happens, this func will raise exception
		return True

	@staticmethod
	def get_master_pswd_from_txt(master_pass_file_path):
		"""
		Check whether there is master pass file, and get master password if exists, create new if not.
		"""
		master_pswd = None
		if os.path.exists(master_pass_file_path):

			with open(master_pass_file_path, 'r') as mfile:
				header_str = mfile.readline() # read json formatted header
				header_json_dict = read_header(header_str)
				if 'master_password' not in header_json_dict:
					print('master_password is not exists in {0}. \
						If you want to create new password, delete {0} file and encrypt again.'
						.format(MASTER_PASS_TXT))
					return None
				master_pswd = ['master_password'] # get master pass
		else: 
			# if there is no master password, make user to input new one
			master_pswd = confirm_pswd_print()
			with open(master_pass_file_path, 'w') as mfile:
				mfile.write(create_header(master_pswd))
		return master_pswd

	@staticmethod
	def encrypt_dir(raw_dir_path, encrypted_dir_path=None):
		"""
		Encrypt directory by zip and encrypt using openssl command.
		It returns True if succeeded, otherwise returns False.
		"""
		if os.path.exists(raw_dir_path) == False: return False
		# has to be a directory
		if os.path.isdir(raw_dir_path) == False: return False
		master_pass_file_path = os.path.join(raw_dir_path, MASTER_PASS_TXT)
		# check whether there is master pass file in working dir path and get master password.
		master_pswd = get_master_pswd_from_txt(master_pass_file_path)
		if master_pswd == None: return False
		zu.zip_dir(raw_dir_path)
		# remove final slash that is included in in_dir_path if exists.
		if raw_dir_path.endswith(os.sep): raw_dir_path = raw_dir_path[0:-1]
		zip_file_path = raw_dir_path + '.zip'
		encrypt_file(zip_file_path, master_pswd, encrypted_dir_path)
		return True

	@staticmethod
	def get_decrypted_txt(encrypted_file_path, failed_act=None):
		"""
		Decrypt file using openssl command.
		Returns decrypted text if success, else returns None.
		"""
		if os.path.exists(encrypted_file_path) == False: return None
		if encrypted_file_path.endswith(ENCRYPTED_EXT) == False: return None # unsupported extension
		# make user to input password until it gets correct password.
		while True:
			master_pswd = getpass.getpass('Input master password: ')
			cmd = OPENSSL_CMD.format('-d', encrypted_file_path, master_pswd)
			decrypted_txt = exec_command_get_result(cmd, failed_act)
			if decrypted_txt != None: return decrypted_txt

	@staticmethod
	def decrypt_txt_file(encrypted_file_path, raw_file_path=None, handle_decrpyted_txt_func=None, remove_enc_file=False):
		"""
		WARNING:
		This function should only be used for encrypted text file.
		It will return nothing if you used for other kinds of files.
		If you want to decrypt other kinds of files, use "decrypt_file" function.

		Decrypt text file using openssl command.
		You can handle decrypted text file by putting handle_decrpyted_txt_func in the args.
		Decrypted file is exported in same dir of encrypted_file_path, if raw_file_path is not specified.
		Returns True if success and False if not.
		"""
		if raw_file_path == None: raw_file_path = rm_ext_from_path(encrypted_file_path)
		# Existence of path is checked here.
		decrypted_txt = get_decrypted_txt(encrypted_file_path, lambda: print('Failed to decrypt. May be miss typing?'))
		# Failed to decrypt
		if decrypted_txt == None: return False
		if sys.flags.debug: print('Decryption Success!')
		# method for handling raw text files
		if handle_decrpyted_txt_func != None: decrypted_txt = handle_decrpyted_txt_func(decrypted_txt)
		with open(raw_file_path, 'w+') as raw_file:
			raw_file.write(decrypted_txt)
		if remove_enc_file: os.remove(encrypted_file_path)
		return True

	@staticmethod
	def decrypt_file(encrypted_file_path, raw_file_path=None, failed_act=None, remove_enc_file=False):
		"""
		Decrypt file using openssl command. It can be used for any types of file format.
		Decrypted file is exported in same dir of encrypted_file_path, if raw_file_path is not specified.
		Returns True if success and False if not.
		"""
		if os.path.exists(encrypted_file_path) == False: return False
		if encrypted_file_path.endswith(ENCRYPTED_EXT) == False: return False # unsupported extension
		if raw_file_path == None: raw_file_path = rm_ext_from_path(encrypted_file_path)
		while True:
			master_pswd = getpass.getpass('Input master password: ')
			cmd = OPENSSL_CMD_WITH_OUTPUT.format('-d', encrypted_file_path, master_pswd, raw_file_path)
			if exec_command(cmd, failed_act):
				if remove_enc_file: os.remove(encrypted_file_path)
				return True

	@staticmethod
	def decrypt_dir(encrypted_dir_path, dst_dir_path=None, remove_enc_file=False, remove_zip=False):
		"""
		Decrypt .zip.enc file using openssl command.
		Returns True if succeeded, else False.
		"""
		if os.path.isfile(encrypted_dir_path) == False: return False
		tmp_zip_file_path = rm_ext_from_path(encrypted_dir_path)
		if decrypt_file(encrypted_dir_path, tmp_zip_file_path) == False: return False
		if dst_dir_path == None: dst_dir_path = rm_ext_from_path(tmp_zip_file_path)
		# whether to succeed in unzipping to a directory
		if zu.unzip_dir(tmp_zip_file_path, dst_dir_path):
			if remove_enc_file: os.remove(encrypted_dir_path)
			if remove_zip: os.remove(tmp_zip_file_path)
			return True
		else:
			return False

	@staticmethod
	def gen_rnd_pswd(length=8, include_simbols=True, rnd_seed=None):
		"""Generate random password with specified length. Used for salting passwords."""
		chars = string.ascii_letters + string.digits
		if include_simbols: chars += '!@#$%^&*{}[]'
		# random.SystemRandom() uses os.urandom() for seed which is more reliable than normal random()
		# rnd = random.SystemRandom()
		# random_pass = ''.join(rnd.choice(chars) for i in range(length))
		
		# however, SystemRandom is not suitable for testing
		random.seed(rnd_seed) # uses time for seed if None is specified
		random_pass = ''.join(random.choice(chars) for i in range(length))
		if sys.flags.debug: print(random_pass)
		return random_pass

	@staticmethod
	def path_exists_or_exit(file_path):
		"""Function for checking existence of path or otherwise exists with an error."""
		if os.path.exists(file_path) == False:
			print('File does not exists. Check the specified path.')
			sys.exit(1)
		return True

	@staticmethod
	def check_openssl_availability():
		"""Check openssl command availability in user's envrionments."""
		return EasyCrypt.exec_command(EasyCrypt.OPENSSL_CHECK_CMD)

