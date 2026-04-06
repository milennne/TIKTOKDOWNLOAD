# 🎀 TikTok Downloader

Aplicación web amigable para descargar videos de TikTok en alta calidad o de forma rápida, sin marcas de agua.

### 1. Clona el repositorio
```bash
git clone https://github.com/milennne/sem04_practica.git
cd TIKTOKDOWNLOAD
```

> ⚠️ Si ya corriste una versión anterior, elimina el contenedor antes de correr la siguiente:
> ```bash
> docker rm -f video-app
>```


### 2. Elige una versión y ejecútala

#### Versión Base
```bash
docker build -t video-downloader:v1.0 .
docker run -d -p 5000:5000 --name video-app video-downloader:v1.0
```

#### Versión Optimizada
```bash
docker rm -f video-app
docker build -f Dockerfile.optimizado -t video-downloader:v1.1-optimizado .
docker run -d -p 5000:5000 --name video-app video-downloader:v1.1-optimizado
```

#### Versión Multi-stage
```bash
docker rm -f video-app
docker build -f Dockerfile.multistage -t video-downloader:v1.2-multistage .
docker run -d -p 5000:5000 --name video-app video-downloader:v1.2-multistage
```

### 3. Abre la app
[http://localhost:5000](http://localhost:5000)
