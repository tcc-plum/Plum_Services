from services import Servicos
import os
import glob
import time

biometria = Servicos()

PASTA_COM_CLUSTERS = '../Plum_Clustering/clusters'
    
def work_files():
    
    diretorio_local = ''
    cluster = ''
    diretorios = []
    if len(os.listdir(PASTA_COM_CLUSTERS)) > 0:    
        for pasta in os.listdir(PASTA_COM_CLUSTERS):
            
            diretorio_local = PASTA_COM_CLUSTERS + '/'
            cluster = pasta
            caminho_storage = 'SKY/' + cluster + '/' + biometria.data('date')
            diretorio_local = diretorio_local + pasta
            arquivos = glob.glob(diretorio_local + '/*.jpg')
            
            for arquivo in arquivos:
                
                arquivo = arquivo.replace(os.sep, '/')
                nome_arquivo = arquivo.split(sep='/')
                caminho_storage = caminho_storage + '/' + nome_arquivo[-1]
                resultado = biometria.saveFileToCloudStorage(arquivo, caminho_storage)
                url_imagem = biometria.getFileUrlCloudStorage(caminho_storage)
                resultado['img_url'] = url_imagem
                resultado['path_local'] = arquivo
                resultado['path_cloud'] = caminho_storage
                resultado['path_id'] = nome_arquivo[-1]
                
                caminho_json = 'cluster/' + cluster
                
                try:
                    resultado_biometria = biometria.skyBiometry(arquivo, caminho_storage, cluster)
                    
                    if resultado_biometria:
                        inserido = biometria.saveJsonClusterToFirebase(caminho_json, resultado)
                        print('[INFO] Foi inserido o registro ' + inserido)
                except:
                    print('[ERRO] Não foi possível inserir o documento do cluster')
                
                caminho_storage = 'SKY/' + cluster + '/' + biometria.data('date')
                diretorios.append(arquivo)
    else:
        print('[INFO] Não há arquivos para enviar para a API')
        
            
    return diretorios

while True:
    try:
        arquivos = work_files()
        if len(arquivos) > 0:
            for arquivo in arquivos:
                if os.path.isfile(arquivo):
                    print('[INFO] Removendo o arquivo: ' + arquivo)
                    os.remove(arquivo)
    except:
        print('[ERRO] Alguma operação falhou ao operacionalizar a API')
    time.sleep(5)
