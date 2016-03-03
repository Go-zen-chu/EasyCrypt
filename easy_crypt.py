# coding:utf-8
"""
	Python code for en/decrypting file using openssl command.
	Aim of this script is to make en/de cryption of files and dirs easier, nothing more, nothing less.

	Since this script uses openssl command be aware if you are Windows user
	(Mac and Linux distributions have openssl commands by default).
	If you want to use this script on Windows, please install OpenSSL via 
	https://www.openssl.org/source/
	or 
	https://wiki.openssl.org/index.php/Binaries
	and make sure the command properly works from command prompt.

	If you use python debug flag (-d), some of the outputs are printed.
"""
from __future__ import print_function # using Python3 print for lambda, forward compatibility
import os, sys, getpass, argparse, random, string
import subprocess as sps

class EasyCrypt:
	# This script uses AES 256bit by default and encrypted files are exported in Base64 format.
	OPENSSL_CMD = 'openssl aes-256-cbc {0} -base64 -in "{1}" -k "{2}"'
	OPENSSL_CMD_WITH_OUTPUT = OPENSSL_CMD + ' -out "{3}"'
	# Extension for encrypted files. Change if any.
	ENCRYPTED_EXT = '.enc'

	@staticmethod
	def rm_ext_from_path(abs_path):
		dirname, filename = os.path.split(abs_path)
		basename, ext = os.path.splitext(filename)
		return os.path.join(dirname, basename)

	@staticmethod
	def exec_command(cmd_str):
	"""
	Execute shell command, returns True if succeeded otherwise raise exception.
	"""
		try:
			sps.check_output(cmd_str, shell=True)
		except sps.CalledProcessError:
			raise

	@staticmethod
	def exec_command_get_result(cmd_str, attempt_failed_act=None):
	"""
	Execute shell command, returns stdout of result if succeeded otherwise return None or raise exception.
	"""
		try:
			proc = sps.Popen(cmd_str, shell=True, stderr=sps.PIPE, stdout=sps.PIPE) # these are for getting output strings
			result_code = proc.wait()
			if result_code != 0:
				if attempt_failed_act != None: attempt_failed_act()
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
		if encrypted_file_path == None: encrypted_file_path = raw_file_path + ENCRYPTED_EXT
		cmd = OPENSSL_CMD_WITH_OUTPUT.format("-e", raw_file_path, master_pswd, encrypted_file_path)
		exec_command(cmd) # if error happens, this func will raise exception
		return True

	@staticmethod
	def get_decrypted_txt(encrypted_file_path, attempt_failed_act=None):
		"""
		Decrypt file using openssl command.
		Returns decrypted text if success, else returns None.
		"""
		if os.path.exists(encrypted_file_path) == False: return None
		if encrypted_file_path.endswith(ENCRYPTED_EXT) == False: return None # unsupported extension
		# make user to input password until it gets correct password.
		while True:
			master_pswd = getpass.getpass('Input master password: ')
			cmd = OPENSSL_CMD.format("-d", encrypted_file_path, master_pswd)
			decrypted_txt = exec_command_get_result(cmd, attempt_failed_act)
			if decrypted_txt != None: return decrypted_txt

	@staticmethod
	def decrypt_txt_file(encrypted_file_path, out_file_path=None, handle_decrpyted_txt_func=None):
		"""
		WARNING: This function should only be used for encrypted text file. It will return nothing if you used for other kinds of files.
		Decrypt text file using openssl command.
		Decrypted file is exported in same dir of encrypted_file_path, if out_file_path is not specified.
		Returns True if success and False if not.
		"""
		if os.path.exists(encrypted_file_path) == False: return False
		if out_file_path == None: out_file_path = rm_ext_from_path(encrypted_file_path)
		decrypted_txt = get_decrypted_txt(encrypted_file_path, lambda: print('Failed to decrypt. May be miss typing?'))
		# Failed to decrypt
		if decrypted_txt == None: return False
		if sys.flags.debug: print('Decryption Success!')
		if handle_decrpyted_txt_func != None: decrypted_txt = handle_decrpyted_txt_func(decrypted_txt)
		with open(out_file_path, 'w+') as raw_file:
			raw_file.write(decrypted_txt)
		return True

	@staticmethod
	def decrypt_file(encrypted_file_path, out_file_path=None, attempt_failed_act=None):
		"""
		Decrypt file using openssl command. It can be used for any types of file format.
		Decrypted file is exported in same dir of encrypted_file_path, if out_file_path is not specified.
		Returns True if success and False if not.
		"""
		if os.path.exists(encrypted_file_path) == False: return False
		if out_file_path == None: out_file_path = rm_ext_from_path(encrypted_file_path)
		while True:
			master_pswd = getpass.getpass('Input master password: ')
			cmd = OPENSSL_CMD_WITH_OUTPUT.format("-d", encrypted_file_path, master_pswd, out_file_path)
			if exec_command(cmd) == True: return True

	@staticmethod
	def gen_rnd_pswd(length=8, include_simbols=True):
		"""Generate random password with specified length. Used for salting passwords."""
		chars = string.ascii_letters + string.digits
		if include_simbols: chars + '!@#$%^&*{}[]'
		# random.SystemRandom() uses os.urandom() for seed which is more reliable than normal random()
		rnd = random.SystemRandom()
		random_pass = ''.join(rnd.choice(chars) for i in range(length))
		if sys.flags.debug: print(random_pass)
		return random_pass

	@staticmethod
	def path_exists_or_exit(file_path):
		"""Function for checking existence of path or otherwise exists with an error."""
		if os.path.exists(file_path) == False:
			print('File does not exists. Check the specified path.')
			sys.exit(1)
		return True

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='This is a python encrypter using AES-256-CBC algorithm of openssl.')
	parser.add_argument('-d', type=str, help='Decrypt encripted file')
	parser.add_argument('-e', type=str, help='Encrypt text to pypw file')
	parser.add_argument('-g', action='store_true', help='Generate random password')
	args = parser.parse_args()
	# if using debug mode in python
	if sys.flags.debug: print(args)
	pass_header = '# This line is auto-generated by crypt_text.py. Master Password: '
	
	if args.g:
		print(gen_rnd_pswd())
	elif args.d != None:
		path_exists_or_exit(args.d)
		decrypt_txt_file(args.d)
	elif args.e != None:
		path_exists_or_exit(args.e)
		with open(args.e, 'r') as raw_file:
			raw_header = raw_file.readline()
		if raw_header.startswith(pass_header):
			# already master password is confirmed
			# erace pass_header and whitespace then strip the password
			master_pswd = raw_header.replace(pass_header, '').replace(' ', '').rstrip()
		else:
			# if there is no master password, make user to input new one
			master_pswd = confirm_pswd_print()
			with open(args.e, 'r') as raw_file:
				raw_file_data = raw_file.readlines()
			# add master password to the top of file 
			raw_file_data.insert(0, pass_header + master_pswd + os.linesep)
			with open(args.e, 'w') as raw_file:
				raw_file.write(str.join('', raw_file_data))
		encrypt_file(args.e, master_pswd)
	else:
		print('No arguments! Input -h or --help flag for help.')

