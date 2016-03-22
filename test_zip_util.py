# coding:utf-8
import unittest, os, shutil, sys
from zip_util import ZipUtil as zu

class ZipUtilTest(unittest.TestCase):
	"""Test class for ZipUtil"""

	TEST_TMP_DIR_NAME = 'test_tmp'
	ZIP_TEST_DIR_NAME = 'zip_test_dir'
	UNZIP_TEST_DIR_NAME = 'unzip_test_dir'
	TEST_FILE_NAME = 'test.txt'
	TEST_HIDDEN_FILE_NAME = '.test.txt'
	TEST_TMP_DIR_NAME_NO_EXIST = 'test_tmp_ghost'

	test_tmp_dir = None
	zip_test_dir = None
	zip_test_file = None
	zip_test_hid_file = None
	test_no_exist = None # path that not exists

	@classmethod
	def get_current_dir(cls):
		cur_dir = os.path.dirname(os.path.abspath(__file__))
		if sys.flags.debug: print('get_current_dir : ' + cur_dir)
		return cur_dir

	@classmethod
	def get_test_tmp_dir(cls):
		cur_dir = cls.get_current_dir()
		return os.path.join(cur_dir, cls.TEST_TMP_DIR_NAME)

	# these methods are called once when initializing class
	@classmethod
	def setUpClass(cls):
		if sys.flags.debug: print('setUpClass : called.')
		test_tmp_path = cls.get_test_tmp_dir()
		cls.test_tmp_dir = test_tmp_path
		# initialize for test
		if os.path.exists(test_tmp_path) == False:
			os.makedirs(test_tmp_path) # make dir for test
		cls.zip_test_dir = os.path.join(test_tmp_path, cls.ZIP_TEST_DIR_NAME)
		cls.zip_test_file = os.path.join(cls.zip_test_dir, cls.TEST_FILE_NAME)
		cls.zip_test_hid_file = os.path.join(cls.zip_test_dir, cls.TEST_HIDDEN_FILE_NAME)
		if os.path.exists(cls.zip_test_dir) == False:
			os.makedirs(cls.zip_test_dir)
		with open(cls.zip_test_file, 'w+') as test_file:
			test_file.write(cls.TEST_FILE_NAME)
		with open(cls.zip_test_hid_file, 'w+') as test_file:
			test_file.write(cls.TEST_HIDDEN_FILE_NAME)
		# for checking path that not exists
		cls.test_no_exist = os.path.join(test_tmp_path, cls.TEST_TMP_DIR_NAME_NO_EXIST)
		if sys.flags.debug: print('setUpClass : Finished setting up.')

	@classmethod
	def tearDownClass(cls):
		if sys.flags.debug: print('tearDownClass : called.')
		if os.path.exists(cls.test_tmp_dir):
			# careful for the path because this is dangerous process
			shutil.rmtree(cls.test_tmp_dir)
		if sys.flags.debug: print('tearDownClass : Finished cleaning up.')

	# these methods are called everytime before and after test methods is called
	def setUp(self):
		if sys.flags.debug: print('setUp method is called.')

	def tearDown(self):
		if sys.flags.debug: print('tearDown method is called.')


	# ========================== test methods ==========================

	def test_is_hidden(self):
		expected = False
		actual = zu.is_hidden(self.zip_test_file)
		self.assertEqual(expected, actual)
		expected = True
		actual = zu.is_hidden(self.zip_test_hid_file)
		self.assertEqual(expected, actual)

	def test_utf8mac_to_sjis(self):
		pass

	def test_sjis_to_utg8mac(self):
		pass

	def test_zip_dir_conv(self):
		# false test for path that not exists
		expected = False
		actual = zu.zip_dir_conv(self.test_no_exist)
		self.assertEqual(expected, actual)
		# true test
		expected = True
		actual = zu.zip_dir_conv(self.zip_test_dir)
		self.assertEqual(expected, actual)
		os.remove(self.zip_test_dir + '.zip')
		# true test that has os.sep at the end of path
		expected = True
		actual = zu.zip_dir_conv(self.zip_test_dir + os.sep)
		self.assertEqual(expected, actual)
		os.remove(self.zip_test_dir + '.zip')

	def test_zip_dir(self):
		# false test for path that not exists
		expected = False
		actual = zu.zip_dir(self.test_no_exist)
		self.assertEqual(expected, actual)

		expected = True
		actual = zu.zip_dir(self.zip_test_dir)
		self.assertEqual(expected, actual)
		os.remove(self.zip_test_dir + '.zip')

	def test_unzip_dir(self):
		# false test for path that not exists
		expected = False
		actual = zu.unzip_dir(self.test_no_exist)
		self.assertEqual(expected, actual)
		# false test for path that not exists
		expected = False
		actual = zu.unzip_dir(self.test_no_exist, self.test_no_exist)
		self.assertEqual(expected, actual)

		expected = True
		zu.zip_dir(self.zip_test_dir)
		zip_path = self.zip_test_dir + '.zip'
		actual = zu.unzip_dir(zip_path)
		self.assertEqual(expected, actual)

if __name__ == '__main__':
	unittest.main() # run unit test
