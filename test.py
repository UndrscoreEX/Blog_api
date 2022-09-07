import unittest
import requests

class TestCalc(unittest.TestCase):
    URL = 'https://api.somethingsomethingaws.ml'


    def test_home(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        print('home page works')

    def test_search(self):
        kw_test1 = {'inpt':'japan'}
        kw_test2 = {'inpt':'tokyo beer'}
        resp_p1 = requests.post(f'{self.URL}/all/search-json',data=kw_test1)
        resp_p2 = requests.post(f'{self.URL}/all/search-json', data=kw_test2)
        self.assertEqual(len(resp_p1.json()),23)
        self.assertEqual(len(resp_p2.json()),8)
        print('search function works')

    def test_pages(self):
        respes = [requests.get(self.URL+"/pages/{x}") for x in ['1','30','70','94']]
        for resp in respes:
            self.assertEqual(resp.status_code, 200)   
            print('page loads')     




if __name__ == '__main__':
    tester = TestCalc()
    tester.test_home()
    tester.test_search()
    tester.test_pages()