# coding:utf-8
import os, sys, argparse
import crypt_text
import zip_util

MASTER_PASS_TXT = 'master_pass.txt'

def exit_with_message(message='Error.'):
	print message
	sys.exit(1)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='This is a python directory encrypter using AES-256-CBC algorithm.')
	parser.add_argument('-i', '--input', type=str, help='Path to the raw folder or encrypted zip file.')
	parser.add_argument('-o', '--output', type=str, help='Destination folder path that encrypted zip file will be uploaded or decrypted folder is placed.')
	args = parser.parse_args()
	# if using debug mode in python
	if sys.flags.debug: print args

	if args.input == None: exit_with_message('No path is specified by -i flag.')
	if args.output == None: exit_with_message('No path is specified by -o flag.')
	crypt_text.path_exists_or_exit(args.input)
	crypt_text.path_exists_or_exit(args.output)

	if os.path.isdir(args.input):
		if args.input.endswith(os.sep):
			args.input = args.input[0:-1]
	dirpath, filename = os.path.split(args.input)
	basename, ext = os.path.splitext(filename)

	if sys.flags.debug: print dirpath, filename, basename, ext

	if ext == crypt_text.ENCRYPTED_EXT:
		# Decrypt and output to --out folder
		if os.path.isfile(args.input) == False:
			exit_with_message('Encrypted file path has to be specified for -i flag.')
		zip_file_path = os.path.join(args.output, basename)
		crypt_text.decrypt_file(args.input, zip_file_path) # zip is produced in --out folder
		zip_util.unzip_dir(zip_file_path, args.output)
		os.remove(zip_file_path)
		os.remove(args.input)
	else:
		# Encrypt and move to --out folder
		if os.path.isdir(args.input) == False:
			exit_with_message('Folder path has to be specified for -i flag.')
		master_pass_file_path = os.path.join(args.input, MASTER_PASS_TXT)
		master_pass = None
		if os.path.exists(master_pass_file_path):
			with open(master_pass_file_path, 'r') as mfile:
				master_pass = mfile.readline()
		else:
			# if there is no master password, make user to input new one
			master_pass = crypt_text.confirm_pswd()
			with open(master_pass_file_path, 'w') as mfile:
				mfile.write(master_pass)
		zip_util.zip_dir(args.input) # filename is dirname in this case
		zip_file_path = args.input + '.zip'
		crypt_text.encrypt_file(zip_file_path, master_pass,
			os.path.join(args.output, filename + '.zip' + crypt_text.ENCRYPTED_EXT))
		os.remove(zip_file_path)

