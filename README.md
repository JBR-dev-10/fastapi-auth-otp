# FastAPI Auth & OTP API

Este proyecto es una API robusta de autenticación y gestión de usuarios construida con **FastAPI**. Implementa un sistema de verificación segura mediante contraseñas de un solo uso (OTP) con vencimiento temporal y protección contra ataques de fuerza bruta.

## 🚀 Características

- **Autenticación Segura:** Registro e inicio de sesión utilizando hashing de contraseñas con `bcrypt` y `passlib`.
- **Verificación OTP:** Generación y validación de códigos de un solo uso con expiración de 15 minutos.
- **Control de Sesiones:** Manejo de tokens JWT (Access y Refresh tokens) y cierre de sesión seguro.
- **Seguridad Dinámica:** Protección contra ataques de fuerza bruta integrada mediante `slowapi`.
- **Base de Datos:** Persistencia relacional configurada con SQLAlchemy y SQLite.

## 🛠️ Requisitos e Instalación

### 1. Clonar el repositorio e ingresar a la carpeta
```bash
git clone <url-de-tu-repositorio>
cd fastapi-auth-otp
```

### 2. Crear y activar el entorno virtual (`venv`)
- **En Windows:**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **En macOS/Linux:**
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar las dependencias corregidas
```bash
pip install -r requirements.txt
```

## 🖥️ Ejecución del Servidor

Para iniciar la API en modo de desarrollo, ejecuta:
```bash
uvicorn app.main:app --reload
```
La documentación interactiva estará disponible en: [http://127.0.0](http://127.0.0)

## 🧪 Pruebas Unitarias e Integración

Las pruebas automatizadas validan los flujos de registro, errores de contraseña, inicio de sesión y perfiles. Para ejecutarlas con el entorno virtual activo:

```bash
pytest -v
```
