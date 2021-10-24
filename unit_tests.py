import unittest as unit
import pdf_work as p_w
from PyPDF2 import PdfFileReader
import os


class TestPdfWorkMethods(unit.TestCase):
    test_files_path = "FilesForTesting"

    def test_file_uniting(self):
        first_file_name = 'Test1.pdf'
        second_file_name = 'Test2.pdf'

        os.path.exists(first_file_name)
        os.path.exists(second_file_name)

        with open(TestPdfWorkMethods.test_files_path + '/' + first_file_name, mode='rb') as f_file:
            with open(TestPdfWorkMethods.test_files_path + '/' + second_file_name, mode='rb') as s_file:
                first_reader = PdfFileReader(f_file)
                second_reader = PdfFileReader(s_file)

                test_len = first_reader.getNumPages() + second_reader.getNumPages()
                res_file_name = p_w.unit_file(TestPdfWorkMethods.test_files_path, (first_file_name, second_file_name))
                with open(res_file_name, mode='rb') as res_file:
                    res_reader = PdfFileReader(res_file)
                    self.assertEqual(test_len, res_reader.getNumPages())

                os.remove(res_file_name)

    def test_split_file(self):
        file_name = "Test1.pdf"
        file_path_for_splitting = TestPdfWorkMethods.test_files_path + '/' + file_name
        split_index_list = [1, 5, 10]

        with open(file_path_for_splitting, mode='rb') as split_file:
            split_reader = PdfFileReader(split_file)
            test_pages_num = split_reader.getNumPages()

            res_folder_path = p_w.split_file(TestPdfWorkMethods.test_files_path, file_name, split_index_list)
            self.assertEqual(len(os.listdir(res_folder_path)), len(split_index_list) + 1)

            result_page_num = 0
            for t_file_name in os.listdir(res_folder_path):
                with open(res_folder_path + '/' + t_file_name, mode='rb') as t_file:
                    t_reader = PdfFileReader(t_file)
                    result_page_num += t_reader.getNumPages()
                os.remove(res_folder_path + '/' + t_file_name)

            self.assertEqual(result_page_num, test_pages_num)
            os.rmdir(res_folder_path)

    def test_page_deleting(self):
        test_file_name = "Test1.pdf"
        delete_page_lst = [1, 2, 3]

        with open(TestPdfWorkMethods.test_files_path + '/' + test_file_name, mode='rb') as test_file:
            reader = PdfFileReader(test_file)
            test_len = reader.getNumPages() - len(delete_page_lst)

            res_file_path = p_w.delete_pages(TestPdfWorkMethods.test_files_path, test_file_name, delete_page_lst)

            with open(res_file_path, mode='rb') as res_file:
                res_reader = PdfFileReader(res_file)
                self.assertEqual(test_len, res_reader.getNumPages())

            #os.remove(res_file_path)
