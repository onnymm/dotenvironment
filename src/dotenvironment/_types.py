from typing import (
    Callable,
    TypeVar,
)

# Genérico
_T = TypeVar('_T')

# Representación de función para castear
CastFunction = Callable[[str], _T]
"""
### Función de casteo
Este tipo de dato ayuda a tipar una función para proporcionar al método
`variable` de una instancia de `DotEnvironment`. Este tipo de función siempre
recibe una cadena de texto como valor entrante:

Uso:
>>> # Valores válidos como True
>>> truthy_values = {'1', 'true', 'True', 'TRUE'}
>>> 
>>> # Función lambda tipada
>>> fn: CastFunction[bool] = lambda v: v in truthy_values
>>>
>>> # Esto es lo mismo
>>> def fn(v: str) -> bool:
>>>     return  v in truthy_values
>>>
>>> DEBUG_MODE = env.variable('DEBUG', fn, False)
"""
