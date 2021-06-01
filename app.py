#desafio backend 2
from flask import Flask, request, redirect, url_for, render_template, jsonify, Response, make_response,abort
from resources.db_func import Database as db
from resources.controller import *
import requests
import re


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"mensagem":"Desculpe, essa rota não existe dentro da API."}), 404

@app.errorhandler(405)
def page_not_found(error):
    return jsonify({"mensagem":"Desculpe,metodo nao permitido dentro da API."}), 405 

@app.route('/quote', methods=['POST'])

def quote():

    body = dict(request.json)

    #verificando se os campos existem        
    if len(body['destinatario']) < 1: 
        return jsonify({"mensagem":"Favor inserir destinatario."})

    if len(body['destinatario']['endereco']) < 1:
        return jsonify({"mensagem":"Favor inserir campo cep com digitos."})

    if not re.match(pattern="^\d{8}$",string=str(body['destinatario']['endereco']['cep'])):
        return jsonify({"mensagem":"Favor inserir cep de 8 digitos contendo apenas numeros."})

    if len(body['volumes']) < 1:
        return jsonify({"mensagem":"Favor inserir volumes."})

    #validando o schema do destinatário e volumes fornecido pelo usuario
    try:
        validate_destinatario(body.get('destinatario'))
    except KeyError:
        return jsonify(str(validator.errors))

    if len(errors_in_vol(body.get('volumes'))) > 0:
        return jsonify(errors_in_vol(body.get('volumes')))
    
    #nao havendo imprevistos, consumo da api fr
    else:
        body.update(fr_user)
        data =  json.loads(requests.post('https://freterapido.com/api/external/embarcador/v1/quote-simulator',json=body).text)

        try:
            response = parser_quote(data)
            #validando o schema com o json de resposta pela API FR
            schema_erro = val_transportadoras_ans(response.get('transportadoras'))
            if len(schema_erro) > 0:
                return json.dumps(schema_erro)
            
            #resposta esperada
            for cotacao in response['transportadoras']:
                if db.transportador_existe(cotacao['nome']) == False:
                    db.adicionar_transportador(cotacao['nome']) 
                print(db.adicionar_cotacao(dict(cotacao)))
            return jsonify(response)

        #caso não passe pelo schema, mostrar erro
        except TypeError:
            return jsonify(data)


@app.route('/metrics', methods=['GET'])

def metrics():

    #rotas nao obrigatorias que forem metrics puro e metrics?last_quotes= serao redirecionadas
    if str(request.query_string) != "b''":
        try:
            if str(request.args.get('last_quotes').encode()) == "b''":
                last_quotes = 0
        except AttributeError:
            abort(404)
        else:
            try: 
                last_quotes = int(request.args.get('last_quotes'))
            except:
                print("aqui "+str(request.args.get('last_quotes').encode()) +"aqui")
                return jsonify({'mensagem':'Insira um valor numerico para a ultima cotação, na query last_quotes= ex: last_quotes=3'})
        #se existir querystring em last quote, usaremos o valor dela, caso contrário iremos exibir todos.
        return jsonify(db.metricas(last_quotes))
    return jsonify(db.metricas())

if __name__ == '__main__':
    
    db = Database()

    app.run(host='0.0.0.0', port=80)