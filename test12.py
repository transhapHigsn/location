from app import app
import unittest
import tempfile
import os

class LocatorTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.db_fd = tempfile.mkstemp()
        self.app.config['DATABASE']=tempfile.mkstemp()
        with app.app_context():
            app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

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

if __name__ == '__main__':
    unittest.main()                

