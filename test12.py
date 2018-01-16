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

    insert_sql = "Insert into Location values (?,?,?,?,?,?)"
    select_sql = "Select * from Location"

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

    def test_emptyDb(self):
        with app.app_context():
            cur = apper.get_db().cursor()
            d = cur.fetchall()
            self.assertEqual(len(d), 0)

    def test_firstInsertDb(self):
        data = ('1','Gurgaon', 'Haryana', 45.23, 23.21, 5)
        with app.app_context():
            cur = apper.get_db().cursor()
            cur.execute(self.insert_sql, data)
            self.assertEqual(cur.lastrowid, 1)

    def test_updateDb(self):
        data = ('1', 'Gurgaon', 'Haryana', 45.23, 23.21, 5)
        with app.app_context():
            conn = apper.get_db()
            cur = conn.cursor()
            cur.execute(self.insert_sql, data)
            conn.commit()

            sql2 = "Update Location set place_name='South Delhi' where accuracy=5"
            cur.execute(sql2)
            conn.commit()

            #sql3 = "Select * from Location" #" where place_name='Gurgaon'"
            cur.execute(self.select_sql)
            d = cur.fetchone()

            self.assertEqual(d['place_name'], 'South Delhi')

    def test_dbSelectQuery(self):
        data = ('1','Gurgaon', 'Haryana', 45.23, 23.21, 5)
        with app.app_context():
            conn = apper.get_db()
            cur = conn.cursor()
            #sql1 = "INSERT INTO Location VALUES ('1', 'Gurgaon', 'Haryana', 45.23, 23.21, 5)"
            cur.execute(self.insert_sql, data)
            conn.commit()

            sql2 = "SELECT * FROM Location where accuracy=0"
            cur.execute(sql2)
            d = cur.fetchall()

            self.assertEqual(len(d), 0)

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

