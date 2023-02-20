import grpc
import connection_pb2
import connection_pb2_grpc

def get_connections():
    print("Getting connections...")
    # Connect to the gRPC server
    channel = grpc.insecure_channel('localhost:30051',options=[('grpc.default_authority', 'localhost:30051')])
    print("Connected to the gRPC server")
    stub = connection_pb2_grpc.ConnectionServiceStub(channel)

    # Create the request object with person_id=1
    #request = connection_pb2.ConnectionRequest(person_id=1)
    request = connection_pb2.ConnectionRequest(person_id=5, start_date="2023-02-10", end_date="2023-02-15", meters=5000)

    # Make the gRPC request to the server
    response = stub.FindContacts(request)

    # Print out the connections for person_id=1
    for connection in response.connections:
        print(f"Location: {connection.location.latitude}, {connection.location.longitude}")
        print(f"Person: {connection.person.first_name} {connection.person.last_name}\n")
    
    print("Script completed successfully.")

get_connections()

