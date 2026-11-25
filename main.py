"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas
"""
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import ErrorSoftwareFJ
from logger_config import obtener_logger

log = obtener_logger()

clientes, servicios, reservas = [], [], []


def simulacion(numero: int, titulo: str):
    print(f"\n=== Simulación {numero}: {titulo} ===")
    log.info("--- Simulación %s: %s ---", numero, titulo)


def main():
    sala = ReservaSala("Sala Innovación", 80000, capacidad=10)
    equipo = AlquilerEquipo("Portátil Gamer", 60000)
    asesoria = AsesoriaEspecializada("Asesoría en Python", 100000)
    servicios.extend([sala, equipo, asesoria])
    for s in servicios:
        print(s)

    simulacion(1, "Registro de cliente válido (VÁLIDA)")
    try:
        c1 = Cliente("Nehemías Pérez", "1100223344", "nehemias@correo.com", "3001234567")
        clientes.append(c1)
        print(c1)
    except ErrorSoftwareFJ as e:
        log.error("Error: %s", e)

    simulacion(2, "Cliente con correo inválido (INVÁLIDA)")
    try:
        Cliente("Ana Gómez", "123456789", "ana-correo.com", "3101234567")
    except ErrorSoftwareFJ as e:
        log.error("Cliente rechazado: %s", e)

    simulacion(3, "Cliente con documento no numérico (INVÁLIDA)")
    try:
        Cliente("Luis Mora", "ABC123", "luis@correo.com", "3201234567")
    except ErrorSoftwareFJ as e:
        log.error("Cliente rechazado: %s", e)

    simulacion(4, "Segundo cliente válido (VÁLIDA)")
    try:
        c2 = Cliente("María Torres", "52123456", "maria@empresa.co", "3157654321")
        clientes.append(c2)
        print(c2)
    except ErrorSoftwareFJ as e:
        log.error("Error: %s", e)

    c1, c2 = clientes[0], clientes[1]

    simulacion(5, "Reserva de sala 3 horas con descuento (VÁLIDA)")
    try:
        r1 = Reserva(c1, sala, 3, descuento=0.10, personas=6)
        r1.confirmar()
        reservas.append(r1)
        print(r1)
    except ErrorSoftwareFJ as e:
        log.error("Error: %s", e)

    simulacion(6, "Sala con exceso de personas (INVÁLIDA)")
    try:
        r = Reserva(c1, sala, 2, personas=25)
        r.confirmar()
    except ErrorSoftwareFJ as e:
        log.error("Reserva fallida: %s | Causa: %r", e, e.__cause__)

    simulacion(7, "Alquiler de equipo 5 días con seguro (VÁLIDA)")
    try:
        r2 = Reserva(c2, equipo, 5, seguro=True)
        r2.confirmar()
        r2.procesar()
        reservas.append(r2)
        print(r2)
    except ErrorSoftwareFJ as e:
        log.error("Error: %s", e)

    simulacion(8, "Alquiler con días negativos (INVÁLIDA)")
    try:
        r = Reserva(c2, equipo, -2)
        r.confirmar()
    except ErrorSoftwareFJ as e:
        log.error("Reserva fallida: %s | Causa: %r", e, e.__cause__)

    simulacion(9, "Asesoría nivel experto 2 horas (VÁLIDA)")
    try:
        r3 = Reserva(c1, asesoria, 2, nivel="experto")
        r3.confirmar()
        reservas.append(r3)
        print(r3)
    except ErrorSoftwareFJ as e:
        log.error("Error: %s", e)

    simulacion(10, "Asesoría con nivel inexistente (INVÁLIDA)")
    try:
        r = Reserva(c1, asesoria, 1, nivel="maestro")
        r.confirmar()
    except ErrorSoftwareFJ as e:
        log.error("Reserva fallida: %s | Causa: %r", e, e.__cause__)

    simulacion(11, "Procesar una reserva cancelada (INVÁLIDA)")
    try:
        r3.cancelar()
        r3.procesar()
    except ErrorSoftwareFJ as e:
        log.error("Operación rechazada: %s", e)

    simulacion(12, "Reserva de servicio no disponible (INVÁLIDA)")
    try:
        sala.disponible = False
        Reserva(c2, sala, 1)
    except ErrorSoftwareFJ as e:
        log.error("Reserva rechazada: %s", e)
    finally:
        sala.disponible = True 

    print("\n=== Resumen de reservas ===")
    for r in reservas:
        print(r)
    log.info("Fin de las simulaciones. El sistema continuó operando sin interrupciones.")


if __name__ == "__main__":
    main()
