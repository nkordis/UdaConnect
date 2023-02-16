from app.udaconnect.models import Connection
from app.udaconnect.schemas import ConnectionSchema

from . import connection_pb2
from . import connection_pb2_grpc


def register_routes(api, app, root="api/v2"):
    from app.udaconnect.controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")
