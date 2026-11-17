# Tutorial (Básico)

## 0 - Instalación y plantilla

El paquete se instala fácilmente con el gestor de paquetes Python que usemos:

```bash
# con PIP
pip install dynaconf
# con UV
uv add dynaconf
``` 

Una vez instalado podemos crear en el directorio actual una plantilla predefinida:

```bash
# con PIP
dynaconf init
# con UV
uv run dynaconf init
```

Esta es la estructura de archivos obtenida:

```bash
.
├── config.py         # rutina Python
├── settings.toml     # datos publicables
├── .secrets.toml     # datos sensibles
└── .gitignore        # blacklist para Git
```

Se obtiene un archivo `config.py` con una preconfiguración muy básica
y se crean dos archivos TOML vacíos:
- `settings`: se usa para configuraciones generales: usuarios, puertos, rutas de archivo, etc.
- `secrets`:  se usa para los datos sensibles como contraseñas, tokens, etc. 

Agregando la opción `-f` al comando `dynaconf init` se eligen formatos de archivo alternativos: `yaml`, `json`,  etc. El archivo `.gitignore` (archivo oculto) viene preconfigurado para excluir los archivos `secrets` del respaldo en Git, reduciendo el riesgo de filtraciones de datos sensibles.

Para hacer pruebas simplemente se invoca a las rutinas Python:

```bash
# con Python (global o desde el entorno virtual)
python config.py
# con UV
uv run config.py
```

## 1 - Lectura de parámetros desde archivo

### Configurar

Mediante la clase `Dynaconf` se crea un objeto que leerá todos los archivos que le indiquemos en el argumento `setting_files` :

```python
# importacion
from dynaconf import Dynaconf

# lectura de archivos -> objeto 'settings'
settings = Dynaconf(
    # directorio de referencia 
	   root_path="./",          # directorio de trabajo actual (valor default)
		# rutas de archivos (relativas)
    settings_files=[
		'settings.toml',     # se lee primero
	    '.secrets.toml',     # se lee segundo 
	    # (etc.)    
    ], 
)
```

Los archivos se leen en el orden definido por la lista y las variables internas se agrupan en base a las reglas de cada formato de archivo. Si un mismo argumento aparece repetido en varios archivos entonces se toma el valor indicado por el último archivo leído.

### Definición y lectura de parámetros

Dynaconf acepta múltiples formatos para los archivo de configuración: TOML, YAML, JSON, INI, etc.  En este ejemplo se usan dos archivos TOML. Si el archivo `settings.toml` es el siguiente:

```toml
# parametros simples
user = "admin"

# parametros anidados -> subcategoría 'red'
[red]
host="127.0.0.1"
puerto=8000
```
donde hay un parámetro suelto llamado `user` y dos parámetros llamados  `host` y `puerto` agrupados dentro de `red`. Además el archivo `.secrets.toml` (archivo oculto) contiene una contraseña:

```toml
# parametros simples
password="1234"
```

entonces Dynaconf mostrará las variables definidas en los archivos como **atributos** del objeto `settings`, respetando la estructura original. En el ejemplo previo los valores podrán ser consultados así:

```python
# parametros simples
print(settings.user)
print(settings.password)

# parametros anidados
print(settings.red.host)
print(settings.red.puerto)
```
Nótese que los atributos `host` y `puerto` quedan contenidos dentro del atributo `red` porque así se los organizó en el archivo TOML.

## 2 - Variables de entorno

Las variables de entorno son variables manejadas en la *shell*, por fuera de la rutina de Python. Dynaconf podrá leerlas **siempre y cuando** se cumplan dos reglas:
- las variables deben ser preexistentes, de otro modo el programa fallará;
- sus nombres deben comenzar con un prefijo predefinido, o serán ignoradas.


### Configurar 

La configuración mínima para leer variables de entorno es la siguiente:

```python
# importacion
from dynaconf import Dynaconf

# lectura de variables de entorno
settings = Dynaconf(
    load_dotenv=True,          # lee archivo '.env' (opcional)
    envvar_prefix="DEMO"       # prefijo de variables - valor default: DYNACONF
)
```

En este ejemplo el prefijo elegido es `DEMO`, por ello los nombres de variables deberán empezar con `DEMO_`. 

Esta es la estructura de archivos:

```bash
.
├── config.py        # rutina Python
└── .env             # archivo para variables de entorno (opcional)
```

### Declarar  y leer variables

Las variables pueden ser declaradas desde la terminal:

```bash
export DEMO_FIGURAR="Quiero aparecer en el programa - definida desde SHELL"
```

o pueden ser declaradas en un archivo `.env`: 

```env
DEMO_FIGURAR="Quiero aparecer en el programa - definida desde ARCHIVO"
```

Si se usan ambos mecanismos entonces prevalecerán los valores definidos desde terminal. La lectura se hace omitiendo el prefijo en los nombres de atributo:

```python
print(settings.figurar)
```

Los nombres de **todas las variables ya detectadas**  por Dynaconf, sin su prefijo, son los siguientes:

``` python
# lista de variables de entorno (SIN su prefijo )
lista_vars = dict(settings).keys()
for variable in lista_vars:
    print(variable)
```

### Anular prefijos

El prefijo de las variables de entorno se puede anular haciendo `envvar_prefix=False`: 

```python
# importacion
from dynaconf import Dynaconf

# lectura de variables de entorno
settings = Dynaconf(
    load_dotenv=True,          # lee archivo '.env' (opcional)
    envvar_prefix="False"      # prefijo ANULADO
)
```

En este caso se podrá **leer a todas las variables de entorno** disponibles en la *shell* y además no se modificarán sus nombres:
```python
print(settings.demo_figurar)
``` 

## 3 - Múltiples entornos

A menudo los valores de los parámetros de configuración deben adaptarse al entorno en donde se desplegará el programa. 

Parámetros típicos:
- sistema  de archivos: rutas a archivos y directorios
- red: IPs, dominios, rutas, puertos
- credenciales: usuarios, contraseñas, *tokens* de acceso.
- etc.

Es conveniente agrupar los valores de los parámetros en distintos grupos y elegir la combinación más conveniente en el despliegue actual. A cada grupo  de parámetros se lo llama **entorno**.

### Agrupar las variables 

imagínese por ejemplo un programa cliente que debe hacer peticiones HTTP a un servidor. Dicho servidor puede ser:
- un servidor local para pruebas locales;
- un servidor remoto para trabajo real;
- un servidor desplegado en un *runtime* de contenedores, por ejemplo Docker.

Para cada situación particular se crea un entorno. Un archivo como `settings.toml`acorde es el siguiente:

``` toml
# entorno de pruebas (local) - sistema anfitrión
[development]
host = "localhost"
puerto = 8000

# entorno de producción - servidor remoto
[production]
host = "server.provider.com"
puerto = 80

# despliegue en contenedores
[container]
host = "container-server"
# puerto = 8000         # valor anulado/faltante
```

En este caso cada entorno quedará definido por una clave: `development`, `production`, `container`.  Estas claves no representan subcategorías de parámetros sino que identifican valores alternativos. 

### Configurar entornos

Esta es la configuración típica para trabajar con entornos:

```python
# importacion
from dynaconf import Dynaconf

# lectura de parámetros
settings = Dynaconf(
    settings_files=[
        'settings.toml',
   	    ], 
   	load_dotenv=True,           # lee archivo '.env' (opcional)
   	# Opciones de entornos
   	environments=True,            # habilitacion
   	default_env="development",    # el predefinido
   	env="container",              # el elegido actualmente
)
```

Argumentos fundamentales:

- `environments`: habilita la definición de los entornos
- `env`: indica qué entorno debe elegirse.
- `default_env`: especifica el entorno predefinido. Sus valores sirven de seguro en caso que falten valores en los otros entornos.

### Controlar con variables de entorno

Mediante variables de entorno se puede elegir el entorno a cargar. Esto se realiza con la variable predefinida `ENV_FOR_DYNACONF` , lo cual puede configurarse desde la terminal:

```bash
export ENV_FOR_DYNACONF="production"
```
o también puede realizarse desde un archivo `.env`, tal como se vio previamente.

Creando esta variable se podrá cambiar de entorno activo sin necesidad de modificar el código fuente.
