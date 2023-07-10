# https://stackoverflow.com/questions/60964308/call-java-method-in-python-with-jpype

import os
from socketserver import ThreadingUnixDatagramServer
import jpype


class DeviceJavaSmartwatch:
    global client
    
    def __init__(self):
        self.startJVM()
        
    def startJVM(self):
        classes = "../psica/target/classes/"
        jar1 = "../psica/lib/bcprov-jdk15on-1.70.jar"
        jar2 = "../psica/lib/bloom-filter-1.2.1.jar"
        jar3 = "../psica/lib/cuckoofilter4j-1.0.2.jar"
        jar4 = "../psica/lib/guava-31.1-jre.jar"

        if not jpype.isJVMStarted():
            jpype.startJVM("-ea", classpath=[classes, jar1, jar2, jar3, jar4], convertStrings=True)
            
        self.client = jpype.JClass("psica.Client")()

    def stopJVM(self):
        if jpype.isJVMStarted():
            jpype.shutdownJVM()

    def setCipherFile(self, algo): 
        if (algo == "ECCUnbPSICA"):
            path = self.client.ECC_PSI_Unbalanced_set_cipher()


        return path

    def setServerCipherFile(self):
        newPath = self.client.ECC_PSI_Rev_set_server_cyph()
        return newPath

    def computeCardinalityBloom(self, algo):
        if(algo == "ECCUnbPSICA"):
            cardinality = self.client.PSI_Unbalanced_cardinality_bloom()
        return cardinality

    def decryptCipher(self, algo):
        # print("DeviceJava::decryptCipher - algo: ", algo)
        if (algo == "ECCUnbPSICA"):
            self.client.ECC_PSI_Unbalanced_decrypt_cypher()
        
