# 🎀 TikTok Downloader

Aplicación web amigable para descargar videos de TikTok en alta calidad o de forma rápida, sin marcas de agua.

### 1. Clona el repositorio
```bash
git clone https://github.com/milennne/sem04_practica.git
cd tiktok-downloader
```
*(Nota: Cambia `tu-usuario` y la URL por el enlace real de tu repositorio de GitHub)*

### 2. Elige una versión y ejecútala

#### Versión Base
```bash
docker build -t video-downloader:v1.0 .
docker run -d -p 5000:5000 --name video-app video-downloader:v1.0
```

#### Versión Optimizada
```bash
docker build -f Dockerfile.optimizado -t video-downloader:v1.1-optimizado .
docker run -d -p 5000:5000 --name video-app video-downloader:v1.1-optimizado
```

#### Versión Multi-stage
```bash
docker build -f Dockerfile.multistage -t video-downloader:v1.2-multistage .
docker run -d -p 5000:5000 --name video-app video-downloader:v1.2-multistage
```

### 3. Abre la app
[http://localhost:5000](http://localhost:5000)
