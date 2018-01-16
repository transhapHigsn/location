from app import app
import app as apper
import unittest
import json
import os
import tempfile

class LocatorTest(unittest.TestCase):

    insert_data = json.dumps({
        'pin': 'IN/110001',
        'name': 'Connaught Place',
        'admin': 'New Delhi',
        'lat': 28.6333,
        'lon': 77.2167,
    })

    data = json.dumps({
        'latitude': 28.6333,
        'longitude': 77.2167,
        'radius': 5.0,
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    def setUp(self):
        app.config['TESTING'] = True
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()

        self.app = app.test_client()
        apper.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_database(self):
        test = os.path.exists('apper.db')
        self.assertFalse(test)

    def test_schemaSql(self):
        pass

    def test_main(self):
        resp = self.app.get('/', follow_redirects=True)
        self.assertEqual(resp.status_code, 404)

    def test_get1(self):
        resp = self.app.get('/get_using_self', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_get2(self):
        resp = self.app.get('/get_using_postgres', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_post1(self):
        resp = self.app.get('/post_location', follow_redirects=True)
        self.assertEqual(resp.status_code, 405)

    def test_post2(self):
        resp = self.app.post('/post_location', data=self.insert_data, headers=self.headers)
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(resp.status_code, 200)

    def test_postApi(self):
        resp = self.app.post('/post_location', data=self.insert_data, headers=self.headers)
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['msg'], 'Already present')

    def testPostWrongData(self):
        insert_data = json.dumps({
            'pin':'IN/810001',
            'admin':'New Delhi',
            'lat':28.6333,
            'lon':77.2167,
        })
        res = self.app.post("/post_location", data=insert_data, headers=self.headers)
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(data['msg'], 'Incomplete data')

    def testCompareGetApis(self):
        res1 = self.app.get("/get_using_postgres", data=self.data, headers=self.headers)
        data1 = json.loads(res1.get_data(as_text=True))

        res2 = self.app.get("/get_using_self", data=self.data, headers=self.headers)
        data2 = json.loads(res2.get_data(as_text=True))

        self.assertEqual(data1['number'], data2['number'])


if __name__ == '__main__':
    unittest.main()                

