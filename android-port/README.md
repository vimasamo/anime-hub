# Instrucciones para Compilar el APK de Android

Este directorio contiene todo lo necesario para convertir el Anime Hub en una aplicación nativa de Android usando **Capacitor**.

## Requisitos Previos

1.  **Node.js y npm**: Instalados en tu sistema.
2.  **Android Studio**: Instalado y configurado con el SDK de Android.
3.  **Backend Desplegado**: Debes subir el contenido de la carpeta `/server` a Koyeb o Render primero.

## Pasos para Compilar

1.  **Actualizar la URL de la API**:
    Edita el archivo `www/app.js` y cambia la constante `API_URL` por la URL real de tu backend desplegado.

2.  **Instalar Dependencias**:
    ```bash
    npm install
    ```

3.  **Añadir Plataforma Android**:
    ```bash
    npx cap add android
    ```

4.  **Sincronizar el Código**:
    Cada vez que hagas cambios en la carpeta `www/`, ejecuta:
    ```bash
    npx cap sync
    ```

5.  **Abrir en Android Studio**:
    ```bash
    npx cap open android
    ```
    Desde Android Studio, podrás ejecutar la app en un emulador o generar un APK firmado (`Build > Build Bundle(s) / APK(s) > Build APK(s)`).

## Estructura de Archivos
- `www/`: Contiene una copia del frontend.
- `capacitor.config.json`: Configuración principal de la app.
- `package.json`: Dependencias de Capacitor.
