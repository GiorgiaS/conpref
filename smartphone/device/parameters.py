class Parameters:
    # From the college
    userCoordinates = {
        "lat": -38.79295833709386,
        "long": 145.9609198134932,
    }

    currentPPs = []
    serviceList = []

    # Parameters for the PSI-CA Java Library
    PSICAAlg = "ECCUnbPSICA"
    filter = "BLOOM" 

    # Getters
    def getUserCoordinates(self):
        return self.userCoordinates

    def getCurrentPPs(self):
        return self.currentPPs

    def getPSICAAlg(self):
        return self.PSICAAlg

    def getFilter(self):
        return self.filter

    def getServiceList(self):
        return self.serviceList

    # Setters
    def setUserCoordinates(self, lat, long):
        self.userCoordinates.update({"lat": lat})
        self.userCoordinates.update({"long": long})

    def setCurrentPPs(self, ppList):
        self.currentPPs = ppList

    def setServiceList(self, services):
        self.serviceList = services
