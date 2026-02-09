import dotenv
from typing import (
    Any,
    Callable,
)
from types import EllipsisType
from ._errors import PrefixMustBeUpperCaseError
from ._types import (
    _T,
    CastFunction,
)
from ._variable_config import _VariableConfig

# Carga de entorno
dotenv.load_dotenv()

class DotEnvironment():
    """
    ## Variables de entorno
    Esta clase permite declarar el uso de variables de entorno, conversión al tipo
    de dato requerido y sus valores predeterminados de una forma rápida y
    centralizada.

    Uso:
    >>> dotenvironment import DotEnvironment
    >>> # Inicialización de una instancia
    >>> env = DotEnvironment()
    >>> # Carga DB_PORT desde el .env
    >>> DB_PORT = env.variable('DB_PORT', int)

    En este ejemplo se declara el uso de una variable de entorno declarada en el
    archivo `.env` como `DB_PORT`.

    ****
    ### Prefijos
    Puede usarse un prefijo para evitar colisiones en proyectos grandes.
    >>> # Altamente recomendado
    >>> env = DotEnvironment('ONNYMM_')

    Y luego buscar una variable de entorno declarada, por ejemplo, como
    `ONNYMM_DB_PORT` de esta forma:
    >>> # Carga ONNYMM_DB_PORT desde el .env
    >>> DB_PORT = env.variable('DB_PORT', int)

    ****
    ### Valores predeterminados
    En caso de usar un valor predeterminado en ausencia de un valor declarado en
    las variables de entorno, se puede usar un tercer argumento posicional:
    >>> DB_PORT = env.variable('DB_PORT', int, 5432)

    En caso de no encontrarse un valor, se usa el valor predeterminado
    proporcionado, que en este caso es `5432`.

    También puede proporcionarse una función como valor predeterminado. Si el valor
    predeterminado es callable, éste será ejecutado únicamente cuando la variable
    de entorno no esté definida:
    >>> from datetime import date
    >>> DEFAULT_DATE = env.variable('DATE', datetime.fromisoformat, date.today)

    Esto puede ser útil en casos donde obtener un valor predeterminado requiere
    cómputo complejo o lento innecesario de ejecutar si en realidad sí fue provisto
    un valor predeterminado:
    >>> def my_complex_computing_here() -> CustomObject:
    >>>     # some complex computing algorythms
    >>> MY_VALUE = env.variable('MY_VALUE', CustomObject, my_complex_computing_here)

    Si no se requiere usar un valor predeterminado puede dejarse el tercer argumento
    sin declararse o especificarse explícitamente. El uso de `...` indica que la
    variable es requerida y no tiene valor predeterminado:
    >>> # Ambos ejemplos funcionan igual
    >>> DB_PORT = env.variable('DB_PORT', int)
    >>> DB_PORT = env.variable('DB_PORT', int, ...)

    ****
    ### Casteos
    Al cargar una variable se declara el tipo de dato de ésta. Es importante
    definirlo correctamente:
    >>> DB_PORT = env.variable('DB_PORT', int) # 5432
    >>> DB_PORT = env.variable('DB_PORT', str) # "5432"

    También se pueden usar funciones para castear el valor. El valor leído desde
    las variables de entorno siempre se recibe como `str`:
    >>> # Valores válidos como True
    >>> truthy_values = {'1', 'true', 'True', 'TRUE'}
    >>> DEBUG_MODE = env.variable('DEBUG', lambda v: v in truthy_values)

    Se puede tipar una función sin perder información:
    >>> from dotenvironment import CastFunction
    >>> # Función declarada fuera de la obtención de la variable de entorno
    >>> cast_fn: CastFunction[bool] = lambda v: v in truthy_values
    >>> DEBUG_MODE = env.variable('DEBUG', cast_fn)

    O métodos/funciones de librerías estándar o externas que usan el valor entrante
    como string:
    >>> DATE = env.variable('DATE', date.fromisoformat) # Valor obligatorio
    >>> DATE = env.variable('DATE', date.fromisoformat, date.today()) # Valor predeterminado

    ****
    ### Debug
    Para saber qué variables han sido cargadas puede imprimirse la instancia. Las
    variables que no hayan sido encontradas y que tomaron valores predeterminados
    se mostrarán con una leyenda de `(default)`:
    >>> env = DotEnvironment('ONNYMM_')
    >>> ONNYMM_DB_USER = env.variable('DB_USER', str)
    >>> ONNYMM_DB_PORT = env.variable('DB_PORT', int, 5432)
    >>> print(env)
    >>> # DotEnvironment([
    >>> #    <ONNYMM_DB_USER[<class 'str'>]= 'root'>,
    >>> #    <ONNYMM_DB_PORT[<class 'int'>]= 5432 (default)>
    >>> # ])

    Puedes acceder a ellas por medio de la instancia:
    >>> print(env['DB_PORT']) # Puede accederse a la variable sin especificar el prefijo
    >>> print(env['ONNYMM_DB_PORT']) # O con el prefijo

    El acceso es de solo lectura. La instancia no permite modificar valores.

    O incluso comprobar si una variable fue cargada:
    >>> 'DB_PORT' in env
    >>> 'ONNYMM_DB_PORT' in env
    """
    _stored_variables: dict[str, _VariableConfig]

    def __init__(
        self,
        prefix: str = '',
    ) -> None:

        # Validación de prefijo
        self._validate_prefix(prefix)

        # Se inicializan valores
        self._prefix = prefix
        self._stored_variables = {}

    def variable(
        self,
        name: str,
        cast: _T | CastFunction[_T],
        default: _T | Callable[[], _T] | EllipsisType = ...,
    ) -> _T:
        """
        ## Nueva variable desde el entorno
        Este método de instancia declara el uso de una variable de entorno junto con un
        tipo de dato con el que se realizará el casteo del valor y opcionalmente un
        valor predeterminado en caso no haberse proporcionado un valor para la variable
        en el entorno.

        Uso:
        >>> # Carga DB_PORT desde el .env
        >>> DB_PORT = env.variable('DB_PORT', int)

        En este ejemplo se declara el uso de una variable de entorno declarada en el
        archivo `.env` como `DB_PORT`.

        ****
        ### Prefijos
        Puede usarse un prefijo para evitar colisiones en proyectos grandes.
        >>> # Altamente recomendado
        >>> env = DotEnvironment('ONNYMM_')

        Y luego buscar una variable de entorno declarada, por ejemplo, como
        `ONNYMM_DB_PORT` de esta forma:
        >>> # Carga ONNYMM_DB_PORT desde el .env
        >>> DB_PORT = env.variable('DB_PORT', int)

        ****
        ### Valores predeterminados
        En caso de usar un valor predeterminado en ausencia de un valor declarado en
        las variables de entorno, se puede usar un tercer argumento posicional:
        >>> DB_PORT = env.variable('DB_PORT', int, 5432)

        En caso de no encontrarse un valor, se usa el valor predeterminado
        proporcionado, que en este caso es `5432`.

        También puede proporcionarse una función como valor predeterminado. Si el valor
        predeterminado es callable, éste será ejecutado únicamente cuando la variable
        de entorno no esté definida:
        >>> from datetime import date
        >>> DEFAULT_DATE = env.variable('DATE', datetime.fromisoformat, date.today)

        Esto puede ser útil en casos donde obtener un valor predeterminado requiere
        cómputo complejo o lento innecesario de ejecutar si en realidad sí fue provisto
        un valor predeterminado:
        >>> def my_complex_computing_here() -> CustomObject:
        >>>     # some complex computing algorythms
        >>> MY_VALUE = env.variable('MY_VALUE', CustomObject, my_complex_computing_here)

        Si no se requiere usar un valor predeterminado puede dejarse el tercer argumento
        sin declararse o especificarse explícitamente. El uso de `...` indica que la
        variable es requerida y no tiene valor predeterminado:
        >>> # Ambos ejemplos funcionan igual
        >>> DB_PORT = env.variable('DB_PORT', int)
        >>> DB_PORT = env.variable('DB_PORT', int, ...)

        ****
        ### Casteos
        Al cargar una variable se declara el tipo de dato de ésta. Es importante
        definirlo correctamente:
        >>> DB_PORT = env.variable('DB_PORT', int) # 5432
        >>> DB_PORT = env.variable('DB_PORT', str) # "5432"

        También se pueden usar funciones para castear el valor. El valor leído desde
        las variables de entorno siempre se recibe como `str`:
        >>> # Valores válidos como True
        >>> truthy_values = {'1', 'true', 'True', 'TRUE'}
        >>> DEBUG_MODE = env.variable('DEBUG', lambda v: v in truthy_values)

        Se puede tipar una función sin perder información:
        >>> from dotenvironment import CastFunction
        >>> # Función declarada fuera de la obtención de la variable de entorno
        >>> cast_fn: CastFunction[bool] = lambda v: v in truthy_values
        >>> DEBUG_MODE = env.variable('DEBUG', cast_fn)

        O métodos/funciones de librerías estándar o externas que usan el valor entrante
        como string:
        >>> DATE = env.variable('DATE', date.fromisoformat) # Valor obligatorio
        >>> DATE = env.variable('DATE', date.fromisoformat, date.today()) # Valor predeterminado
        """

        # Carga de la variable
        variable = _VariableConfig(self._prefix, name, cast, default)
        # Datos de la variable
        self._stored_variables[f'{self._prefix}{name}'] = variable

        return variable.value

    def _validate_prefix(
        self,
        prefix: str,
    ) -> None:

        # Si el prefijo provisto no está en mayúsculas
        if prefix != prefix.upper():
            # Se detiene la inicialización y se muestra el error
            raise PrefixMustBeUpperCaseError('El prefijo de nombre de variables de entorno debe ir en MAYÚSCULAS')

    def __repr__(
        self,
    ) -> str:

        # Obtención de las variables obtenidas desde el env
        stored_values = self._stored_variables.values()
        # Creación de un resumen
        summary = [var for var in stored_values]

        return f'DotEnvironment({summary})'

    def __getitem__(
        self,
        key: str,
    ) -> Any:

        # Si la llave proporcionada se encuentra en las variables obtenidas...
        if key in self._stored_variables:
            # Se retorna el valor de ésta
            return self._stored_variables[key].value

        # Construcción de la llave usando el prefijo
        prefixed = f'{self._prefix}{key}'
        # Si la llave con prefijo se encuentra en las variables obtenidas...
        if prefixed in self._stored_variables:
            # Se retorna el valor de ésta
            return self._stored_variables[prefixed].value

        # De no encontrarse se lanza un error
        return KeyError(f'La variable {key!r} no está definida en este entorno.')

    def __contains__(
        self,
        key: str,
    ) -> bool:

        # La llave proporcionada existe
        key_exists = key in self._stored_variables
        # La llave con prefijo existe
        prefixed_exists = f'{self._prefix}{key}' in self._stored_variables

        # Retorno de la evaluación
        return key_exists or prefixed_exists
