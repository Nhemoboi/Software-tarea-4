"""
Clase abstracta base para las entidades generales del sistema.
"""
from abc import ABC, abstractmethod
import itertools


class EntidadBase(ABC):
    """Entidad general: todo objeto del sistema tiene un identificador único."""

    _contador = itertools.count(1)

    def __init__(self):
        self._id = next(EntidadBase._contador)

    @property
    def id(self) -> int:
        """Identificador de solo lectura (encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible de la entidad."""

    def __str__(self) -> str:
        return self.describir()
