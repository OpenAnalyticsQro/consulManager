# FACTURA_CLI
from ConsulManager.Logger import logger, CONSUL_MANAGER_LOG_NAME
import logging

GRPC_MANAGER_NAME = "FACT"

log = logging.getLogger(f'{CONSUL_MANAGER_LOG_NAME}.{GRPC_MANAGER_NAME}')
log.setLevel(logging.DEBUG)




