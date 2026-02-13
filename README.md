# 📺 ANIME HUB

**ANIME HUB** es un reproductor de anime premium diseñado para ofrecer una experiencia limpia, fluida y **totalmente libre de anuncios intrusivos**. 

![ANIME HUB UI](https://via.placeholder.com/800x450?text=ANIME+HUB+Interface)

## ✨ Características

- 🚫 **Ad-Block Integrado**: Olvídate de los popups molestos. El sistema captura el primer intento de publicidad y lo bloquea automáticamente.
- 🎨 **Interfaz Premium**: Diseño moderno con modo oscuro, tipografía elegante y micro-animaciones.
- 🖼️ **Lista de Episodios con Miniaturas**: Navega fácilmente por los episodios con imágenes reales y una disposición vertical clara.
- 🏠 **Dashboard Dinámico**: Carruseles con los últimos episodios actualizados y los animes en emisión.
- 🔍 **Buscador Avanzado**: Filtra por género, año o nombre.

---

## 🚀 Desarrollo (Ejecución desde el código)

Si quieres ejecutar el proyecto para desarrollo o en Linux/macOS:

1. **Instala las dependencias**:
   ```bash
   pip install fastapi uvicorn cloudscraper beautifulsoup4 httpx python-multipart
   ```
2. **Inicia el servidor**:
   ```bash
   cd server
   python main.py
   ```
3. **Abre la app**: Visita `http://localhost:8000` en tu navegador.

---

## 📦 Crear el Ejecutable (.exe) para Windows

Puedes compilar **ANIME HUB** en un único archivo ejecutable para usarlo sin necesidad de tener instalado Python.

### 1. Requisitos
- Tener Python instalado en Windows.
- Instalar PyInstaller:
  ```bash
  pip install pyinstaller
  ```
- Colocar tu archivo de icono (ej: `favicon.ico`) en la carpeta raíz.

### 2. Comando de Compilación
Ejecuta esto en tu terminal dentro de la carpeta del proyecto:

```bash
python -m PyInstaller --noconfirm --onefile --windowed --add-data "frontend;frontend" --icon="favicon.ico" --name "ANIME HUB" server/standalone.py
```

### 3. Resultado
Encontrarás el archivo **`ANIME HUB.exe`** dentro de la carpeta `dist`. Solo necesitas ese archivo para llevarte la aplicación a cualquier parte.

---

## 🛠️ Tecnologías
- **Backend**: Python (FastAPI, Cloudscraper, BeautifulSoup4)
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **Bundling**: PyInstaller

---

*Nota: Este proyecto es un scraper educativo para uso personal.*
