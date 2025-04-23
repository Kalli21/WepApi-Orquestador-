# 📘 Documentación Técnica - WebApi Intermediario

## 1. 🎯 Arquitectura

Este proyecto forma parte de una arquitectura basada en microservicios con comunicación RESTful. En el diagrama general del sistema se representa su posición, sin embargo, este documento se enfoca únicamente en la **WebApi Intermediario**.

### Documentación del proyecto
https://drive.google.com/file/d/11VVjcke___jWK9IltuePe-pejsZQAbUS/view?usp=sharing
---

## 2. 🧩 Patrón de diseño

El patrón de diseño utilizado es **MVC** (Modelo - Vista - Controlador), aplicado principalmente a través de los controladores en la carpeta `Controller`, los cuales exponen las APIs necesarias para la orquestación de los módulos internos.

---

## 3. ⚙️ Instalación y Configuración

### 3.1 Requisitos Previos

- Python 3.9 o superior (**3.10 recomendado**)
- `pip` (gestor de paquetes de Python)
- `virtualenv` (opcional pero recomendado)
- Credenciales de **Firebase File Storage**

### 3.2 Instalación

```bash
# Clona el repositorio
git clone https://github.com/Kalli21/WepApi-Orquestador-.git
cd WepApi-Orquestador-

# (Opcional) Crea y activa un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instala las dependencias
pip install -r requirements.txt

# Corre el proyecto
uvicorn main:app --reload
