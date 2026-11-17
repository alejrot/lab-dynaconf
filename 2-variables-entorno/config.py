"""Este demo pone a prueba la lectura de variables de entorno, sean éstas declaradas desde la terminal o desde uun archivo '.env'."""
# importacion
from dynaconf import Dynaconf

# CONFIGURAR:
prefijo = False         # prefijo anulado
prefijo = "DEMO"        # prefijo custom


# lectura de variables de entorno
settings = Dynaconf(
    load_dotenv=True,           # lee archivo '.env' (opcional)
    envvar_prefix=prefijo,      # prefijo de variables - valor default: DYNACONF
)

if prefijo is not False:
    print(settings.figurar)
    # print(settings.extra)       # (no encontrada)
else:
    print(settings.extra)
    print(settings.demo_figurar)
