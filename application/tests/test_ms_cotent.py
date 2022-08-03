from . import BaseTestClass
import re
import json
class MsContentTestCase(BaseTestClass):

    def test_ms_content_add_unico(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type":"UNICO"
        })
        self.assertEqual(200, res.status_code)
        self.assertIn(b'Se agrego correctamente', res.data)

    def test_ms_content_add_unico_repeated(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type":"UNICO"
        })
        res2 = self.client.post('/api/content/add', json={
            "title": "Los   SimnSómns  \n",
            "type": "UNICO"
        })
        self.assertEqual(200, res2.status_code)
        self.assertIn(b'Ya se encuentra registrado', res2.data)

    def test_ms_content_add_serie_request_fail(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type":"SERIE"
        })
        self.assertEqual(200, res.status_code)
        self.assertIn(b'El programa es tipo Serie, Suministra la season y el episode', res.data)

    def test_ms_content_add_serie(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type":"SERIE",
            "season":1,
            "episode":5

        })
        self.assertEqual(200, res.status_code)
        self.assertIn(b'Se creo serial_episode', res.data)

    def test_ms_content_add_serie_repeated(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type":"SERIE",
            "season":1,
            "episode":5

        })
        res2 = self.client.post('/api/content/add', json={
            "title": "\nLos    Simnsómns",
            "type": "SERIE",
            "season": 1,
            "episode": 5

        })
        self.assertEqual(200, res2.status_code)
        self.assertIn(b'Ya esta registrado', res2.data)

    def test_ms_content_id(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type":"SERIE",
            "season":1,
            "episode":5

        })
        res2 = self.client.get('/api/content/id/1')
        self.assertEqual(200, res2.status_code)
        self.assertIn(b'{\n  "standard_title": "Los simnsomns-1-5", \n  "title": "Los Simnsomns-1-5"\n}\n', res2.data)

    def test_ms_content_title(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type":"SERIE",
            "season":1,
            "episode":5

        })
        res2 = self.client.get('/api/content/title/Los  SimNsómns ')
        self.assertEqual(200, res2.status_code)
        self.assertIn(b'{\n  "standard_title": "Los simnsomns-1-5", \n  "title": "Los Simnsomns-1-5"\n}\n', res2.data)






