import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from deepface import DeepFace
import psycopg2


FOLDER_TO_WATCH = "C:/analizadorfotos/uploads"
DB_CONFIG = {
    "database": "face_attributes",
    "user": "postgres",
    "password": "102538",
    "host": "127.0.0.1",
    "port": "5432"
}

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            self.process_image(event.src_path)

    def already_exists(self, path):
        """Evita procesar fotos que ya están en la base de datos"""
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM face_attributes WHERE image_path = %s", (path,))
            exists = cur.fetchone() is not None
            cur.close()
            conn.close()
            return exists
        except: return False

    def process_image(self, path):
        try:
            
            if self.already_exists(path):
                return 
            
            print(f"✨ Analizando con RETINAFACE: {os.path.basename(path)}")
            time.sleep(1) 
            
         
            results = DeepFace.analyze(
                img_path=path, 
                actions=['age', 'gender', 'emotion'], 
                detector_backend='retinaface', 
                enforce_detection=False
            )
            
            data = results[0]
            emociones = data['emotion']
            emocion_final = data['dominant_emotion']
            
          
            if emociones.get('happy', 0) > 20:
                emocion_final = 'happy'
            
           
            elif emocion_final == 'sad' and emociones.get('angry', 0) > 15:
                emocion_final = 'angry'

           
            self.save_to_db(path, data['age'], data['dominant_gender'], emocion_final)
            print(f"✅ Procesado: {os.path.basename(path)} -> {emocion_final} (Edad: {data['age']})")
            
        except Exception as e:
            print(f"❌ Error en IA: {e}")

    def save_to_db(self, path, age, gender, emotion):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO face_attributes (image_path, age, gender, emotion) VALUES (%s, %s, %s, %s)",
                (path, age, gender, emotion)
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error DB: {e}")

if __name__ == "__main__":
    if not os.path.exists(FOLDER_TO_WATCH): os.makedirs(FOLDER_TO_WATCH)
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_TO_WATCH, recursive=False)
    print(f"🚀 VIGILANTE ACTIVADO en: {FOLDER_TO_WATCH}")
    print("Listo para recibir fotos de hombres y mujeres...")
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()