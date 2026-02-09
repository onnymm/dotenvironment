import os
from typing import (
    Callable,
    Generic,
)
from types import EllipsisType
from ._errors import (
    EnvironmentVariableNotDefined,
    VariableNameMustBeUpperCaseError,
)
from ._types import (
    _T,
    CastFunction,
)

class _VariableConfig(Generic[_T]):

    def __init__(
        self,
        prefix: str,
        name: str,
        cast: _T | CastFunction[_T],
        default: _T | Callable[[], _T] | EllipsisType = ...
    ) -> None:

        # Se valida el nombre
        self._validate_name(name)

        # Se guardan los parámetros
        self._name = name
        self._cast = cast
        self._default = default
        self._prefix = prefix

        # Nombre de la variable de entorno
        self._variable_name = f'{self._prefix}{self._name}'
        # Se carga la variable
        self._load()

    def _validate_name(
        self,
        name: str,
    ) -> None:

        # Si el nombre provisto no está en mayúsculas
        if name != name.upper():
            # Se detiene la inicialización y se muestra el error
            raise VariableNameMustBeUpperCaseError('El nombre de variables de entorno debe ir en MAYÚSCULAS')

    def _load(
        self,
    ) -> None:

        # Obtención de la variable de entorno
        environment_value = os.environ.get(self._variable_name)
        # Si no existe ningún valor especificado en las variables de entorno...
        if environment_value is None:
            # Obtención de valor predeterminado
            value = self._get_default_var()
        # Si un valor se encontró...
        else:
            self._default_used = False
            # Se castea el valor al tipo de dato especificado
            value = self._cast_value(environment_value)

        # Se guarda el valor resuelto
        self.value = value

    def _get_default_var(
        self,
    ) -> _T:

        # Si el valor por defecto es un ellipsis
        if isinstance(self._default, EllipsisType):
            # Se indica que la variable falta
            raise EnvironmentVariableNotDefined(f'Variable {self._variable_name!r} no definida.')
        # Si el valor por defecto es definido...
        else:
            # Si el valor proporcionado es un callable...
            if callable(self._default):
                # Se ejecuta éste
                value: _T = self._default()
            # Si el valor proporcionado no es un callable...
            else:
                # Se usa éste
                value = self._default

            # Se indica que se usó el valor predeterminado
            self._default_used = True

            return value

    def _cast_value(
        self,
        variable_value: str,
    ) -> _T:

        # Se castea el valor
        value = self._cast(variable_value)

        return value

    def __repr__(
        self,
    ) -> str:

        # Obtención del nombre de la variable
        var_name = self._variable_name
        # Obtención de la representación del valor de la variable
        var_value = repr(self.value)
        # Obtención del tipo del valor de la variable
        value_type = type(self.value)
        # Leyenda de si el valor fue tomado desde el valor predeterminado
        is_default = ' (default)' if self._default_used else ''
        # Construcción de la representación
        repr_ = f'<{var_name}[{value_type}]= {var_value}{is_default}>'

        return repr_
