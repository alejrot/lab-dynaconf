"""Este demo pone a prueba la definición de multiples 'entornos' (grupos de valores) preconfigurados en los archivos TOML."""
#importar
from dynaconf import Dynaconf

# lectura de parámetros
settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        'settings.toml',
    ],
    load_dotenv=True,           # lee archivo '.env' (opcional)
   	# opciones de entornos
    environments=True,              # habilitacion
    default_env="development",      # el predefinido
    ## opciones elegibles:
    # env="production",
    # env="development",
    env="container",                # el elegido actualmente

)


print(settings.host)
print(settings.puerto)

# lista_vars = dict(settings).keys()
# for variable in lista_vars:
#     print(variable)
