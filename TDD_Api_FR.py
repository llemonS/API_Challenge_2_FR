from app import *
import unittest
import json 

app.testing= True

class APITests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
    #rota metrics
    def test_get_metrics(self):
        response = self.app.get("/metrics")
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['Content-Type'])

    #querystring propositalmente errada
    def test_get_metrics_wrong_query(self):
        response = self.app.get("/metrics?last_quotes=asd")
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['Content-Type'])
        self.assertEqual({'mensagem':'Insira um valor numerico para a ultima cotação, na query last_quotes= ex: last_quotes=3'}, response.get_json())
    #querystring propositalmente errada
    def test_get_metrics_wrong_query_v2(self):
        response = self.app.get("/metrics?dd")
        self.assertEqual(404, response.status_code)
        self.assertEqual("application/json", response.headers['Content-Type'])
        self.assertEqual({"mensagem":"Desculpe, essa rota não existe dentro da API."}, response.get_json())
    
    #last quotes vazio diferente de zero
    def test_get_metrics_wrong_query_v3(self):
        response = self.app.get("/metrics?last_quotes=")
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['Content-Type'])
        self.assertEqual({'mensagem':'Insira um valor numerico para a ultima cotação, na query last_quotes= ex: last_quotes=3'}, response.get_json())

    #rota quotes
    def test_post_quote(self):
        response = self.app.post("/quote", data=json.dumps(envio_cotacao), headers={'Content-Type': 'application/json'})
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers['Content-Type'])

    #rotas desconhecidas
    def test_unknown_route(self):
        response = self.app.get("/haha")
        self.assertEqual(404, response.status_code)
        self.assertEqual("application/json", response.headers['Content-Type'])
        self.assertEqual({"mensagem":"Desculpe, essa rota não existe dentro da API."}, response.get_json())
    
    #rota desconhecida v2
    def test_post_quotes_wrong_route(self):
        response = self.app.post("/quotes", data=json.dumps(envio_cotacao))
        self.assertEqual(404, response.status_code)
        self.assertEqual("application/json", response.headers['Content-Type'])

if __name__ == "__main__":
    
    unittest.main()