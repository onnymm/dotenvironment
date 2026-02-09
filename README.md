## Variables de entorno
Esta librería permite declarar el uso de variables de entorno, conversión al tipode dato requerido y sus valores predeterminados de una forma rápida y centralizada desde un archivo `.env`.

Instalación:
```bash
pip install dotenvironment
```

----

Uso:
```py
from dotenvironment import DotEnvironment
# Inicialización de una instancia
env = DotEnvironment()
# Carga DB_PORT desde el .env
DB_PORT = env.variable('DB_PORT', int)
```

En este ejemplo se declara el uso de una variable de entorno declarada en el archivo `.env` como `DB_PORT`.

----

### Prefijos
Puede usarse un prefijo para evitar colisiones en proyectos grandes.

```py
# Altamente recomendado
env = DotEnvironment('ONNYMM_')
```

Y luego buscar una variable de entorno declarada, por ejemplo, como
`ONNYMM_DB_PORT` de esta forma:
```py
# Carga ONNYMM_DB_PORT desde el .env
DB_PORT = env.variable('DB_PORT', int)
```

----

### Valores predeterminados
En caso de usar un valor predeterminado en ausencia de un valor declarado en las variables de entorno, se puede usar un tercer argumento posicional:
```py
DB_PORT = env.variable('DB_PORT', int, 5432)
```
En caso de no encontrarse un valor, se usa el valor predeterminado proporcionado, que en este caso es `5432`.

Si no se requiere usar un valor predeterminado puede dejarse el tercer argumento sin declararse o especificarse explícitamente. El uso de `...` indica que la variable es requerida y no tiene valor predeterminado:
```py
# Ambos ejemplos funcionan igual
DB_PORT = env.variable('DB_PORT', int)
DB_PORT = env.variable('DB_PORT', int, ...)
```

----

### Casteos
Al cargar una variable se declara el tipo de dato de ésta. Es importante definirlo correctamente:
```py
DB_PORT = env.variable('DB_PORT', int) # 5432
DB_PORT = env.variable('DB_PORT', str) # "5432"
```

También se pueden usar funciones para castear el valor. El valor leído desde las variables de entorno siempre se recibe como `str`:
```py
# Valores válidos como True
truthy_values = {'1', 'true', 'True', 'TRUE'}
DEBUG_MODE = env.variable('DEBUG', lambda v: v in truthy_values)
```

Se puede tipar una función sin perder información:
```py
from dotenvironment import CastFunction
# Función declarada fuera de la obtención de la variable de entorno
cast_fn: CastFunction[bool] = lambda v: v in truthy_values
DEBUG_MODE = env.variable('DEBUG', cast_fn)
```

O métodos/funciones de librerías estándar o externas que usan el valor entrante
como string:
```py
DATE = env.variable('DATE', date.fromisoformat) # Valor obligatorio
DATE = env.variable('DATE', date.fromisoformat, date.today()) # Valor predeterminado
```

----

### Debug
Para saber qué variables han sido cargadas puede imprimirse la instancia. Las
variables que no hayan sido encontradas y que tomaron valores predeterminados
se mostrarán con una leyenda de `(default)`:
```py
env = DotEnvironment('ONNYMM_')
ONNYMM_DB_USER = env.variable('DB_USER', str)
ONNYMM_DB_PORT = env.variable('DB_PORT', int, 5432)
print(env)
# DotEnvironment([
#    <ONNYMM_DB_USER[<class 'str'>]= 'root'>,
#    <ONNYMM_DB_PORT[<class 'int'>]= 5432 (default)>
# ])
```

Puedes acceder a ellas por medio de la instancia:
```py
print(env['DB_PORT']) # Puede accederse a la variable sin especificar el prefijo
print(env['ONNYMM_DB_PORT']) # O con el prefijo
```

El acceso es de solo lectura. La instancia no permite modificar valores.

O incluso comprobar si una variable fue cargada:
```py
'DB_PORT' in env
'ONNYMM_DB_PORT' in env
```
