# This class contains the user's privacy preferences (PPs)
# The PPs are modelledthrough dictionary

class Preferences:
    # PPs list
    P1 = {
        "id": "P1",           # PP ID
        "as": "service1",   # Allowed service
        "dt": ["personal", "sport", "health"],     # Data type
        "rp": 30,           # Retention period
        "ip": "socialnetwork",    # Intended purpose
        "tp": ["tp2"],        # Third parties
        "db": 5               # Data boundary
    }

    P2 = {
        "id": "P2",
        "as": "service2",
        "dt": ["personal", "position"],
        "rp": 40,
        "ip": "marketing",
        "tp": ["tp2", "tp3", "tp4"],
        "db": 4
    }

    P3 = {
        "id": "P3",
        "as": "service3",
        "dt": ["personal", "sport"],
        "rp": 15,
        "ip": "performance",
        "tp": ["tp1"],
        "db": 7
    }

    P4 = {
        "id": "P4",
        "as": "service4",
        "dt": ["health", "sport"],
        "rp": 20,
        "ip": "advertising",
        "tp": ["tp2", "tp4"],
        "db": 5
    }

    P5 = {
        "id": "P5",
        "as": "service5",
        "dt": ["personal", "health"],
        "rp": 15,
        "ip": "statistics",
        "tp": ["tp4"],
        "db": 3
    }

    P6 = {
        "id": "P6",
        "as": "service6",
        "dt": ["position", "sport"],
        "rp": 45,
        "ip": "analisys",
        "tp": ["tp2", "tp3"],
        "db": 5
    }

    P7 = {
        "id": "P7",
        "as": "service7",
        "dt": ["sport", "health"],
        "rp": 35,
        "ip": "marketing",
        "tp": ["tp1", "tp3"],
        "db": 5
    }

    P8 = {
        "id": "P8",
        "as": "service8",
        "dt": ["personal", "sport"],
        "rp": 40,
        "ip": "marketing",
        "tp": ["tp1", "tp3"],
        "db": 3
    }

    P9 = {
        "id": "P9",
        "as": "service9",
        "dt": ["health"],
        "rp": 60,
        "ip": "performance",
        "tp": ["tp1", "tp2", "tp4"],
        "db": 6
    }

    P10 = {
        "id": "P10",
        "as": "service10",
        "dt": ["personal", "sport"],
        "rp": 30,
        "ip": "socialnetwork",
        "tp": ["tp2", "tp3"],
        "db": 3
    }

    P11 = {
        "id": "P11",
        "as": "service11",
        "dt": ["personal"],
        "rp": 40,
        "ip": "socialnetwork",
        "tp": ["tp2"],
        "db": 3
    }

    P12 = {
        "id": "P12",
        "as": "service12",
        "dt": ["position", "health", "sport"],
        "rp": 20,
        "ip": "analisys",
        "tp": ["tp1"],
        "db": 3
    }

    P13 = {
        "id": "P13",
        "as": "service13",
        "dt": ["sport", "health"],
        "rp": 20,
        "ip": "marketing",
        "tp": ["tp1", "tp2", "tp3"],
        "db": 7
    }

    P14 = {
        "id": "P14",
        "as": "service14",
        "dt": ["sport", "health"],
        "rp": 30,
        "ip": "performance",
        "tp": ["tp1", "tp2"],
        "db": 7
    }

    P15 = {
        "id": "P15",
        "as": "service15",
        "dt": ["position", "health"],
        "rp": 30,
        "ip": "advertising",
        "tp": ["tp1", "tp4"],
        "db": 7
    }


    P16 = {
        "id": "P16",
        "as": "service16",
        "dt": ["personal"],
        "rp": 30,
        "ip": "statistics",
        "tp": ["tp2", "tp3"],
        "db": 7
    }

    P17 = {
        "id": "P17",
        "as": "service17",
        "dt": ["position", "sport"],
        "rp": 30,
        "ip": "advertising",
        "tp": ["tp2"],
        "db": 7
    }

    P18 = {
        "id": "P18",
        "as": "service18",
        "dt": ["position", "health"],
        "rp": 30,
        "ip": "performance",
        "tp": ["tp1", "tp2"],
        "db": 7
    }

    P19 = {
        "id": "P19",
        "as": "service19",
        "dt": ["sport", "position"],
        "rp": 45,
        "ip": "socialnetwork",
        "tp": ["tp1", "tp3"],
        "db": 7
    }

    P20 = {
        "id": "P20",
        "as": "service20",
        "dt": ["position", "health"],
        "rp": 30,
        "ip": "statistics",
        "tp": ["tp1"],
        "db": 7
    }

    P21 = {
        "id": "P21",
        "as": "service21",
        "dt": ["sport"],
        "rp": 30,
        "ip": "advertising",
        "tp": ["tp2", "tp4"],
        "db": 7
    }


    P22 = {
        "id": "P22",
        "as": "service22",
        "dt": ["position", "sport"],
        "rp": 30,
        "ip": "performance",
        "tp": ["tp1"],
        "db": 7
    }

    P23 = {
        "id": "P23",
        "as": "service23",
        "dt": ["sport"],
        "rp": 30,
        "ip": "performance",
        "tp": ["tp2", "tp4"],
        "db": 7
    }

    P24 = {
        "id": "P24",
        "as": "service24",
        "dt": ["health"],
        "rp": 30,
        "ip": "performance",
        "tp": ["tp1", "tp3"],
        "db": 7
    }

    P25 = {
        "id": "P25",
        "as": "service25",
        "dt": ["personal", "position"],
        "rp": 40,
        "ip": "performance",
        "tp": ["tp1", "tp3", "tp4"],
        "db": 7
    }

    P26 = {
        "id": "P26",
        "as": "service26",
        "dt": ["health", "personal", "position", "sport"],
        "rp": 30,
        "ip": "performance",
        "tp": ["tp2"],
        "db": 7
    }

    P27 = {
        "id": "P27",
        "as": "service27",
        "dt": ["position"],
        "rp": 40,
        "ip": "performance",
        "tp": ["tp1", "tp2"],
        "db": 7
    }

    # Requested services by the user
    requestedServices_1 = ["service1"]
    requestedServices_2 = ["service1", "service2"]
    requestedServices_5 = ["service1", "service2", "service3", "service4", "service5"]
    requestedServices_10 = ["service1", "service2", "service3", "service4", "service5","service6", "service7", "service8", "service9", "service10"]
    requestedServices_20 = ["service1", "service2", "service3", "service4", "service5","service6", "service7", "service8", "service9", "service10", "service11", "service12", "service13", "service14", "service15", "service16", "service17", "service18", "service19", "service20"]

    def getRequestedServices_1(self):
        return self.requestedServices_1
    
    def getRequestedServices_2(self):
        return self.requestedServices_2

    def getRequestedServices_5(self):
        return self.requestedServices_5

    def getRequestedServices_10(self):
        return self.requestedServices_10

    def getRequestedServices_20(self):
        return self.requestedServices_20


    def getServiceName(self, ppName):
        pp = getattr(self,ppName)
        # print("Preferences::getServiceName - service name of the preference ", pp, ": ", pp["as"])
        return pp["as"]

    def selectDataToSend(self, userPP, servicePol):
        # userPP = list
        # servicePol = list
        data_list = []
        for pp in userPP:
            for pol in servicePol:
                pref = getattr(self, pp)
                # print("Preferences::selectDataToSend - preferences: ", pref)
                # print("Preferences::selectDataToSend - Services Policy: ", pol)

                # 1. check the service
                if(pol["s"] == pref["as"]):
                    # print("\nPreferences::selectDataToSend - allowed service: ", pref["as"], " policy: ", pol["s"])
                    # 2. check the retention period
                    if(int(pol["rp"]) <= int(pref["rp"])):
                        # print("Preferences::selectDataToSend - retention period: ", pol["rp"], " <= ", pref["rp"])
                        # 3. check the intended purpose
                        if(pol["ip"] == pref["ip"]):
                            # print("Preferences::selectDataToSend - allowed intended purpose: ", pref["ip"], " policy: ", pol["ip"])
                            # 4. check the third parties
                            if(set(pol["tp"]).issubset(set(pref["tp"]))):
                                # print("Preferences::selectDataToSend - tp in PP: ", pref["tp"], " tp in Pol: ", pol["tp"])
                                # 5. check and return the type of data
                                if(set(pol["dt"]).issubset(set(pref["dt"]))):
                                    # print("Preferences::selectDataToSend - dt in PP: ", pref["dt"], " dt in Pol: ", pol["dt"])
                                    data_list.append(pol["dt"])

        return data_list
