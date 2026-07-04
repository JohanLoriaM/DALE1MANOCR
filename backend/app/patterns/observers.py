import logging
from ..interfaces.IObserver import IObserver

logging.basicConfig(
    filename='sistema.log',
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)


class AuditLogObserver(IObserver):
    def update(self, event_type: str, data: dict):
        if event_type == "NUEVA_INSCRIPCION":
            logging.info(
                f"Usuario ID {data.get('id_usuario')} inscrito en Proyecto ID {data.get('id_proyecto')}")


class EmailNotificationObserver(IObserver):
    def update(self, event_type: str, data: dict):
        if event_type == "NUEVA_INSCRIPCION":
            logging.info(
                f"Simulando envío de correo de confirmación al usuario ID {data.get('id_usuario')}")
