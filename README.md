# YouTube MP3 Downloader

Este script permite descargar audios de YouTube en formato MP3 con la mejor calidad disponible. Procesa múltiples enlaces desde un archivo de texto y los convierte automáticamente.

## Requisitos

- Python 3.6 o superior
- yt-dlp
- ffmpeg (para la conversión de audio)

## Instalación

### 1. Instalar dependencias

#### Instalar yt-dlp

Puedes instalar yt-dlp mediante pip:

```bash
pip install yt-dlp
```

El script intentará instalar automáticamente yt-dlp si no está disponible en tu sistema.

#### Instalar ffmpeg (Windows)

1. Descarga ffmpeg desde [ffmpeg.org](https://ffmpeg.org/download.html) o desde [este enlace directo](https://github.com/BtbN/FFmpeg-Builds/releases)
2. Extrae el archivo descargado
3. Copia la carpeta extraída a una ubicación permanente (por ejemplo, `C:\ffmpeg`)
4. Añade la carpeta `bin` de ffmpeg al PATH de Windows:
   - Abre el Panel de Control
   - Busca "variables de entorno" y selecciona "Editar las variables de entorno del sistema"
   - En la pestaña "Avanzado", haz clic en "Variables de entorno"
   - En la sección "Variables del sistema", selecciona "Path" y haz clic en "Editar"
   - Haz clic en "Nuevo" y añade la ruta a la carpeta bin (ejemplo: `C:\ffmpeg\bin`)
   - Haz clic en "Aceptar" para cerrar todas las ventanas

Hay un video tutorial disponible que explica este proceso paso a paso.

#### Instalar ffmpeg (macOS)

Usando Homebrew:

```bash
brew install ffmpeg
```

#### Instalar ffmpeg (Linux)

Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

Fedora:
```bash
sudo dnf install ffmpeg
```

Arch Linux:
```bash
sudo pacman -S ffmpeg
```

## Uso

### 1. Preparar el archivo de URLs

Crea un archivo de texto llamado `descargas.txt` en el mismo directorio que el script. Añade una URL de YouTube por línea. Por ejemplo:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=jNQXAC9IVRw
```

### 2. Ejecutar el script

```bash
python youtube_mp3_downloader.py
```

### 3. Resultados

- Los archivos MP3 descargados se guardarán en una carpeta llamada `descargas`
- Si alguna descarga falla, las URLs correspondientes se guardarán en `fallidos.txt`

## Características

- Descarga audios en formato MP3 con la mejor calidad disponible
- Manejo de errores con reintentos automáticos
- Creación automática de carpeta de destino
- Registro de URLs fallidas para reintentos posteriores
- Información detallada del progreso durante la descarga

## Solución de problemas

Si encuentras problemas con las descargas:

1. Asegúrate de que ffmpeg esté correctamente instalado y en el PATH del sistema
2. Verifica tu conexión a internet
3. Comprueba que las URLs en `descargas.txt` sean válidas
4. Intenta actualizar yt-dlp a la última versión:
   ```bash
   pip install -U yt-dlp
   ```

## Notas adicionales

- El script creará automáticamente la carpeta `descargas` si no existe
- Los archivos se nombrarán según el título del video de YouTube
- Las URLs fallidas se pueden reintentar renombrando `fallidos.txt` a `descargas.txt`
