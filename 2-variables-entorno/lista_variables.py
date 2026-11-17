# importacion
from dynaconf import Dynaconf

# lectura de variables - filtrado por prefijo
settings = Dynaconf(
    # envvar_prefix="DEMO",
    envvar_prefix=False,
    load_dotenv=True,
)

# lista de variables de entorno (SIN su prefijo )
lista_vars = dict(settings).keys()
for variable in lista_vars:
    print(variable)
