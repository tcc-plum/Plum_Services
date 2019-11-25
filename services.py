import pyrebase
import datetime
import requests
import random
import datetime
import os
import base64
import json
import uuid
from persistence import MySQL

class Servicos:
    
    FIREBASE_KEY = "AIzaSyBYZqhEllq8-vN0XN_yBpav54CCVGRHq9E"
    FIREBASE_AUTH = "teste-tcc-2c7b3.firebaseapp.com"
    FIREBASE_DATABASE = "https://teste-tcc-2c7b3.firebaseio.com/"
    FIREBASE_STORAGE = "teste-tcc-2c7b3.appspot.com"
    
    URL_API = 'http://127.0.0.1:9000/api'
    
    JSON_DB_PATH = 'DB/'
    
    def firebase(self):
        k_fields = ["apiKey", "authDomain", "databaseURL", "storageBucket"]
        v_fields = [self.FIREBASE_KEY, self.FIREBASE_AUTH, self.FIREBASE_DATABASE, self.FIREBASE_STORAGE]
        config = dict(zip(k_fields, v_fields))
        return pyrebase.initialize_app(config)
    
    def storage(self):
        return self.firebase().storage()
    
    def db(self):
        return self.firebase().database()
    
    def data(self, tipo='datetime'):
        resultado = ''
        if tipo == 'datetime':
            resultado = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        elif tipo == 'date':
            resultado = datetime.datetime.now().strftime('%Y%m%d')
        return resultado
    
    def saveFileToCloudStorage(self, diretorio_foto, caminho_storage):
        return self.storage().child(caminho_storage).put(diretorio_foto, self.FIREBASE_KEY)
    
    def getFileUrlCloudStorage(self, caminho_storage):
        return self.storage().child(caminho_storage).get_url(self.FIREBASE_KEY)
    
    def saveJsonSkyToFirebase(self, json_file):
        return self.db().child("sky").push(json_file)
    
    def saveJsonClusterToFirebase(self, caminho_do_cluster, json_file):
        return self.db().child(caminho_do_cluster).push(json_file)
    
    def salvarDB(self, documento):
        
        id = uuid.uuid4()
        id = str(id).replace('_', '')
        id = str(id).replace('-', '')
        id = str(id).replace('/', '')
        
        json_file = str(id) + ".json"
        json_string = {id : documento}
        json_path = self.JSON_DB_PATH + json_file
        
        try:          
            with open(json_path, 'w', encoding='utf8') as arquivo:
                json.dump(json_string, arquivo, ensure_ascii=False)
                arquivo.close()
            
            self.insereMySQL(id, json_string)
        except:
            print('[ERRO] Documento JSON não gerado ou registros não inseridos no MySQL')
        
        return str(id)
    
    def insereMySQL(self, id, json_string):
        mysql = MySQL()
        sentimentos = ["irritação", "náusea", "medo", "felicidade", "tristeza", "surpresa", "neutralidade"]
        
        ## Documento
        HashID = id
        Data = json_string[HashID]['resposta']['data']
        
        fk = mysql.inserir_documento(HashID, Data)
        
        ## Foto
        Nome = json_string[HashID]['resposta']['foto']['nome']
        Largura = json_string[HashID]['resposta']['foto']['largura']
        Altura = json_string[HashID]['resposta']['foto']['altura']
        Local = json_string[HashID]['local_dir']
        Dispositivo = json_string[HashID]['dispositivo']
        Imagem = json_string[HashID]['blob']
        
        mysql.inserir_foto(Nome, Largura, Altura, Local, Dispositivo, Imagem, fk)
        
        ## Sentimento        
        for i in range(0, 7):
            Descricao = sentimentos[i]
            Valor = json_string[HashID]['resposta']['sentimentos'][Descricao]['valor']
            Confianca = json_string[HashID]['resposta']['sentimentos'][Descricao]['confiança']
            mysql.inserir_sentimento(Descricao, Valor, Confianca, fk)
                
        ## Pessoa
        Genero = json_string[HashID]['resposta']['gênero']['valor']
        Confianca_G = json_string[HashID]['resposta']['gênero']['confiança']
        Idade = json_string[HashID]['resposta']['idade']['valor']
        Confianca_I = json_string[HashID]['resposta']['idade']['confiança']
        
        mysql.inserir_pessoa(Genero, Confianca_G, Idade, Confianca_I, fk)
        

    def skyBiometry(self, diretorio_local):
        url = self.URL_API
        erro = False
        
        try:
            dir_local = diretorio_local
            dir_local = str(dir_local).replace(os.sep, '/')    
            arquivo = open(dir_local, 'rb')
            if not arquivo.closed:
                arquivo.close()
                try:
                    arquivo = open(dir_local, 'rb')
                except:
                    print('[ERRO] Não foi possível abrir o arquivo!')
            # sky_biometry = requests.post(url, files = {'media': open(dir_local, 'rb')}).json()
            sky_biometry = requests.post(url, files = {'media': arquivo}).json()
                        
            if sky_biometry['resposta']['status'] == 'sucesso':
                dispositivo = ['entrada','saida']
                indice = random.randint(0,1)
                sky_biometry['dispositivo'] = dispositivo[indice]
                sky_biometry['local_dir'] = dir_local
                
                with open(dir_local, 'rb') as arquivo_2:
                    imagem = arquivo_2.read()
                
                blob = base64.b64encode(imagem)
                
                sky_biometry['blob'] = blob.decode('utf-8')
                
                arquivo.close()
                            
                # guid = self.saveJsonSkyToFirebase(sky_biometry)
                # print('Documento {} inserido com sucesso!'.format(guid))
                
                guid = self.salvarDB(sky_biometry)
                print('Documento {} inserido com sucesso!'.format(guid))
                
            else:
                print('[WARNING] A resposta da tag status não é sucesso!')        
        except:
            print('[ERRO] Erro ao consultar a API ou salvar retorno no Firebase')
            erro = True    
        
        if erro:
            return False
        else:
            return True
