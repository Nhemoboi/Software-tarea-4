"""
Clase Cliente con validaciones y encapsulación.
"""
import re
from entidades import EntidadBase
from excepciones import ClienteInvalidoError


class Cliente(EntidadBase):
    """Representa a un cliente de Software FJ."""

    _PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

    def __init__(self, nombre: str, documento: str, correo: str, telefono: str):
        super().__init__()
       
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono


    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str):
        if not isinstance(valor, str) or not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError(
                "El documento debe ser numérico de 6 a 12 dígitos."
            )
        self._documento = valor

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not isinstance(valor, str) or not self._PATRON_CORREO.match(valor):
            raise ClienteInvalidoError(f"Correo electrónico inválido: {valor!r}.")
        self._correo = valor

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not isinstance(valor, str) or not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError("El teléfono debe tener 10 dígitos numéricos.")
        self._telefono = valor

    def describir(self) -> str:
        return (f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | "
                f"{self.correo} | Tel: {self.telefono}")
