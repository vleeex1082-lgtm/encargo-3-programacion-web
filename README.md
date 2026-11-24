# Encargo 3 – Programación Web

Aplicación con Flask para realizar dos ejercicios: calcular un promedio con asistencia y comparar la cantidad de letras de tres nombres. Los resultados se guardan en memoria mientras el servidor está funcionando.

## Requisitos

- Python 3.10 o posterior
- pip

## Instalar y ejecutar

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Luego abre http://127.0.0.1:5000 en el navegador. Para detener el servidor, presiona Ctrl+C en PowerShell.

## Ejercicios

- **Ejercicio 1:** recibe tres notas entre 10 y 70 y un porcentaje de asistencia entre 0 y 100. Se aprueba con promedio desde 40 y asistencia desde 75%.
- **Ejercicio 2:** recibe tres nombres diferentes y muestra el nombre con más letras. Los espacios y signos no se cuentan.

El menú tiene dos botones, uno para cada ejercicio. La carpeta `templates` guarda las páginas HTML y la carpeta `static` contiene los estilos CSS. El historial permite revisar y borrar resultados mientras la aplicación está abierta.

## Evidencia

Las capturas de la aplicación y su manifiesto de integridad están en `evidencias/`. `enlace_github.txt` se debe completar con la URL del repositorio antes de entregar en Blackboard.
