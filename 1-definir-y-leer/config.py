"""Este demo lee los valores de los parámetros guardados en los archivos TOML anexos."""
#importacion
from dynaconf import Dynaconf

# lectura de archivos
settings = Dynaconf(
   	# directorio de referencia
	root_path="./",         # directorio de trabajo actual (valor default)
	# rutas de archivos (relativas)
    settings_files=[
        'settings.toml',    # se lee primero
        '.secrets.toml'     # se lee segundo
    ],

)

# parametros simples
print(settings.user)
print(settings.password)

# parametros anidados
print(settings.red.host)
print(settings.red.puerto)
