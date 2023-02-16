import grpc
import time
from app.udaconnect import connection_pb2
from app.udaconnect import connection_pb2_grpc

from concurrent import futures
from datetime import datetime

from app.udaconnect.models import Connection
from app.udaconnect.schemas import ConnectionSchema
from app.udaconnect.services import ConnectionService
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

class ConnectionServicer(connection_pb2_grpc.ConnectionServiceServicer):
    def FindContacts(self, request, context):
        start_date = datetime.strptime(request.start_date, DATE_FORMAT)
        end_date = datetime.strptime(request.end_date, DATE_FORMAT)
        distance = request.meters

        results = ConnectionService.find_contacts(
            person_id=request.person_id,
            start_date=start_date,
             end_date=end_date,
            meters=distance,
        )
        connections = []
        for result in results:
            connection = connection_pb2.Connection(
                id=result.id,
                person_id=result.person_id,
                contact_id=result.contact_id,
                latitude=result.latitude,
                longitude=result.longitude,
                creation_time=result.creation_time,
            )
            connections.append(connection)
        return connection_pb2.ConnectionResponse(connections=connections)

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
connection_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionServicer(), server)



print("Server starting on port 5000...")
server.add_insecure_port("[::]:5000")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)