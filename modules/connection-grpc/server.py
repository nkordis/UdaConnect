import grpc
from concurrent import futures
import connection_pb2
import connection_pb2_grpc
from services import ConnectionsService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    connection_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionsService(), server)
    server.add_insecure_port('[::]:30051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
