from . import BaseTestClass
import re
import json
class MsContentTestCase(BaseTestClass):

    def test_ms_content_add_request_title(self):
        res = self.client.post('/api/content/add',json={
            "type_content":"UNICO"
        })
        self.assertEqual(400, res.status_code)
        self.assertIn(b'Se requiere el campo: title', res.data)

    def test_ms_content_add_request_type_content(self):
        res = self.client.post('/api/content/add',json={
            "title":'Los Simpson'
        })
        self.assertEqual(400, res.status_code)
        self.assertIn(b'Se requiere el campo: type_content', res.data)

    def test_ms_content_add_unico(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type_content":"UNICO"
        })
        self.assertEqual(200, res.status_code)
        self.assertIn(b'Se agrego correctamente', res.data)

    def test_ms_content_add_unico_repeated(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type_content":"UNICO"
        })
        res2 = self.client.post('/api/content/add', json={
            "title": "Los   SimnSómns  \n",
            "type_content": "UNICO"
        })
        self.assertEqual(200, res2.status_code)
        self.assertIn(b'Ya se encuentra registrado', res2.data)

    def test_ms_content_add_serie_request_fail_season(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type_content":"SERIE"
        })
        self.assertEqual(400, res.status_code)
        self.assertIn(b'el programa es tipo SERIE se requiere el campo season', res.data)

    def test_ms_content_add_serie_request_fail_episode(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type_content":"SERIE",
            "season":1
        })
        self.assertEqual(400, res.status_code)
        self.assertIn(b'el programa es tipo SERIE se requiere el campo episode', res.data)

    def test_ms_content_add_serie(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type_content":"SERIE",
            "season":1,
            "episode":5

        })
        self.assertEqual(200, res.status_code)
        self.assertIn(b'Se creo serial_episode', res.data)

    def test_ms_content_add_serie_repeated(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type_content":"SERIE",
            "season":1,
            "episode":5

        })
        res2 = self.client.post('/api/content/add', json={
            "title": "\nLos    Simnsómns",
            "type_content": "SERIE",
            "season": 1,
            "episode": 5

        })
        self.assertEqual(200, res2.status_code)
        self.assertIn(b'Ya esta registrado', res2.data)

    def test_ms_content_add_type_content_different(self):
        res = self.client.post('/api/content/add', json={
            "title": "Los Simnsomns",
            "type_content": "SERIADOS"


        })

        self.assertEqual(400, res.status_code)
        self.assertIn(b"el tipo de contenido SERIADOS no existe debe ser UNICO o SERIE ", res.data)


    def test_ms_content_id(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type_content":"SERIE",
            "season":1,
            "episode":5

        })
        res2 = self.client.get('/api/content/id/1')
        self.assertEqual(200, res2.status_code)
        self.assertIn(b'{\n  "standard_title": "Los simnsomns-1-5", \n  "title": "Los Simnsomns-1-5"\n}\n', res2.data)

    def test_ms_content_id_failed(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type_content":"SERIE",
            "season":1,
            "episode":5

        })
        res2 = self.client.get('/api/content/id/10')
        self.assertEqual(400, res2.status_code)
        self.assertIn(b'No se encontro ningun dato', res2.data)

    def test_ms_content_title(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type_content":"SERIE",
            "season":1,
            "episode":5

        })
        res2 = self.client.get('/api/content/title/Los Simnsomns-1-5')
        self.assertEqual(200, res2.status_code)
        self.assertIn(b'{\n  "standard_title": "Los simnsomns-1-5", \n  "title": "Los Simnsomns-1-5"\n}\n', res2.data)

    def test_ms_content_title_failed(self):
        res = self.client.post('/api/content/add',json={
            "title":"Los Simnsomns",
            "type_content":"SERIE",
            "season":1,
            "episode":5

        })
        res2 = self.client.get('/api/content/title/Los Simnsomns')
        self.assertEqual(400, res2.status_code)
        self.assertIn(b'No se encontro ningun dato', res2.data)







