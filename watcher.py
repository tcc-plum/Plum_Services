import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from services import Servicos
import os

class Watcher:
    
    DIRECTORY_TO_WATCH = '../Plum_Clustering/clusters'

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            
            biometria = Servicos()
            time.sleep(2)
            biometria.skyBiometry(event.src_path)
            time.sleep(2)
            os.remove(event.src_path)
