import mysql.connector as conn
from mysql.connector import Error

class MySQL:
    
    def conexao(self):
        conect = None
        
        try:
             conect = conn.connect(host='localhost', 
                                   database='plum',
                                   user='alunos', 
                                   password='alunos')
             
            #  if conect.is_connected():
                #  print('Conectado ao banco de dados')
        except Error as e:
            print(e)
            
        # finally:
        #     if conect is not None and conect.is_connected():
        #         conect.close()
            
        return conect
    
    def inserir_documento(self, HashID, Data):       
        conect = self.conexao()
        cursor = conect.cursor()
        
        query = 'INSERT INTO DOCUMENTO (HashID, Data) VALUES (%s, %s)'
        
        cursor.execute(query, (HashID, Data))
        
        # if cursor.lastrowid:
        #     print('ultimo id inserido: ', cursor.lastrowid)
        # else:
        #     print('ultimo id inserido nao encontrado')
        
        inserted_id = cursor.lastrowid
        
        conect.commit()
        
        cursor.close()
        conect.close()
        
        return inserted_id
    
    def inserir_foto(self, Nome, Largura, Altura, Local, Dispositivo, Imagem, FK):
        conect = self.conexao()
        cursor = conect.cursor()
        
        query = 'INSERT INTO FOTO (Nome, Largura, Altura, Local, Dispositivo, Imagem, ID_Foto_Documento) ' \
            'VALUES (%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(query, (Nome, Largura, Altura, Local, Dispositivo, Imagem, FK))
        
        conect.commit()
        
        cursor.close()
        conect.close()
    
    def inserir_sentimento(self, Descricao, Valor, Confianca, FK):
        conect = self.conexao()
        cursor = conect.cursor()
        
        query = 'INSERT INTO SENTIMENTO (Descricao, Valor, Confianca, ID_Sentimento_Documento) ' \
            'VALUES (%s,%s,%s,%s)'
        cursor.execute(query, (Descricao, Valor, Confianca, FK))
        
        conect.commit()
        
        cursor.close()
        conect.close()
        
    def inserir_pessoa(self, Genero, Confianca_G, Idade, Confianca_I, FK):
        conect = self.conexao()
        cursor = conect.cursor()
        
        query = 'INSERT INTO PESSOA (Genero, Confianca_G, Idade, Confianca_I, ID_Pessoa_Documento) ' \
            'VALUES (%s,%s,%s,%s, %s)'
        cursor.execute(query, (Genero, Confianca_G, Idade, Confianca_I, FK))
        
        conect.commit()
        
        cursor.close()
        conect.close()

