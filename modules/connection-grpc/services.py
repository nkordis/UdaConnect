from concurrent import futures
import grpc
import connection_pb2
import connection_pb2_grpc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config_by_name
from models import Location, Person
import sys


class ConnectionsService(connection_pb2_grpc.ConnectionServiceServicer):

    def __init__(self, config_name = 'dev'):
        print(f"Initializing ConnectionsService with config: {config_name}", file=sys.stderr)
        self.config = config_by_name[config_name]
        self.engine = create_engine(self.config.SQLALCHEMY_DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def FindContacts(self, request, context):
        print("Received FindContacts request...", file=sys.stderr)
        with self.get_session() as session:
            locations = (
                session.query(Location, Person)
                .join(Person)
                .all()
            )
        connections = []
        for location, person in locations:
            connection = connection_pb2.Connection(
                location=connection_pb2.Location(
                    id=location.id,
                    person_id=location.person_id,
                    longitude=location.longitude,
                    latitude=location.latitude,
                    creation_time=location.creation_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                ),
                person=connection_pb2.Person(
                    id=person.id,
                    last_name=person.last_name,
                    first_name=person.first_name,
                    company_name=person.company_name,
                ),
            )
            connections.append(connection)
        print(f"Returning {len(connections)} connections", file=sys.stderr)
        return connection_pb2.ConnectionResponse(connections=connections)


def serve(config_name='dev'):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    connection_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionsService(), server)
    server.add_insecure_port('[::]:30051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
