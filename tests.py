import unittest
import requests
import json
from models import engine
from sqlalchemy.orm import sessionmaker
import app

class LocatorTestCase(unittest.TestCase):

    maxDiff = None

    headers = {
            'Content-Type':'application/json',
            'Accept': 'application/json',
        }

    insert_data = json.dumps({
            'pin':'IN/110001',
            'name':'Connaught Place',
            'admin':'New Delhi',
            'lat':28.6333,
            'lon':77.2167,
        })
    
    
    data = json.dumps({
            'latitude':28.6333,
            'longitude': 77.2167,
            'radius': 5.0,
        })

    session = None

    ans = {'nearby': ['IN/110001', 'IN/110002', 'IN/110003', 'IN/110004', 'IN/110005', 'IN/110006', 'IN/110008', 'IN/110020', 
                        'IN/110021', 'IN/110022', 'IN/110023', 'IN/110024', 'IN/110025', 'IN/110026', 'IN/110027', 'IN/110028',
                        'IN/110029', 'IN/110051', 'IN/110052', 'IN/110053', 'IN/110054', 'IN/110055', 'IN/110056', 'IN/110057',
                        'IN/110058', 'IN/110059', 'IN/110060', 'IN/110061', 'IN/110062', 'IN/110063', 'IN/110064', 'IN/110065',
                        'IN/110066', 'IN/110067', 'IN/110081', 'IN/110082', 'IN/110083', 'IN/110084', 'IN/110091', 'IN/110092', 
                        'IN/110093', 'IN/110094', 'IN/110096'],
                'msg': 'Successful',
                'number': 43}
    
    def setUp(self):
        print("Setting up")
        self.session = sessionmaker(bind=engine)
        self.session = self.session()
        self.app = app

    def tearDown(self):
        self.session.close()
        print("Shutting Down")

    def testPostDataWithSameLatAndLan(self):
        insert_data = json.dumps({
            'pin':'IN/810001',
            'name':'Connaught Place',
            'admin':'New Delhi',
            'lat':28.6333,
            'lon':77.2167,
        })
        res = self.app.get('/')
        res = requests.post("http://127.0.0.1:5000/post_location", data=insert_data, headers=self.headers)

        val = res.json()
        self.assertEqual(val,{'msg':'Already present'})

    def testPostWrongData(self):
        insert_data = json.dumps({
            'pin':'IN/810001',
            'admin':'New Delhi',
            'lat':28.6333,
            'lon':77.2167,
        })
        res = requests.post("http://127.0.0.1:5000/post_location", data=insert_data, headers=self.headers)

        val = res.json()
        self.assertEqual(val,{'msg':'Incomplete data'})

    def testCompareGetApis(self):
        res1 = requests.get("http://127.0.0.1:5000/get_using_postgres", data=self.data, headers=self.headers)
        val1 = res1.json()

        res2 = requests.get("http://127.0.0.1:5000/get_using_postgres", data=self.data, headers=self.headers)
        val2 = res2.json()

        self.assertEqual(val2['nearby'],val1['nearby'])

    def test_PostCheckSamePin(self):
        res = requests.post("http://127.0.0.1:5000/post_location", data=self.insert_data, headers=self.headers)

        val = res.json()
        self.assertEqual(val,{'msg':'Already present'})
    
    def test_PostgresCheck(self):
        res = requests.get("http://127.0.0.1:5000/get_using_postgres", data=self.data, headers=self.headers)
        val = res.json()
        
        self.assertEqual(val,self.ans)
    
    def test_SelfCheck(self):
        res = requests.get("http://127.0.0.1:5000/get_using_self", data=self.data, headers=self.headers)
        val = res.json()

        ans = {'msg': 'Successful', 'number': 43, 'nearby': ['IN/110002', 'IN/110003', 'IN/110004', 'IN/110005', 'IN/110006', 'IN/110007', 'IN/110008', 'IN/110020',
         'IN/110021', 'IN/110022', 'IN/110023', 'IN/110024', 'IN/110025', 'IN/110026', 'IN/110027', 'IN/110028', 'IN/110029', 'IN/110051',
         'IN/110052', 'IN/110053', 'IN/110054', 'IN/110055', 'IN/110056', 'IN/110057', 'IN/110058', 'IN/110059', 'IN/110060',
         'IN/110061', 'IN/110062', 'IN/110063', 'IN/110064', 'IN/110065', 'IN/110066', 'IN/110067', 'IN/110081', 'IN/110082',
         'IN/110083', 'IN/110084', 'IN/110091', 'IN/110092', 'IN/110093', 'IN/110094', 'IN/110096']}
        
        self.assertCountEqual(val['nearby'],ans['nearby'])    


def testTime():
    unittest.main()

if __name__ =='__main__':
    from timeit import Timer


    t = Timer(lambda: testTime())
    print(t.timeit(number=20))
