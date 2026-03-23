# Analizador de Rostros IA (Go + Python + Postgres)

Este proyecto es un sistema de análisis de atributos faciales en tiempo real. Utiliza una arquitectura híbrida donde **Python** se encarga del procesamiento de imágenes con Inteligencia Artificial, **PostgreSQL** almacena los metadatos y un servidor en **Go** gestiona las consultas mediante un lenguaje de búsqueda personalizado.

## 🚀 Características principales
- **Detección de Rostros:** Utiliza el backend `RetinaFace` para máxima precisión.
- **Análisis de Atributos:** Predicción de edad, género y 7 tipos de emociones.
- **Procesamiento Asíncrono:** Un "Vigilante" en Python detecta nuevas imágenes y las procesa automáticamente.
- **Query Language Personalizado:** Motor de búsqueda en Go que permite consultas como `FIND faces WHERE age > 20 AND emotion = 'happy'`.
- **Muestra Balanceada:** Script de carga que asegura diversidad de género y edad (20-70 años).

---

## 🛠️ Tecnologías utilizadas
- **Backend:** Go (Golang)
- **IA/ML:** Python 3 (DeepFace, TensorFlow, OpenCV)
- **Base de Datos:** PostgreSQL
- **Librerías clave:** `watchdog` (monitoreo de archivos), `psycopg2` (conexión DB), `net/http` (servidor web).

---

## 📋 Requisitos previos
1. Tener instalado **PostgreSQL** y creada la base de datos `face_attributes`.
2. Contar con el dataset **UTKFace** descargado localmente.
3. Python 3.x con las dependencias: `pip install deepface tf-keras opencv-python watchdog psycopg2`.

---

## 🏃‍♂️ Guía de ejecución

Sigue estos pasos en orden para poner en marcha el sistema:

### 1. Preparar la Base de Datos
Crea la tabla necesaria en PostgreSQL:
```sql
CREATE TABLE face_attributes (
    id SERIAL PRIMARY KEY,
    image_path TEXT UNIQUE,
    age INTEGER,
    gender VARCHAR(20),
    emotion VARCHAR(20)
);
