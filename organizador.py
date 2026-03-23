import os
import shutil
import random


ORIGEN_UTK = "C:/Users/xime0/Downloads/UTKFace" 
DESTINO = "C:/analizadorfotos/uploads"

def cargar_muestra_balanceada():
    if not os.path.exists(DESTINO): os.makedirs(DESTINO)
    
    
    hombres_listos = {edad: False for edad in range(20, 71)}
    mujeres_listas = {edad: False for edad in range(20, 71)}
    
    archivos = os.listdir(ORIGEN_UTK)
    random.shuffle(archivos) 
    
    contador = 0
    print("🚀 Buscando parejas (Hombre/Mujer) de 20 a 70 años...")

    for nombre in archivos:
        partes = nombre.split('_')
        if len(partes) >= 2:
            try:
                edad = int(partes[0])
                genero = partes[1] 
                
                if 20 <= edad <= 70:
                    
                    if genero == '0' and not hombres_listos[edad]:
                        shutil.copy(os.path.join(ORIGEN_UTK, nombre), os.path.join(DESTINO, nombre))
                        hombres_listos[edad] = True
                        contador += 1
                    
                    elif genero == '1' and not mujeres_listas[edad]:
                        shutil.copy(os.path.join(ORIGEN_UTK, nombre), os.path.join(DESTINO, nombre))
                        mujeres_listas[edad] = True
                        contador += 1
            except: continue
            
       
        if all(hombres_listos.values()) and all(mujeres_listas.values()):
            break

    print(f"✅ ¡Misión cumplida! Se enviaron {contador} fotos balanceadas a 'uploads'.")

if __name__ == "__main__":
    cargar_muestra_balanceada()