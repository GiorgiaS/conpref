# This class interacts with deviceJava to compute the PSICA with the EdgeServer

from deviceJavaSmartwatch import DeviceJavaSmartwatch
from deviceClient import  DeviceClient

class DevicePSICASmartwatch:
    devJava = DeviceJavaSmartwatch()
    devClient = DeviceClient()

    def ECCUnbPSICA(self, algo, filter): # ifECC = boolean
        cardinality = 0
        # 1. generate key
        # 2. generate client_cipher.txt
        cipherPath = self.devJava.setCipherFile(algo)
    
        # 3. receive bloom/cuckoo file
        if(filter == "BLOOM"):
            self.devClient.askBloomFile(algo)

        # 4. send client_cipher.txt
        self.devClient.sendCipherFile(cipherPath)
        # 5. receive recv_client_cypher_2.txt
        self.devClient.askEncCliCipherFile(algo)
        # 6. decrypt the received file
        self.devJava.decryptCipher(algo)
        # 7. compute cardinality
        if(filter == "BLOOM"):
            cardinality = self.devJava.computeCardinalityBloom(algo)

        # print("DevicePSICA::ECCUnbPSICA - cardinality: ", cardinality)
        
        return cardinality

     