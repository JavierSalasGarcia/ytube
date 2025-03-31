#!/usr/bin/env python3
"""
Script para descargar audios de YouTube en formato MP3 con la mejor calidad disponible
desde enlaces almacenados en un archivo de texto.

Requisitos:
pip install yt-dlp
"""

import os
import sys
import time
import subprocess
import platform

def check_yt_dlp_installed():
    """Verifica si yt-dlp está instalado."""
    try:
        subprocess.run(["yt-dlp", "--version"], 
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE, 
                       check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def instalar_yt_dlp():
    """Instala yt-dlp usando pip."""
    print("Instalando yt-dlp...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], 
                      check=True)
        print("yt-dlp instalado correctamente.")
        return True
    except subprocess.SubprocessError as e:
        print(f"Error al instalar yt-dlp: {e}")
        return False

def descargar_audio(url, carpeta_destino="descargas", intentos_max=2):
    """
    Descarga el audio de un video de YouTube en formato MP3 usando yt-dlp.
    
    Args:
        url (str): URL del video de YouTube
        carpeta_destino (str): Carpeta donde se guardarán los audios
        intentos_max (int): Número máximo de intentos en caso de fallos
    
    Returns:
        bool: True si la descarga fue exitosa, False en caso contrario
    """
    # Crear carpeta de destino si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    # Opciones para yt-dlp
    # -x: Extraer audio
    # --audio-format mp3: Formato MP3
    # --audio-quality 0: Mejor calidad
    # -o: Patrón de nombre de salida
    comando = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", f"{carpeta_destino}/%(title)s.%(ext)s",
        url
    ]
    
    # Intentar descargar con reintentos
    for intento in range(1, intentos_max + 1):
        try:
            print(f"Descargando: {url}")
            resultado = subprocess.run(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            
            # Verificar si la descarga fue exitosa
            if resultado.returncode == 0:
                print(f"✓ Descarga completa.")
                return True
            else:
                print(f"Error en la descarga (intento {intento}/{intentos_max}):")
                print(resultado.stderr)
                
                if intento < intentos_max:
                    tiempo_espera = intento * 3
                    print(f"Reintentando en {tiempo_espera} segundos...")
                    time.sleep(tiempo_espera)
                else:
                    print("Se alcanzó el número máximo de intentos.")
                    return False
        
        except Exception as e:
            print(f"Error al procesar {url}: {str(e)}")
            if intento < intentos_max:
                tiempo_espera = intento * 3
                print(f"Reintentando en {tiempo_espera} segundos...")
                time.sleep(tiempo_espera)
            else:
                return False
    
    return False

def main():
    """
    Función principal que lee las URLs desde el archivo y procesa cada enlace.
    """
    # Verificar si yt-dlp está instalado
    if not check_yt_dlp_installed():
        print("yt-dlp no está instalado.")
        if not instalar_yt_dlp():
            print("No se pudo instalar yt-dlp. Por favor, instálalo manualmente con:")
            print("pip install yt-dlp")
            sys.exit(1)
    
    archivo_urls = "descargas.txt"
    carpeta_destino = "descargas"
    
    # Verificar si el archivo existe
    if not os.path.exists(archivo_urls):
        print(f"Error: El archivo {archivo_urls} no existe.")
        print(f"Por favor, crea un archivo llamado '{archivo_urls}' con una URL de YouTube por línea.")
        sys.exit(1)
    
    # Contador de descargas
    total_urls = 0
    descargas_exitosas = 0
    urls_fallidas = []
    
    # Leer archivo de URLs
    try:
        with open(archivo_urls, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file if line.strip()]
    except UnicodeDecodeError:
        try:
            with open(archivo_urls, 'r', encoding='latin-1') as file:
                urls = [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f"Error al leer el archivo: {str(e)}")
            sys.exit(1)
    
    total_urls = len(urls)
    
    if total_urls == 0:
        print("No se encontraron URLs para descargar.")
        print("Asegúrate de que el archivo no esté vacío y contenga URLs válidas de YouTube.")
        sys.exit(0)
    
    print(f"Se encontraron {total_urls} URLs para descargar.")
    print(f"Los archivos se guardarán en la carpeta: {os.path.abspath(carpeta_destino)}")
    print("Iniciando descargas...")
    
    # Procesar cada URL
    for i, url in enumerate(urls, 1):
        print(f"\nProcesando [{i}/{total_urls}]: {url}")
        if descargar_audio(url, carpeta_destino):
            descargas_exitosas += 1
        else:
            urls_fallidas.append(url)
        
        # Pequeña pausa entre descargas para evitar sobrecarga
        if i < total_urls:
            time.sleep(1.5)
    
    # Resumen final
    print(f"\nResumen de descargas:")
    print(f"Total de URLs procesadas: {total_urls}")
    print(f"Descargas exitosas: {descargas_exitosas}")
    print(f"Descargas fallidas: {total_urls - descargas_exitosas}")
    
    # Guardar las URLs fallidas para un posible reintento
    if urls_fallidas:
        fallidos_archivo = "fallidos.txt"
        with open(fallidos_archivo, 'w', encoding='utf-8') as f:
            for url in urls_fallidas:
                f.write(f"{url}\n")
        print(f"\nLas URLs que no pudieron descargarse se guardaron en '{fallidos_archivo}'")
        print("Puedes reintentar esas descargas más tarde renombrando ese archivo a 'descargas.txt'.")

if __name__ == "__main__":
    main()