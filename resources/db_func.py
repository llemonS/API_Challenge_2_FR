#Banco com metodos necessarios para consumir dados
import sqlite3
import os

class Database():

    def __init__(self):

        self.db_name = "FR_Challenge.db"
        
        if os.path.exists(str(os.getcwd()+"/"+self.db_name)) != True:
            self.contact(self.db_name, """CREATE TABLE IF NOT EXISTS Transportador(id INTEGER PRIMARY KEY AUTOINCREMENT, Nome VARCHAR(100) NOT NULL);""")
            self.contact(self.db_name, """CREATE TABLE IF NOT EXISTS Cotacao(id INTEGER PRIMARY KEY AUTOINCREMENT, Servico VARCHAR(50) NOT NULL, Prazo_Entrega INTEGER NOT NULL, Preco_Frete REAL NOT NULL, nome_id INTEGER NOT NULL, FOREIGN KEY (nome_id) REFERENCES Transportador(id));""")
    
    def adicionar_transportador(self, nome):
        if self.transportador_existe(nome) == False :
            self.contact(self.db_name, "INSERT INTO Transportador VALUES(NULL,'{0}');".format(nome))
            return True
        return False
        
    def listar_transportadores(self):
        resposta = self.contact(self.db_name, """Select * FROM Transportador""")
        resposta = resposta.fetchall()
        return  dict(resposta)

    def transportador_existe(self, nome):
        transportadores = self.listar_transportadores()
        for _id, _nome in transportadores.items():
            if _nome == nome:
                return(_id)
                break
        return False

    def adicionar_cotacao(self, data):
        row_dict = dict(data)
        transportadores = self.listar_transportadores()
        for _id, _nome in transportadores.items():
          if _nome == row_dict.get('nome'):
            self.contact(self.db_name, "INSERT INTO Cotacao VALUES(NULL,'{0}','{1}','{2}','{3}');".format(row_dict.get('servico'),row_dict.get('prazo_entrega'),row_dict.get('preco_frete'),_id))
            return {"mensagem":"cotacao adicionada com sucesso"}
            break
        return {"mensagem":"nao foi possivel adicionar a cotacao"}

    def listar_cotacoes(self,nome):
        if self.transportador_existe(nome) > 0:
            resposta = self.contact(self.db_name, "Select * From Cotacao INNER JOIN Transportador ON Cotacao.nome_id = Transportador.id WHERE Transportador.Nome = '{0}';".format(nome))
            resposta = resposta.fetchall()
            return list(resposta)
        return {"mensagem": "nao foi possivel encontrar cotacão para o nome {0}".format(nome)}

    def metricas(self, last_quotes=0):
        all_quotes = []
        response = []
        max_min = []
        transportadores = self.listar_transportadores()
        for _id, _nome in transportadores.items():
            all_quotes.append(self.listar_cotacoes(_nome))
        for item in all_quotes:
            if len(item) > 0:
                total = 0
                for field in item:
                    total += field[3]
                response.append({"transportadora":field[6],"quantidade":len(item),"total":total,"media":total/len(item)})
        for each in all_quotes:
            if len(each)>0:
                max_min.append(max(each, key=lambda x:x[3]))
                max_min.append(min(each, key=lambda x:x[3]))

        maximo = max(max_min, key=lambda x:x[3])
        minimo = min(max_min, key=lambda x:x[3])
        response = sorted(response, key=lambda k: k['quantidade'], reverse=True)
        max_min = dict({"maior_cotacao": {"nome":maximo[6],"prazo_entrega":maximo[2],"preco_frete":maximo[3],"servico":maximo[1]}, "menor_cotacao": {"nome":minimo[6],"prazo_entrega":minimo[2],"preco_frete":minimo[3],"servico":minimo[1]}})
        if last_quotes > 0:
            return response[:last_quotes], max_min
        return response, max_min

    def contact(self, database_name , database_command):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        result = cursor.execute(database_command)
        conn.commit()
        return result
