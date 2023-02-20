from concurrent import futures
import grpc
import connection_pb2
import connection_pb2_grpc


class ConnectionsService(connection_pb2_grpc.ConnectionServiceServicer):

    def FindContacts(self, request, context):
        connections = [
            connection_pb2.Connection(
                location=connection_pb2.Location(
                    id=1,
                    person_id=1,
                    longitude='123.456',
                    latitude='789.012',
                    creation_time='2022-02-20T10:00:00.000Z'
                ),
                person=connection_pb2.Person(
                    id=1,
                    last_name='Doe',
                    first_name='John',
                    company_name='Example Company'
                )
            )
        ]
        return connection_pb2.ConnectionResponse(connections=connections)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    connection_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionsService(), server)
    server.add_insecure_port('[::]:30051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
