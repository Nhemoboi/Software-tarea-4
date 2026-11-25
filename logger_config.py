"""
Configuración del registro de eventos (logs).
Los eventos y errores se guardan en logs/software_fj.log.
"""
import logging
import os

RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(RUTA_LOGS, exist_ok=True)
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")


def obtener_logger(nombre: str = "software_fj") -> logging.Logger:
    """Devuelve un logger configurado."""
    logger = logging.getLogger(nombre)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(module)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    archivo = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    archivo.setFormatter(formato)
    consola = logging.StreamHandler()
    consola.setLevel(logging.INFO)
    consola.setFormatter(formato)
    logger.addHandler(archivo)
    logger.addHandler(consola)
    return logger
