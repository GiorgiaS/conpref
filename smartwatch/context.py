# This class tracks the information related to the old and new contexts.
# Furthermore, it allows to update the newContext with the new changes, and the oldContext.

class Context:
    oldContext = {
        # "edgeId": 0,
        "situation": "common",
        "city": "melbourne",
        "area": "",
        "pi": "",
        "currentTime": "weekday",
        "currentActivity": "walking",
        "siTh": 0
    }

    newContext = {
        # "edgeId": 0,
        "situation": "common",
        "city": "melbourne",
        "area": "college",
        "pi": "ormond college",
        "currentTime": "weekday",
        "currentActivity": "walking",
        "siTh": 0
    }

    edgeId = 0

    # Getters

    def getOldContext(self):
        return self.oldContext

    def getOldEdgeId(self):
        return self.oldContext["edgeId"]

    def getOldArea(self):
        return self.oldContext["area"]

    def getOldPi(self):
        return self.oldContext["pi"]

    def getNewContext(self):
        return self.newContext

    def getNewSituation(self):
        return self.newContext["situation"]

    def getNewCity(self):
        return self.newContext["city"]

    def getNewArea(self):
        return self.newContext["area"]

    def getNewPi(self):
        return self.newContext["pi"]

    def getNewCurrentTime(self):
        return self.newContext["currentTime"]

    def getNewActivity(self):
        return self.newContext["currentActivity"]

    def getNewSiTh(self):
        return self.newContext["siTh"]

    def getEdgeId(self):
        return self.edgeId

    # Setters

    def setNewSituation(self, situation):
        self.newContext.update({"situation": situation})

    def setNewCity(self, city):
        self.newContext.update({"city": city})

    def setNewArea(self, area):
        self.newContext.update({"area": area})

    def setNewPi(self, pi):
        self.newContext.update({"pi": pi})

    def setNewTime(self, time):
        self.newContext.update({"currentTime": time})

    def setNewActivity(self, activity):
        self.newContext.update({"currentActivity": activity})

    def setNewIntersection(self, intersection):
        self.newContext.update({"siTh": intersection})

    def setEdgeId(self, id):
        self.edgeId = id

    # Update the old context with the newly one

    def updateOldContext(self):
      #  self.oldContext.update({"edgeId": self.newContext["edgeId"]})
        self.oldContext.update({"situation": self.newContext["situation"]})
        self.oldContext.update({"city": self.newContext["city"]})
        self.oldContext.update({"area": self.newContext["area"]})
        self.oldContext.update({"pi": self.newContext["pi"]})
        self.oldContext.update({"currentTime": self.newContext["currentTime"]})
        self.oldContext.update(
            {"currentActivity": self.newContext["currentActivity"]})
