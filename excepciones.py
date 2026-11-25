"""
Módulo de excepciones personalizadas.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base del sistema Software FJ."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""


class ParametroInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un parámetro de servicio (horas, días, etc.) es inválido."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando un servicio no está disponible para ser reservado."""


class CalculoCostoError(ErrorSoftwareFJ):
    """Se lanza cuando falla el cálculo del costo de un servicio."""


class ReservaError(ErrorSoftwareFJ):
    """Se lanza ante errores generales en la gestión de una reserva."""


class EstadoReservaError(ReservaError):
    """Se lanza cuando se intenta una transición de estado no permitida."""
