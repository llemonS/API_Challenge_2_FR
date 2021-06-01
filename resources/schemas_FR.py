#schemas e dicionarios para uso da plataforma

fr_user = {'codigo_plataforma': '588604ab3', 
            'token': 'c8359377969ded682c3dba5cb967c07b', 
            'retornar_consolidacao': True, 
            'remetente':{'cnpj': '17184406000174'}}


schema_destinatario ={
          "endereco":{
            "type":"dict","required":True, "schema":{
                "cep":{
                "type":"string", "required":True}}}}

schema_volumes={
          "tipo":{"type":"integer","required":True},
          "sku":{"type":"string"},
          "tag":{"type":"string"}, 
          "descricao":{"type":"string"},
          "quantidade":{"type":"integer","required":True},
          "altura":{"type":"float","required":True},
          "largura":{"type":"float","required":True},
          "comprimento":{"type":"float","required":True},
          "peso":{"type":"float", "required":True},
          "valor":{"type":"float","required":True},
          "volumes_produto":{"type":"integer"},
          "consolidar":{"type":"boolean"},
          "sobreposto":{"type":"boolean"},
          "tombar":{"type":"boolean"},}

schema_transportadoras={
  "nome":{"type":"string", "required":True},
  "servico":{"type":"string","required":True},
  "prazo_entrega":{"type":"integer", "required":True},
  "preco_frete":{"type":"float", "required":True},}

