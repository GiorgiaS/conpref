from http import server
import jpype


class EdgeJava:
    global server

    def __init__(self):
        classes = "../psica/target/classes/"
        jar1 = "../psica/lib/bcprov-jdk15on-1.70.jar"
        jar2 = "../psica/lib/bloom-filter-1.2.1.jar"
        jar3 = "../psica/lib/cuckoofilter4j-1.0.2.jar"
        jar4 = "../psica/lib/guava-31.1-jre.jar"

        if not jpype.isJVMStarted():
            jpype.startJVM(
                "-ea", classpath=[classes, jar1, jar2, jar3, jar4], convertStrings=True)

        self.server = jpype.JClass("psica.Server")()

    # It generates the key, starts the ECC_PSI:Rev method and greates the server_prefix_bloom file
    def prefixFile(self):
        path = self.server.ECC_PSI_Rev_gen_prefix()
        print("EdgeJava::prefixBloomFile - file path: ", path)
        return path

    def serverCyphFile(self):
        path = self.server.ECC_PSI_Rev_gen_serv_cyph()
        return path

    def serverCyphFile(self):
        path = self.server.ECC_PSI_Rev_gen_serv_cyph()
        return path

    def serverCuckooFile(self, algo):
        if (algo == "revECCUnbPSICA"):
            path = self.server.ECC_PSI_Rev_gen_cuckoo()
        elif (algo == "ECCUnbPSICA"):
            path = self.server.ECC_PSI_Unbalanced_gen_cuckoo()
        else: # algo == "UnbPSICA"
            path = self.server.PSI_Unbalanced_gen_cuckoo()
        return path

    def serverBloomFile(self, algo):
        print("EdgeJava::serverBloomFile - algo: ", algo)
        if (algo == "revECCUnbPSICA"):
            path = self.server.ECC_PSI_Rev_gen_bloom()
        elif (algo == "ECCUnbPSICA"):
            path = self.server.ECC_PSI_Unbalanced_gen_bloom()
        else: # algo == "UnbPSICA"
            path = self.server.PSI_Unbalanced_gen_bloom()
        return path

    def encryptClientCipher(self, algo):
        if (algo == "ECCUnbPSICA"):
            flag = True
            i= 0
            while flag:
                try:
                    path = self.server.ECC_PSI_Unbalanced_encrypt_client_cipher()
                    flag = False
                except:
                    i = i+1
                    print("EdgeJava::encryptClientCipher - number of error: ", i)

        else:
            path = self.server.PSI_Unbalanced_encrypt_client_cipher()
        return path
    
    def generateKeyP(self):
        print("EdgeJava:generateKeyP - begins")
        self.server.generateKey()

    def stopJVM(self):
        if jpype.isJVMStarted():
            jpype.shutdownJVM()
