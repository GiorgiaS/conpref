# This class is used to communicate with the device side

import socket
import threading
from _thread import *
import pickle

from testingParameters import TestingParameters
from edgeLocator import EdgeLocator
from edgeJava import EdgeJava
from policy import Policy
from policySynthetic import PolicySynthetic


class EdgeServer(threading.Thread):
    edgeJ = EdgeJava()
    HOST = ""
    PORT = 8000

    def threaded(self, clientSocket):
        # while True:
        data = clientSocket.recv(1024)
        algo = ""
        try:
            data = pickle.loads(data)
            command = data[0]
            print("EdgeServer::threaded - pickle command:", command, " Data: ", data)
        except:
            command = data.decode('utf8')
            # print("EdgeServer::threaded - Total command:" , command, " ", type(command))
            try: 
                command_list = command.split(' ')
                command = command_list[0]
                algo = command_list[1]
                print("EdgeServer::threaded - Command:" , command," Algo: ", algo)
            except:
                command = command.split()[0]
                print("EdgeServer::threaded - Except command:", command) 

        # print("EdgeServer::threader - received data: ", data)
        if command == "EDGEID":
            self.findEdgeId(clientSocket, data[1])
        elif command == "PREFF":
            # print("edgeServer::threader - computing bloom file...")
            self.createPrefixFile(clientSocket)
        elif command == "CIPHERF":
            # print("edgeServer::threader - computing cypher file...")
            self.createCypherFile(clientSocket)
        elif command == "CCIPHERF":
            # print("edgeServer::threader - receiving client cypher file...")
            self.receiveCypherFile(clientSocket)
        elif command == "BLOOM":
            # print("edgeServer::threader - rcomputing cuckoo file...")
            self.createBloomFile(clientSocket, algo)
        elif command == "CUCKOO":
            # print("edgeServer::threader - rcomputing cuckoo file...")
            self.createCuckooFile(clientSocket, algo)
        elif command == "SERV":
            # print("EdgeServer::threader - finding policies")
            self.findServiceList(clientSocket, data[1])
        elif command == "ENCCCIPHERF":
            self.encryptCliCipherFile(clientSocket, algo)
        elif command == "KEYP":
            print("EdgeServer::threader - Key P")
            self.generateKeyP(clientSocket)
            
    def findServiceList(self, clientSocket, edgeId):
        # testPar = TestingParameters()
        # If synthetic:
        # if (testPar.getTestType() == "SYN"):
        #     policy = PolicySynthetic()
        # else: # If realistyc:
        policy = Policy()
        
        edge = "e" + edgeId
        # print("EdgeServer::findServiceList - edge-variable name: ", edge)
        services = getattr(policy, edge)
        # print("EdgeServer::findServiceList - services: ", services)
        clientSocket.sendall(pickle.dumps(services))
        clientSocket.close()

    def findEdgeId(self, clientSocket, coordinates):
        edgeLoc = EdgeLocator()
        # Get the edge ID
        edgeId = edgeLoc.getEdgeId(coordinates)
        # print("EdgeServer::threader - data to send: ", edgeId)
        clientSocket.send(str(edgeId).encode('utf8'))
        clientSocket.close()
        

    # 1. generate and send the bloom file
    def createPrefixFile(self, clientSocket):
        # generate the server_prefix_bloom file
        path = "./" + self.edgeJ.prefixFile()
        # print("EdgeServer::createBloomFile - path bloom file: ", path)
        # send the file to the device
        file = open(path, "rb")
        data = file.read()
        clientSocket.sendall(data)
        # print("Edgeserver::createBloomFile - server_prefix_bloom file sent")
        clientSocket.close()

    # 2. receive client_cipher
    def receiveCypherFile(self, clientSocket):
        with open("./server/recv_client_cipher.txt", "wb") as recFile:
            while True:
                recData = clientSocket.recv(1024)
                if not recData:
                    # print("EdgeServer::receiveCypherFile - stop receiving file")
                    break
                recFile.write(recData)
            recFile.close()
        # print("EdgeServer::receiveCypherFile - received file: recv_client_cypher")
        clientSocket.close()

    # 3-4. generate and send the server_cipher file
    def createCypherFile(self, clientSocket):
        # generate the server_cypher.txt file and send it to the device
        path = "./" + self.edgeJ.serverCyphFile()
        file = open(path, "rb")
        data = file.read()
        clientSocket.sendall(data)
        # print("EdgeServer::getSIIIntersection - path server cypher file: ", path)
        clientSocket.close()

    # 5-6. generate and send the bloom file
    def createBloomFile(self, clientSocket, algo):
        # generate the server_cypher.txt file and send it to the device
        path = "./" + self.edgeJ.serverBloomFile(algo)
        # print("EdgeServer::createBloomFile - bloom file path: ", path)
        file = open(path, "rb")
        data = file.read()
        clientSocket.sendall(data)
        # print("EdgeServer::getSIIIntersection - path server cypher file: ", path)
        clientSocket.close()
        
    def encryptCliCipherFile(self, clientSocket, algo):
        path = "./" + self.edgeJ.encryptClientCipher(algo)
        # print("EdgeServer::encryptCliCipherFile - file path: ", path)
        file = open(path, "rb")
        data = file.read()
        clientSocket.sendall(data)
        clientSocket.close()

    def generateKeyP(self, clientSocket):
        self.edgeJ.generateKeyP()
        path = "./server/keys/P.dat"
        file = open(path, "rb")
        data = file.read()
        clientSocket.sendall(data)
        clientSocket.close()

    def main(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # https://realpython.com/python-sockets/
        # only processes on the host(because HOST=localhost) is able to connect to the server
        sock.bind((self.HOST, self.PORT))
        # if HOST="" (empty string), the server will accepts connection on all IPv4 interfaces
        sock.listen()
        print("EdgeServer::main - server is listening")
        while True:
            clientSocket, addr = sock.accept()
            # print(f"EdgeServer::main - Connected by {addr}")
            start_new_thread(self.threaded, (clientSocket,))


if __name__ == "__main__":
    EdgeServer().main()
