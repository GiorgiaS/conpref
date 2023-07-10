# This file contains all the policy of the system
# Then, each edge has a list of policies to send to the device

class PolicySynthetic:
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

    # Pol27 = {
    #     "id": "pol27",
    #     "s": "service27",
    #     "dt": ["personal"],
    #     "rp": 5,
    #     "ip": "marketing",
    #     "tp": ["tp4", "tp2"],
    # }

    # Pol28 = {
    #     "id": "pol28",
    #     "s": "service28",
    #     "dt": ["personal", "sport"],
    #     "rp": 5,
    #     "ip": "performance",
    #     "tp": ["tp1"],
    # }

    # Pol29 = {
    #     "id": "pol29",
    #     "s": "service29",
    #     "dt": ["health"],
    #     "rp": 5,
    #     "ip": "advertising",
    #     "tp": ["tp4"],
    # }

    # # Never enforced (?)
    # Pol30 = {
    #     "id": "pol30",
    #     "s": "service30",
    #     "dt": ["health"],
    #     "rp": 40,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol31 = {
    #     "id": "pol31",
    #     "s": "service31",
    #     "dt": ["position"],
    #     "rp": 30,
    #     "ip": "analysis",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol32 = {
    #     "id": "pol32",
    #     "s": "service32",
    #     "dt": ["health", "sport"],
    #     "rp": 30,
    #     "ip": "analysis",
    #     "tp": ["tp1"],
    # }

    # Pol33 = {
    #     "id": "pol33",
    #     "s": "service2",
    #     "dt": ["personal"],
    #     "rp": 30,
    #     "ip": "marketing",
    #     "tp": ["tp1", "tp3"],
    # }

    # Pol34 = {
    #     "id": "pol34",
    #     "s": "service2",
    #     "dt": ["health"],
    #     "rp": 30,
    #     "ip": "performance",
    #     "tp": ["tp2", "tp4"],
    # }

    # # Never enforced (?)
    # Pol35 = {
    #     "id": "pol35",
    #     "s": "service2",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol36 = {
    #     "id": "pol36",
    #     "s": "service3",
    #     "dt": ["personal"],
    #     "rp": 14,
    #     "ip": "statistics",
    #     "tp": ["tp2"],
    # }

    # Pol37 = {
    #     "id": "pol37",
    #     "s": "service3",
    #     "dt": ["sport"],
    #     "rp": 15,
    #     "ip": "analisys",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol38 = {
    #     "id": "pol38",
    #     "s": "service3",
    #     "dt": ["health", "sport"],
    #     "rp": 14,
    #     "ip": "marketing",
    #     "tp": ["tp2"],
    # }

    # Pol39 = {
    #     "id": "pol39",
    #     "s": "service3",
    #     "dt": ["sport"],
    #     "rp": 15,
    #     "ip": "performance",
    #     "tp": ["tp1"],
    # }

    # # Never enfoced (?)
    # Pol40 = {
    #     "id": "pol40",
    #     "s": "service3",
    #     "dt": ["position"],
    #     "rp": 70,
    #     "ip": "advertising",
    #     "tp": ["tp4"],
    # }

    # Pol41 = {
    #     "id": "pol41",
    #     "s": "service4",
    #     "dt": ["personal"],
    #     "rp": 14,
    #     "ip": "statistics",
    #     "tp": ["tp2"],
    # }

    # Pol42 = {
    #     "id": "pol42",
    #     "s": "service4",
    #     "dt": ["sport"],
    #     "rp": 25,
    #     "ip": "marketing",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol43 = {
    #     "id": "pol43",
    #     "s": "service4",
    #     "dt": ["health"],
    #     "rp": 14,
    #     "ip": "performance",
    #     "tp": ["tp2"],
    # }

    # Pol44 = {
    #     "id": "pol44",
    #     "s": "service4",
    #     "dt": ["sport", "position"],
    #     "rp": 25,
    #     "ip": "socialnetwork",
    #     "tp": ["tp1", "tp3"],
    # }

    # # Never enforced (?)
    # Pol45 = {
    #     "id": "pol45",
    #     "s": "service4",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol46 = {
    #     "id": "pol46",
    #     "s": "service5",
    #     "dt": ["position"],
    #     "rp": 16,
    #     "ip": "socialnetwork",
    #     "tp": ["tp3"],
    # }

    # Pol47 = {
    #     "id": "pol47",
    #     "s": "service5",
    #     "dt": ["sport"],
    #     "rp": 10,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp4"],
    # }

    # Pol48 = {
    #     "id": "pol48",
    #     "s": "service5",
    #     "dt": ["health"],
    #     "rp": 20,
    #     "ip": "performance",
    #     "tp": ["tp2"],
    # }

    # Pol49 = {
    #     "id": "pol49",
    #     "s": "service5",
    #     "dt": ["personal"],
    #     "rp": 25,
    #     "ip": "socialnetwork",
    #     "tp": ["tp1"],
    # }

    # # Never enforced (?)
    # Pol50 = {
    #     "id": "pol50",
    #     "s": "service5",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }


    # # To get 100 policies
    # Pol51 = {
    #     "id": "pol51",
    #     "s": "service5",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }
    # Pol52 = {
    #     "id": "pol52",
    #     "s": "service5",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }
    # Pol53 = {
    #     "id": "pol53",
    #     "s": "service5",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }
    # Pol54 = {
    #     "id": "pol54",
    #     "s": "service5",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }
    # Pol55 = {
    #     "id": "pol55",
    #     "s": "service5",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }
    # Pol56 = {
    #     "id": "pol56",
    #     "s": "service5",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }
    # Pol57 = {
    #     "id": "pol57",
    #     "s": "service5",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }
    # Pol58 = {
    #     "id": "pol58",
    #     "s": "service5",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }
    # Pol59 = {
    #     "id": "pol50",
    #     "s": "service5",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol60 = {
    #     "id": "pol60",
    #     "s": "service5",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol61 = {
    #     "id": "pol61",
    #     "s": "service3",
    #     "dt": ["personal"],
    #     "rp": 14,
    #     "ip": "statistics",
    #     "tp": ["tp2"],
    # }

    # Pol62 = {
    #     "id": "pol62",
    #     "s": "service3",
    #     "dt": ["sport"],
    #     "rp": 15,
    #     "ip": "analisys",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol63 = {
    #     "id": "pol63",
    #     "s": "service3",
    #     "dt": ["health", "sport"],
    #     "rp": 14,
    #     "ip": "marketing",
    #     "tp": ["tp2"],
    # }

    # Pol64 = {
    #     "id": "pol64",
    #     "s": "service3",
    #     "dt": ["sport"],
    #     "rp": 15,
    #     "ip": "performance",
    #     "tp": ["tp1"],
    # }

    # # Never enfoced (?)
    # Pol65 = {
    #     "id": "pol65",
    #     "s": "service3",
    #     "dt": ["position"],
    #     "rp": 70,
    #     "ip": "advertising",
    #     "tp": ["tp4"],
    # }

    # Pol66 = {
    #     "id": "pol66",
    #     "s": "service4",
    #     "dt": ["personal"],
    #     "rp": 14,
    #     "ip": "statistics",
    #     "tp": ["tp2"],
    # }

    # Pol67 = {
    #     "id": "pol67",
    #     "s": "service4",
    #     "dt": ["sport"],
    #     "rp": 25,
    #     "ip": "marketing",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol68 = {
    #     "id": "pol68",
    #     "s": "service4",
    #     "dt": ["health"],
    #     "rp": 14,
    #     "ip": "performance",
    #     "tp": ["tp2"],
    # }

    # Pol69 = {
    #     "id": "pol69",
    #     "s": "service4",
    #     "dt": ["sport", "position"],
    #     "rp": 25,
    #     "ip": "socialnetwork",
    #     "tp": ["tp1", "tp3"],
    # }

    # # Never enforced (?)
    # Pol70 = {
    #     "id": "pol70",
    #     "s": "service4",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol71 = {
    #     "id": "pol71",
    #     "s": "service5",
    #     "dt": ["position"],
    #     "rp": 16,
    #     "ip": "socialnetwork",
    #     "tp": ["tp3"],
    # }

    # Pol72 = {
    #     "id": "pol72",
    #     "s": "service5",
    #     "dt": ["sport"],
    #     "rp": 10,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp4"],
    # }

    # Pol73 = {
    #     "id": "pol73",
    #     "s": "service5",
    #     "dt": ["health"],
    #     "rp": 20,
    #     "ip": "performance",
    #     "tp": ["tp2"],
    # }

    # Pol74 = {
    #     "id": "pol74",
    #     "s": "service5",
    #     "dt": ["personal"],
    #     "rp": 25,
    #     "ip": "socialnetwork",
    #     "tp": ["tp1"],
    # }

    # # Never enforced (?)
    # Pol75 = {
    #     "id": "pol75",
    #     "s": "service5",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }

    # # to have 50 services in total
    # Pol76 = {
    #     "id": "pol76",
    #     "s": "service1",               # Service
    #     "dt": ["personal", "sport"],   # Data type
    #     "rp": 10,                    # Retention period
    #     "ip": "socialnetwork",         # Intended purpose
    #     "tp": ["tp2"],                 # Third parties
    # }

    # Pol77 = {
    #     "id": "pol77",
    #     "s": "service1",
    #     "dt": ["personal"],
    #     "rp": 5,
    #     "ip": "marketing",
    #     "tp": ["tp4", "tp2"],
    # }

    # Pol78 = {
    #     "id": "pol78",
    #     "s": "service1",
    #     "dt": ["personal", "sport"],
    #     "rp": 5,
    #     "ip": "performance",
    #     "tp": ["tp1"],
    # }

    # Pol79 = {
    #     "id": "pol79",
    #     "s": "service1",
    #     "dt": ["health"],
    #     "rp": 5,
    #     "ip": "advertising",
    #     "tp": ["tp4"],
    # }

    # # Never enforced (?)
    # Pol80 = {
    #     "id": "pol80",
    #     "s": "service1",
    #     "dt": ["health"],
    #     "rp": 40,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol81 = {
    #     "id": "pol81",
    #     "s": "service2",
    #     "dt": ["position"],
    #     "rp": 30,
    #     "ip": "analysis",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol82 = {
    #     "id": "pol82",
    #     "s": "service2",
    #     "dt": ["health", "sport"],
    #     "rp": 30,
    #     "ip": "analysis",
    #     "tp": ["tp1"],
    # }

    # Pol83 = {
    #     "id": "pol83",
    #     "s": "service2",
    #     "dt": ["personal"],
    #     "rp": 30,
    #     "ip": "marketing",
    #     "tp": ["tp1", "tp3"],
    # }

    # Pol84 = {
    #     "id": "pol84",
    #     "s": "service2",
    #     "dt": ["health"],
    #     "rp": 30,
    #     "ip": "performance",
    #     "tp": ["tp2", "tp4"],
    # }

    # # Never enforced (?)
    # Pol85 = {
    #     "id": "pol85",
    #     "s": "service2",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol86 = {
    #     "id": "pol86",
    #     "s": "service3",
    #     "dt": ["personal"],
    #     "rp": 14,
    #     "ip": "statistics",
    #     "tp": ["tp2"],
    # }

    # Pol87 = {
    #     "id": "pol87",
    #     "s": "service3",
    #     "dt": ["sport"],
    #     "rp": 15,
    #     "ip": "analisys",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol88 = {
    #     "id": "pol88",
    #     "s": "service3",
    #     "dt": ["health", "sport"],
    #     "rp": 14,
    #     "ip": "marketing",
    #     "tp": ["tp2"],
    # }

    # Pol89 = {
    #     "id": "pol89",
    #     "s": "service3",
    #     "dt": ["sport"],
    #     "rp": 15,
    #     "ip": "performance",
    #     "tp": ["tp1"],
    # }

    # # Never enfoced (?)
    # Pol90 = {
    #     "id": "pol90",
    #     "s": "service3",
    #     "dt": ["position"],
    #     "rp": 70,
    #     "ip": "advertising",
    #     "tp": ["tp4"],
    # }

    # Pol91 = {
    #     "id": "pol91",
    #     "s": "service2",
    #     "dt": ["position"],
    #     "rp": 30,
    #     "ip": "analysis",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol92 = {
    #     "id": "pol92",
    #     "s": "service2",
    #     "dt": ["health", "sport"],
    #     "rp": 30,
    #     "ip": "analysis",
    #     "tp": ["tp1"],
    # }

    # Pol93 = {
    #     "id": "pol93",
    #     "s": "service2",
    #     "dt": ["personal"],
    #     "rp": 30,
    #     "ip": "marketing",
    #     "tp": ["tp1", "tp3"],
    # }

    # Pol94 = {
    #     "id": "pol94",
    #     "s": "service2",
    #     "dt": ["health"],
    #     "rp": 30,
    #     "ip": "performance",
    #     "tp": ["tp2", "tp4"],
    # }

    # # Never enforced (?)
    # Pol95 = {
    #     "id": "pol95",
    #     "s": "service2",
    #     "dt": ["health", "position"],
    #     "rp": 70,
    #     "ip": "statistics",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol96 = {
    #     "id": "pol96",
    #     "s": "service3",
    #     "dt": ["personal"],
    #     "rp": 14,
    #     "ip": "statistics",
    #     "tp": ["tp2"],
    # }

    # Pol97 = {
    #     "id": "pol97",
    #     "s": "service3",
    #     "dt": ["sport"],
    #     "rp": 15,
    #     "ip": "analisys",
    #     "tp": ["tp2", "tp3"],
    # }

    # Pol98 = {
    #     "id": "pol98",
    #     "s": "service3",
    #     "dt": ["health", "sport"],
    #     "rp": 14,
    #     "ip": "marketing",
    #     "tp": ["tp2"],
    # }

    # Pol99 = {
    #     "id": "pol99",
    #     "s": "service3",
    #     "dt": ["sport"],
    #     "rp": 15,
    #     "ip": "performance",
    #     "tp": ["tp1"],
    # }

    # # Never enfoced (?)
    # Pol100 = {
    #     "id": "pol100",
    #     "s": "service3",
    #     "dt": ["position"],
    #     "rp": 70,
    #     "ip": "advertising",
    #     "tp": ["tp4"],
    # }

    # Assign to each edge a list of policies
    # The list's name corresponds to the edge ID
    # For synthetic tests we only neeed 2 peers

    # 10 services offered
    e304041 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]
    e9019139 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12, Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20]

    # 20 ser

    # 50 services offered
    # e304041 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12,
    #            Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20, Pol21, Pol22, Pol23,
    #            Pol24, Pol25, Pol26, Pol27, Pol28, Pol29, Pol30, Pol31, Pol32, Pol33, Pol34,
    #            Pol35, Pol36, Pol37, Pol38, Pol39, Pol40, Pol41, Pol42, Pol43, Pol44, Pol45,
    #            Pol46, Pol47, Pol48, Pol49, Pol50]

    # e9019139 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12,
    #             Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20, Pol21, Pol22, Pol23,
    #             Pol24, Pol25, Pol26, Pol27, Pol28, Pol29, Pol30, Pol31, Pol32, Pol33, Pol34,
    #             Pol35, Pol36, Pol37, Pol38, Pol39, Pol40, Pol41, Pol42, Pol43, Pol44, Pol45,
    #             Pol46, Pol47, Pol48, Pol49, Pol50]

    # 100 services offered
    # e304041 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12,
    #            Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20, Pol21, Pol22, Pol23,
    #            Pol24, Pol25, Pol26, Pol27, Pol28, Pol29, Pol30, Pol31, Pol32, Pol33, Pol34,
    #            Pol35, Pol36, Pol37, Pol38, Pol39, Pol40, Pol41, Pol42, Pol43, Pol44, Pol45,
    #            Pol46, Pol47, Pol48, Pol49, Pol50, Pol51, Pol52, Pol53, Pol53, Pol55, Pol56,
    #            Pol57, Pol58, Pol59, Pol60, Pol61, Pol62, Pol63, Pol64, Pol65, Pol66, Pol67,
    #            Pol68, Pol69, Pol70, Pol71, Pol72, Pol73, Pol74, Pol75, Pol76, Pol77, Pol78,
    #            Pol79, Pol80, Pol81, Pol82, Pol83, Pol84, Pol85, Pol86, Pol87, Pol88, Pol89,
    #            Pol90, Pol91, Pol92, Pol93, Pol94, Pol95, Pol96, Pol97, Pol98, Pol99, Pol100]

    # e9019139 = [Pol1, Pol2, Pol3, Pol4, Pol5, Pol6, Pol7, Pol8, Pol9, Pol10, Pol11, Pol12,
    #            Pol13, Pol14, Pol15, Pol16, Pol17, Pol18, Pol19, Pol20, Pol21, Pol22, Pol23,
    #            Pol24, Pol25, Pol26, Pol27, Pol28, Pol29, Pol30, Pol31, Pol32, Pol33, Pol34,
    #            Pol35, Pol36, Pol37, Pol38, Pol39, Pol40, Pol41, Pol42, Pol43, Pol44, Pol45,
    #            Pol46, Pol47, Pol48, Pol49, Pol50, Pol51, Pol52, Pol53, Pol53, Pol55, Pol56,
    #            Pol57, Pol58, Pol59, Pol60, Pol61, Pol62, Pol63, Pol64, Pol65, Pol66, Pol67,
    #            Pol68, Pol69, Pol70, Pol71, Pol72, Pol73, Pol74, Pol75, Pol76, Pol77, Pol78,
    #            Pol79, Pol80, Pol81, Pol82, Pol83, Pol84, Pol85, Pol86, Pol87, Pol88, Pol89,
    #            Pol90, Pol91, Pol92, Pol93, Pol94, Pol95, Pol96, Pol97, Pol98, Pol99, Pol100]