# RiesgosGenerales

## Utilitarios

* Crear un environment: `python -m venv <ENV_NAME>`.
* Aplicar el environment: `. /path/to/<ENV_NAME>/bin/activate` (usando _bash_).
* Instalar dependencias requeridas: `pip install -r requirements.txt`.
* Instalar dependencias de desarrollo: `pip install -r requirements-dev.txt`.
* Chequear el código: `pre-commit run --all-files`.
* Cargar data: `python manage.py loaddata-websnapshot`
* Actualizar data: `python manage.py dumpdata --format yaml rrgg auth.user -u rrggweb/fixtures/web-snapshot.yaml`
