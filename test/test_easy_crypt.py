# coding:utf-8
import os, sys, argparse, unittest, shutil
# to import script from other folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../script')
from easy_crypt import EasyCrypt as ec

class EasyCryptTest(unittest.TestCase):
	"""docstring for EasyCryptTest"""

	# main dir for testing EasyCrypt
	TEST_MAIN_DIR_NAME = 'test_tmp_easy_crypt'
	TEST_FILE_NAME = 'test.txt'
	TEST_EMPTY_HEADER_FILE_NAME = 'test_empty_header.txt'
	TEST_NO_EXIST_NAME = 'test_tmp_ghost'

	test_main_dir_path = None
	test_file_path = None
	test_empty_header_file_path = None
	test_no_exist_path = None # path that not exists

	TEST_MASTER_PSWD = 'mst_pswd'
	TEST_HEADER_JSON = {"master_password": TEST_MASTER_PSWD, "version": 0.1}
	TEST_HEADER_JSON_STR = '{"master_password": "' + TEST_MASTER_PSWD + '", "version": 0.1}'
	TEST_HEADER_JSON_ERROR_STR = '{ error_json }'
	TEST_HEADER_JSON_EMPTY_STR = '{ }'


	@classmethod
	def get_current_dir(cls):
		cur_dir = os.path.dirname(os.path.abspath(__file__))
		if sys.flags.debug: print('get_current_dir : ' + cur_dir)
		return cur_dir

	@classmethod
	def get_test_main_dir_path(cls):
		cur_dir = cls.get_current_dir()
		return os.path.join(cur_dir, cls.TEST_MAIN_DIR_NAME)

	# these methods are called once when initializing class
	@classmethod
	def setUpClass(cls):
		if sys.flags.debug: print('setUpClass : called.')
		if ec.check_openssl_availability():
			print('openssl command is availabile')
		else:
			print('openssl command is not availabile. Check your path for openssl or install openssl to your system.')
			sys.exit(1)
		# main dir path for testing EasyCrypt
		test_tmp_path = cls.get_test_main_dir_path()
		cls.test_main_dir_path = test_tmp_path
		cls.test_file_path = os.path.join(test_tmp_path, cls.TEST_FILE_NAME)
		cls.test_empty_header_file_path = os.path.join(test_tmp_path, cls.TEST_EMPTY_HEADER_FILE_NAME)

		# initialize for test
		if os.path.exists(test_tmp_path) == False:
			os.makedirs(test_tmp_path) # make dir for test
		with open(cls.test_file_path, 'w+') as test_file:
			test_file.write(cls.TEST_HEADER_JSON_STR + os.linesep)
			test_file.write(cls.TEST_FILE_NAME)
		with open(cls.test_empty_header_file_path, 'w+') as test_file:
			test_file.write(cls.TEST_HEADER_JSON_EMPTY_STR + os.linesep)
			test_file.write(cls.TEST_EMPTY_HEADER_FILE_NAME)

		# for checking path that not exists
		cls.test_no_exist_path = os.path.join(test_tmp_path, cls.TEST_NO_EXIST_NAME)
		if sys.flags.debug: print('setUpClass : Finished setting up.')

	@classmethod
	def tearDownClass(cls):
		if sys.flags.debug: print('tearDownClass : called.')
		#if os.path.exists(cls.test_main_dir_path):
			# careful for the path because this is dangerous process
			#shutil.rmtree(cls.test_main_dir_path)
		if sys.flags.debug: print('tearDownClass : Finished cleaning up.')

	# these methods are called everytime before and after test methods is called
	def setUp(self):
		if sys.flags.debug: print('setUp : called.')

	def tearDown(self):
		if sys.flags.debug: print('tearDown : called.')

	# ========================== test methods ==========================

	# def test_create_header(self):
	# 	expected = self.TEST_HEADER_JSON_STR
	# 	actual = ec.create_header(self.TEST_MASTER_PSWD)
	# 	if sys.flags.debug: print(actual)	
	# 	self.assertEqual(expected, actual)

	# def test_read_header(self):
	# 	expected = None
	# 	actual = ec.read_header(self.TEST_HEADER_JSON_ERROR_STR)
	# 	self.assertEqual(expected, actual)

	# 	expected = self.TEST_HEADER_JSON
	# 	actual = ec.read_header(self.TEST_HEADER_JSON_STR)
	# 	self.assertEqual(expected, actual)

	# def test_read_header_of_file(self):
	# 	# make sure to make file before launching this method
	# 	expected = None
	# 	actual = ec.read_header_of_file(self.TEST_NO_EXIST_NAME)
	# 	self.assertEqual(expected, actual)

	# 	expected = self.TEST_HEADER_JSON
	# 	actual = ec.read_header_of_file(self.test_file_path)
	# 	self.assertEqual(expected, actual)

	# def test_read_master_pswd(self):
	# 	expected = None
	# 	actual = ec.read_master_pswd(self.test_no_exist_path)
	# 	self.assertEqual(expected, actual)

	# 	expected = None
	# 	actual = ec.read_master_pswd(self.test_empty_header_file_path)
	# 	self.assertEqual(expected, actual)

	# 	expected = self.TEST_MASTER_PSWD
	# 	actual = ec.read_master_pswd(self.test_file_path)
	# 	self.assertEqual(expected, actual)

	# def test_rm_ext_from_path(self):

	# def test_exec_command(self):

	# def test_exec_command_get_result(self):

	# def test_confirm_pswd(self):

	# def test_confirm_pswd_print(self):

	# def test_encrypt_file(self):

	# def test_get_master_pswd_from_txt(self):

	# def test_encrypt_dir(self):

	# def test_get_decrypted_txt(self):

	# def test_decrypt_txt_file(self):

	# def test_decrypt_file(self):

	# def test_decrypt_dir(self):

	# def test_gen_rnd_pswd(self):
	# 	expected = 'i0VpEBOW'
	# 	actual = ec.gen_rnd_pswd(8, include_simbols=False, rnd_seed=1)
	# 	self.assertEqual(expected, actual)

	# 	expected = 'j!4sKHW6'
	# 	actual = ec.gen_rnd_pswd(8, include_simbols=True, rnd_seed=1)
	# 	self.assertEqual(expected, actual)

	# def test_path_exists_or_exit(self):
	# 	# false check
	# 	with self.assertRaises(SystemExit):
	# 		ec.path_exists_or_exit(self.test_tmp_ghost)

	# 	expected = True
	# 	actual = ec.path_exists_or_exit(self.test_main_dir_path)
	# 	self.assertEqual(expected, actual)

	# def test_check_openssl_availability(self):

if __name__ == '__main__':
	unittest.main() # run unit test
