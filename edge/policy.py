# This file contains all the policy of the system
# Then, each edge has a list of policies to send to the device

class Policy:
    Pol1 = {
        "id": "pol1",
        "s": "service1",               # Service
        "dt": ["personal", "sport"],   # Data type
        "rp": 10,                    # Retention period
        "ip": "socialnetwork",         # Intended purpose
        "tp": ["tp2"],                 # Third parties
    }

    Pol2 = {
        "id": "pol2",
        "s": "service2",
        "dt": ["personal"],
        "rp": 5,
        "ip": "marketing",
        "tp": ["tp4", "tp2"],
    }

    Pol3 = {
        "id": "pol3",
        "s": "service3",
        "dt": ["personal", "sport"],
        "rp": 5,
        "ip": "performance",
        "tp": ["tp1"],
    }

    Pol4 = {
        "id": "pol4",
        "s": "service4",
        "dt": ["health"],
        "rp": 5,
        "ip": "advertising",
        "tp": ["tp4"],
    }

    Pol5 = {
        "id": "pol5",
        "s": "service5",
        "dt": ["health"],
        "rp": 10,
        "ip": "statistics",
        "tp": ["tp4"],
    }

    Pol6 = {
        "id": "pol6",
        "s": "service6",
        "dt": ["position"],
        "rp": 30,
        "ip": "analysis",
        "tp": ["tp2", "tp3"],
    }

    Pol7 = {
        "id": "pol7",
        "s": "service7",
        "dt": ["health", "sport"],
        "rp": 30,
        "ip": "marketing",
        "tp": ["tp1"],
    }

    Pol8 = {
        "id": "pol8",
        "s": "service8",
        "dt": ["personal"],
        "rp": 30,
        "ip": "marketing",
        "tp": ["tp1", "tp3"],
    }

    Pol9 = {
        "id": "pol9",
        "s": "service9",
        "dt": ["health"],
        "rp": 30,
        "ip": "performance",
        "tp": ["tp2", "tp4"],
    }


    Pol10 = {
        "id": "pol10",
        "s": "service10",
        "dt": ["personal", "sport"],
        "rp": 20,
        "ip": "socialnetwork",
        "tp": ["tp2", "tp3"],
    }

    Pol11 = {
        "id": "pol11",
        "s": "service11",
        "dt": ["personal"],
        "rp": 14,
        "ip": "socialnetwork",
        "tp": ["tp2"],
    }

    Pol12 = {
        "id": "pol12",
        "s": "service12",
        "dt": ["sport"],
        "rp": 15,
        "ip": "analisys",
        "tp": ["tp1"],
    }

    Pol13 = {
        "id": "pol13",
        "s": "service13",
        "dt": ["health", "sport"],
        "rp": 14,
        "ip": "marketing",
        "tp": ["tp2"],
    }

    Pol14 = {
        "id": "pol14",
        "s": "service14",
        "dt": ["sport"],
        "rp": 15,
        "ip": "performance",
        "tp": ["tp1"],
    }


    Pol15 = {
        "id": "pol15",
        "s": "service15",
        "dt": ["position"],
        "rp": 25,
        "ip": "advertising",
        "tp": ["tp4"],
    }

    Pol16 = {
        "id": "pol16",
        "s": "service16",
        "dt": ["personal"],
        "rp": 14,
        "ip": "statistics",
        "tp": ["tp2"],
    }

    Pol17 = {
        "id": "pol17",
        "s": "service17",
        "dt": ["sport"],
        "rp": 25,
        "ip": "advertising",
        "tp": ["tp2", "tp3"],
    }

    Pol18 = {
        "id": "pol18",
        "s": "service18",
        "dt": ["health"],
        "rp": 14,
        "ip": "performance",
        "tp": ["tp2"],
    }

    Pol19 = {
        "id": "pol19",
        "s": "service19",
        "dt": ["sport", "position"],
        "rp": 25,
        "ip": "socialnetwork",
        "tp": ["tp1", "tp3"],
    }


    Pol20 = {
        "id": "pol20",
        "s": "service20",
        "dt": ["health", "position"],
        "rp": 30,
        "ip": "statistics",
        "tp": ["tp1"],
    }

    Pol21 = {
        "id": "pol21",
        "s": "service21",
        "dt": ["position"],
        "rp": 16,
        "ip": "socialnetwork",
        "tp": ["tp3"],
    }

    Pol22 = {
        "id": "pol22",
        "s": "service22",
        "dt": ["sport"],
        "rp": 10,
        "ip": "statistics",
        "tp": ["tp2", "tp4"],
    }

    Pol23 = {
        "id": "pol23",
        "s": "service23",
        "dt": ["health"],
        "rp": 20,
        "ip": "performance",
        "tp": ["tp2"],
    }

    Pol24 = {
        "id": "pol24",
        "s": "service24",
        "dt": ["personal"],
        "rp": 25,
        "ip": "socialnetwork",
        "tp": ["tp1"],
    }

    # Never enforced (?)
    Pol25 = {
        "id": "pol25",
        "s": "service25",
        "dt": ["health", "position"],
        "rp": 70,
        "ip": "statistics",
        "tp": ["tp2", "tp3"],
    }

    # to have 50 services in total
    Pol26 = {
        "id": "pol26",
        "s": "service26",               # Service
        "dt": ["personal", "sport"],   # Data type
        "rp": 10,                    # Retention period
        "ip": "socialnetwork",         # Intended purpose
        "tp": ["tp2"],                 # Third parties
    }

    # Assign to each edge a list of policies
    # The list's name corresponds to the edge ID
    e9021482 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e303639 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e301486 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e300527 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e303294 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e300527 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9012011 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e300959 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e50121 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e11624 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e304041 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e10006883 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e49920 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9015103 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9007953 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e305938 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e502092 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9011234 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e304023 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e304024 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9019139 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9004237 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9027333 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e10003239 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e10006792 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e304022 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e49873 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e10008857 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9013096 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9022769 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e10008863 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e304991 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e10006881 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e10003261 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9007233 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9018513 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9012209 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9019139 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9020993 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9026935 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e11573 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e134454 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e10009566 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e132242 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]