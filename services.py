import pyrebase
import datetime
import requests

class Servicos:
    
    FIREBASE_KEY = "AIzaSyBYZqhEllq8-vN0XN_yBpav54CCVGRHq9E"
    FIREBASE_AUTH = "teste-tcc-2c7b3.firebaseapp.com"
    FIREBASE_DATABASE = "https://teste-tcc-2c7b3.firebaseio.com/"
    FIREBASE_STORAGE = "teste-tcc-2c7b3.appspot.com"
    
    URL_API = 'http://127.0.0.1:9000/api'
    
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
    
    def skyBiometry(self, diretorio_local, path_firebase, nome_cluster):
        url = self.URL_API
        erro = False
        
        sky_biometry = requests.post(url, files = {'media': open(diretorio_local, 'rb')}).json()
        sky_biometry['current_date'] = self.data('datetime')
        sky_biometry['dev_type'] = 'Entrance'
        sky_biometry['img_url'] = diretorio_local
        sky_biometry['f_url_img'] = path_firebase
        sky_biometry['cluster_id'] = nome_cluster
                
        try:
            sky_biometry = requests.post(url, files = {'media': open(diretorio_local, 'rb')}).json()
            sky_biometry['current_date'] = self.data('datetime')
            sky_biometry['dev_type'] = 'Entrance'
            sky_biometry['img_url'] = diretorio_local
            sky_biometry['f_url_img'] = path_firebase
            sky_biometry['cluster_id'] = nome_cluster
            
        except:
            print('[ERRO] Erro ao receber o retorno da API')
            erro = True
        
        if not erro:
            try:
                inserido = self.saveJsonSkyToFirebase(sky_biometry)
                print('[INFO] Foi inserido o registro ' + inserido)
            except:
                print('[ERRO] Não foi possível inserir o documento de biometria')
        
        return sky_biometry
