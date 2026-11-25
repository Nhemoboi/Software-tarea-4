
from abc import abstractmethod
from entidades import EntidadBase
from excepciones import (ParametroInvalidoError, ServicioNoDisponibleError,
                         CalculoCostoError)

IVA = 0.19


class Servicio(EntidadBase):
    """Clase abstracta que modela un servicio ofrecido por Software FJ."""

    def __init__(self, nombre: str, tarifa_base: float):
        super().__init__()
        if tarifa_base <= 0:
            raise ParametroInvalidoError("La tarifa base debe ser mayor que cero.")
        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)

    def verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    @staticmethod
    def _validar_positivo(valor, nombre_param: str):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ParametroInvalidoError(f"{nombre_param} debe ser un número mayor que cero.")

    @abstractmethod
    def validar_parametros(self, duracion: float, **kwargs) -> None:
        """Valida los parámetros específicos de cada servicio."""

    @abstractmethod
    def calcular_costo(self, duracion: float, impuesto: float = IVA,
                       descuento: float = 0.0, **kwargs) -> float:
        """Calcula el costo total del servicio (versión con parámetros opcionales)."""

    def calcular_costo_simple(self, duracion: float) -> float:
        """Sobrecarga simulada: costo sin impuestos ni descuentos."""
        return self.calcular_costo(duracion, impuesto=0.0, descuento=0.0)

    def _aplicar_ajustes(self, subtotal: float, impuesto: float, descuento: float) -> float:
        if not 0 <= descuento <= 0.5:
            raise CalculoCostoError("El descuento debe estar entre 0 y 0.5 (50%).")
        if not 0 <= impuesto <= 0.3:
            raise CalculoCostoError("El impuesto debe estar entre 0 y 0.3 (30%).")
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)


class ReservaSala(Servicio):
    """Reserva de salas por hora."""

    def __init__(self, nombre: str, tarifa_hora: float, capacidad: int):
        super().__init__(nombre, tarifa_hora)
        self._capacidad = capacidad

    def validar_parametros(self, duracion: float, personas: int = 1, **kwargs):
        self._validar_positivo(duracion, "Las horas")
        if duracion > 12:
            raise ParametroInvalidoError("No se puede reservar una sala por más de 12 horas.")
        if personas > self._capacidad:
            raise ParametroInvalidoError(
                f"La sala admite {self._capacidad} personas (solicitadas: {personas}).")

    def calcular_costo(self, duracion, impuesto=IVA, descuento=0.0, personas=1, **kwargs):
        self.validar_parametros(duracion, personas=personas)
        return self._aplicar_ajustes(self.tarifa_base * duracion, impuesto, descuento)

    def describir(self):
        return (f"Sala '{self.nombre}' (#{self.id}) - ${self.tarifa_base:,.0f}/hora - "
                f"capacidad {self._capacidad}")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos por día, con seguro opcional."""

    def __init__(self, nombre: str, tarifa_dia: float):
        super().__init__(nombre, tarifa_dia)

    def validar_parametros(self, duracion: float, **kwargs):
        self._validar_positivo(duracion, "Los días")
        if duracion > 30:
            raise ParametroInvalidoError("El alquiler no puede superar 30 días.")

    def calcular_costo(self, duracion, impuesto=IVA, descuento=0.0, seguro=False, **kwargs):
        self.validar_parametros(duracion)
        subtotal = self.tarifa_base * duracion
        if seguro:
            subtotal *= 1.10 
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self):
        return f"Equipo '{self.nombre}' (#{self.id}) - ${self.tarifa_base:,.0f}/día"


class AsesoriaEspecializada(Servicio):
    """Asesoría por hora; el nivel del asesor modifica la tarifa."""

    _NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def validar_parametros(self, duracion: float, nivel: str = "junior", **kwargs):
        self._validar_positivo(duracion, "Las horas")
        if nivel not in self._NIVELES:
            raise ParametroInvalidoError(
                f"Nivel '{nivel}' no válido. Opciones: {', '.join(self._NIVELES)}.")

    def calcular_costo(self, duracion, impuesto=IVA, descuento=0.0, nivel="junior", **kwargs):
        self.validar_parametros(duracion, nivel=nivel)
        subtotal = self.tarifa_base * duracion * self._NIVELES[nivel]
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self):
        return f"Asesoría '{self.nombre}' (#{self.id}) - ${self.tarifa_base:,.0f}/hora base"
