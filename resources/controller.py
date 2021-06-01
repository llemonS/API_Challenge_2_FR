#Responsavel por tratar como dicionarios os dados em json, obedecendo os campos aninhados

from cerberus import Validator
from resources.schemas_FR import fr_user, schema_destinatario, schema_volumes, schema_transportadoras
import json

validator = Validator()


def parse_body_quote(data):

    row_dict = dict(data)

    return {
            'nome': row_dict.get('nome'),
            'servico': row_dict.get('servico'),
            'prazo_entrega': row_dict.get('prazo_entrega'),
            'preco_frete' : row_dict.get('preco_frete')
    }

def parser_quote(data):
    transports = []
    row_dict = dict(data)
    print(row_dict)
    for row in row_dict.get('transportadoras'):
        transports.append(parse_body_quote(row))

    return {
            'transportadoras': transports
    }


#validacao do schema do destinatario fornecido pelo usuario
def validate_destinatario(data):
    return validator.validate(data,schema_destinatario)

#validacao do schema de cada volume fornecido pelo usuario
def errors_in_vol(data):
    volume_validacao = []
    volume_error_messages = []
    for item in data:
        if validator.validate(item, schema_volumes) != True:
            volume_validacao.append(validator.validate(item))
            volume_error_messages.append(validator.errors)

    return volume_error_messages

#validacao dos dados vindos pela API da FR
def val_transportadoras_ans(data):
    transp_validacao = []
    transp_error_messages= []
    for item in data:
        if validator.validate(item, schema_transportadoras) != True:
            transp_error_messages.append({'mensagem':"erro de validacao do schema no consumo da API da FR"})
            transp_validacao.append(validator.validate(item))
            transp_error_messages.append(str(validator.errors))
    return transp_error_messages