# src/services/request_manager.py
import logging


class RequestManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RequestManager, cls).__new__(cls)
            cls._instance.clients = {}
            logging.info("RequestManager başlatıldı (Singleton).")
        return cls._instance

    def register_client(self, service_name, client_instance):
        """Belirli bir servis için bir istemci kaydeder."""
        self.clients[service_name] = client_instance
        logging.info(
            f"'{service_name}' istemcisi RequestManager'a başarıyla kaydedildi."
        )

    def get_client(self, service_name):
        """Kaydedilmiş bir istemciyi döndürür."""
        client = self.clients.get(service_name)
        if not client:
            logging.error(f"{service_name} için kayıtlı bir istemci bulunamadı.")
            raise ValueError(f"{service_name} istemcisi bulunamadı. Önce kaydedin.")
        return client
