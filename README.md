# Proyecto de curso

Este es el proyecto que desarrollamos en clase para el **Taller de desarrollo de una aplicación con IA generativa** del [Diplomado en Inteligencia Artificial Generativa](https://educacioncontinua.uc.cl/programas/diplomado-en-inteligencia-artificial-generativa/) de la PUC.

Si quieres partir de cero, te recomiendo comenzar con el [proyecto base](https://github.com/DIAG-TALLER-2024/base).

## ¿Qué es lo que construiremos?

**Next Muby**, una aplicación web donde puedes obtener recomendaciones de películas.

Stack tecnológico:

- [Flask](https://flask.palletsprojects.com/en/stable/) para la aplicación web.
- [Boostrap](https://getbootstrap.com/) como librería de componentes (con [Bootstrap Flask](https://bootstrap-flask.readthedocs.io/en/stable/)).
- [OpenAI API](https://platform.openai.com/) para la interacción con las personas que usan la aplicación.
- [SQLite (con Turso)](https://turso.tech/) como base de datos.

## Instrucciones

### Instalación

Una vez descargado el proyecto, crear Virtual environment:

```sh
python3 -m venv venv
```

Activarlo:

```sh
source venv/bin/activate
```

Instalar dependencias:

```sh
pip install -r requirements.txt
```

### Ejecución

Una vez ya lo instalaste, recuerda activar el Virtual Env:


```sh
source venv/bin/activate
```

Y luego ya puedes ejecutar el proyecto localmente con

```sh
flask run --debug
```

### Agregar a tu propio GitHub

Si descargaste el proyecto con `git clone`, para agregarlo a tu propio repositorio tienes que hacer lo siguiente:

1. [Crear un nuevo repositorio](https://github.com/new) (en blanco).
2. Cambiar la URL del `origin` por la de tu nuevo repositorio: `git remote set-url origin git@github.com:tu-username/tu-nombre-de-repo.git`
3. Listo, ahora puedes subir el código base a tu propio repositorio con `git push -u origin main`
