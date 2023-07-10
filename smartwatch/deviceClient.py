import socket
import pickle
import time 

from deviceJavaSmartwatch import DeviceJavaSmartwatch


# This class is used to interact with the edge
class DeviceClient:
    #HOST = "localhost"
    # for testing with device-edge
    #HOST = "127.0.0.1"
    HOST = "193.206.183.38"
    PORT = 8000

    def askKeyP(self):
        data = "KEYP"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # print("DeviceClient::askKeyP - sending data: ", data)
            sock.connect((self.HOST, self.PORT))
            sock.sendall(data.encode('utf8')) # to serialize (transform data in bytes)

            # 1.2. receive KeyP file from the edge
            # print("DeviceCient::askKeyP - waiting for file")
            with open("./client/keys/P.dat", "wb") as recFile:
                while True:
                    recData = sock.recv(1024)
                    if not recData:
                        # print("DeviceCient::askPrefixFilter - stop receiving file")
                        break
                    recFile.write(recData)
                recFile.close()
            # print("DeviceCient::askPrefixFilter - received file: recv_prefix_filter")
            # print("DeviceClient::askPrefixFilter - bloom file at: ", devJava.setBloomFile())
    

    def askServices(self, edgeId):
        data= "SERV", edgeId
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.HOST, self.PORT))
            sock.sendall(pickle.dumps(data)) # to serialize (transform data in bytes)
            
            # If test is realistic:
            # data = sock.recv(1024)
            # If test is synthetic:
            # data = sock.recv(8000)
            # sock.close()
            # services = pickle.loads(data)
            data = []
            while True:
                packet = sock.recv(4096)
                if not packet: break
                data.append(packet)
            services = pickle.loads(b"".join(data))
            sock.close()
            # print("DeviceClient::askServices - list of policies: ", services )
            return services

    def sendCoordinates(self, coordinates):
        data = "EDGEID", coordinates
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.HOST, self.PORT))
            except:
                print("Server connection refused from client hostname: ", socket.gethostname(), " and IP address: ", socket.gethostbyname(socket.gethostname()))
            sock.sendall(pickle.dumps(data)) # to serialize (transform data in bytes)
            data = sock.recv(1024)
            sock.close()
            edgeId = data.decode('utf8')
        # print("DeviceClient::sendCoordinates - received edge ID: ", edgeId)
        return edgeId

    # Send the PSICA request to the edgeServer
    def askPrefixFilter(self):
        #devJava = DeviceJava()
        # 1. sends the request to the edge and waits for the server_prefix_bloom_file
        data = "PREFF"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # print("DeviceClient::askPrefixFilter - sending data: ", data)
            sock.connect((self.HOST, self.PORT))
            sock.sendall(data.encode('utf8')) # to serialize (transform data in bytes)

            # 1.2. receive bloom file from the edge
            # print("DeviceCient::askPrefixFilter - waiting for file")
            with open("./client/recv_prefix_filter", "wb") as recFile:
                while True:
                    recData = sock.recv(1024)
                    if not recData:
                        # print("DeviceCient::askPrefixFilter - stop receiving file")
                        break
                    recFile.write(recData)
                recFile.close()
            # print("DeviceCient::askPrefixFilter - received file: recv_prefix_filter")
            # print("DeviceClient::askPrefixFilter - bloom file at: ", devJava.setBloomFile())
    
            
            # newPath = devJava.setCipherFile()


            # print("DeviceClient::askPrefixFilter - new client_cypher path: ", newPath)
            
        sock.close()
        
        
    def sendCipherFile(self, path):
        data = "CCIPHERF"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.HOST, self.PORT))
            sock.sendall(data.encode('utf8'))
            # print("DeviceClient::sendCypherFile - file path to send: ", path)
            # To send the first the command (string) and then the file
            time.sleep(0.1)
            # send the file
            file = open(path, "rb")
            data = file.read()
            sock.sendall(data)
            # print("DeviceClient::sendCypherFile - server_prefix_bloom file sent")

        sock.close()

    # 4. receive recv_server_ciper
    def askCipherFile(self):
        # 1. sends the request to the edge and waits for the server_prefix_bloom_file
        data = "CIPHERF"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # print("DeviceClient::askCypherFile - sending data: ", data)
            sock.connect((self.HOST, self.PORT))
            sock.sendall(data.encode('utf8')) # to serialize (transform data in bytes)
            # 2. receive the file from the edge
            # print("DeviceCient::computeIntersection - waiting for file")

            with open("./client/recv_server_cipher.txt", "wb") as recFile:
                while True:
                    recData = sock.recv(1024)
                    if not recData:
                        # print("DeviceCient::computeIntersection - stop receiving file")
                        break
                    recFile.write(recData)
                recFile.close()
            # print("DeviceCient::computeIntersection - received file: recv_prefix_filter")

        sock.close()
        # return newPath
        
    def askBloomFile(self, algo):
        data = "BLOOM " + str(algo)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # print("DeviceClient::askBloomFile - sending data: ", data)
            sock.connect((self.HOST, self.PORT))
            sock.sendall(data.encode('utf8')) # to serialize (transform data in bytes)
            # 2. receive the file from the edge
            # print("DeviceCient::askBloomFile - waiting for file")
            with open("./client/client_bloom", "wb") as recFile:
                while True:
                    recData = sock.recv(1024)
                    if not recData:
                        # print("DeviceCient::askBloomFile - stop receiving file")
                        break
                    recFile.write(recData)
                recFile.close()
            # print("DeviceCient::askBloomFile - received file: client_bloom")
        sock.close()

    def askEncCliCipherFile(self, algo):
        data = "ENCCCIPHERF " + str(algo)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # print("DeviceClient::computeIntersection - sending data: ", data)
            sock.connect((self.HOST, self.PORT))
            sock.sendall(data.encode('utf8')) # to serialize (transform data in bytes)
            # 2. receive the file from the edge
            # print("DeviceCient::computeIntersection - waiting for file")

            with open("./client/recv_client_cipher_2.txt", "wb") as recFile:
                while True:
                    recData = sock.recv(1024)
                    if not recData:
                        # print("DeviceCient::computeIntersection - stop receiving file")
                        break
                    recFile.write(recData)
                recFile.close()
            # print("DeviceCient::computeIntersection - received file: recv_prefix_filter")
        sock.close()
