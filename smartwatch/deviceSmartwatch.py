# This class simulates the user life
# It's the main class device/user-side

import hashlib
import os
import time
from pygeodesy.sphericalNvector import LatLon

from deviceClient import DeviceClient
from userPath import UserPath
from parameters import Parameters
from context import Context
from location import Location
from deviceJavaSmartwatch import DeviceJavaSmartwatch
from preferences import Preferences
from devicePSICASmartwatch import DevicePSICASmartwatch
from ppParser import PPParser

class DeviceSmartwatch:
    client = DeviceClient()
    param = Parameters()
    ctx = Context()
    loc = Location()
    path = UserPath()
    devJ = DeviceJavaSmartwatch()
    pref = Preferences()
    devPSICA = DevicePSICASmartwatch()
    ppPars = PPParser()

    # This method:
    # - updates the user's coordinates;
    # - checks whether there is a change in the area, pi and/or edgeID.
    #   If yes, it starts the computation of the new PSICA and to get the new PPs

    def changePosition(self, coordinates, testOutputFilename, ppFilename, requestedServices):
        newServices = []
        newPPs = []
        selectDataStartTime = 0
        startTime = time.time()
        
        # print("Device::changePosition - updating coordinates: ",
        #   coordinates[0], coordinates[1])
        self.param.setUserCoordinates(coordinates[0], coordinates[1])

        # Check new area, new PI and new EdgeId
        print("\nDevice::changePosition - location changes")
        edgeId = self.client.sendCoordinates(coordinates)
        newArea = self.detectArea()
        newPI = self.detectPI()

        # If the edge changes:
        # 1. update the new context
        # 2. ask the services it offers (and the policies)
        if(self.ctx.getEdgeId() != edgeId):
                print("device::changePosition - new edgeId: ",
                      edgeId, "old edgeId: ", self.ctx.getEdgeId())
                # print("device::changePosition - edgeId before: ", self.ctx.getNewEdgeId(), " new EdgeId: ", edgeId)
                self.ctx.setEdgeId(edgeId)
                newserviceList = self.acquireServices(edgeId)
                self.param.setServiceList(newserviceList)
                # Get the list of the services that the user want to exploit and that are provided by the edge
                for service in newserviceList:
                    # print("device::changePosition - service name in the serviceList: ", service["s"] )
                    if(requestedServices == 1):
                        reqServices = self.pref.getRequestedServices_1()
                    elif(requestedServices == 2):
                        reqServices = self.pref.getRequestedServices_2()
                    elif(requestedServices == 10):
                        reqServices = self.pref.getRequestedServices_10()
                    if(service["s"] in reqServices): # To check
                        newServices.append(service)
                self.param.setServiceList(newServices)

        # print("device::changePosition - I'm updating with new coordinates: ", coordinates)
        # update PPs if something changes
        if(self.ctx.getOldContext()!= self.ctx.getNewContext()):
            print("Device::changePosition - old/new area: ", self.ctx.getOldArea(), "/", self.ctx.getNewArea())
            print("Device::changePosition - old/new PI: ", self.ctx.getOldPi(), "/", self.ctx.getNewPi())
            print("Device::changePosition - old/new EdgeID: ", self.ctx.getEdgeId(), "/", edgeId)

            if(newArea and not newPI): # If the area changes but not the PI the PP enforcement is not necessary      
                                       # This is for the test case, since the selection of the areas and of the PIs is handmade and there can be a PI in two or more different areas.   
                self.ctx.updateOldContext()
                return 


            newPPs = self.getPPsToEnforce(ppFilename, self.param.getServiceList(), testOutputFilename)

            # update parameters
            self.param.setCurrentPPs(newPPs)

            selectDataStartTime = time.time()
            data = self.pref.selectDataToSend(newPPs, self.param.getServiceList())
            selectDataStopTime = time.time()

            print("Device::changePosition - data to share: ", data)

            # Keep track of the execution time
            # print("Device::changePosition - time required to compute the overal algorithm: ", time.time() - startTime, "seconds")
            file = open("%s.txt" %(testOutputFilename), "a")
            if(selectDataStartTime != 0):
                file.write("\n\tData selection: " + str("{:.4f}".format(
                    selectDataStopTime - selectDataStartTime)) + "seconds")
            file.write("\n\t" + self.ctx.getNewArea() + " " + self.ctx.getNewPi() +
                    " all computation: " + str("{:.4f}".format(time.time() - startTime)) + "seconds\n")
            # file.write("\n\tTime to extract which data to share: " + str("{:.4f}".format(time.time() - PPstartTime)))
            file.close()

            # update old ctx with the newest
            self.ctx.updateOldContext()
            return True
        else:
            print("Device::changePosition - No context changes")
            return False


    def acquireServices(self, edgeId):
        # Ask the policies list to the new edge
        return self.client.askServices(edgeId)


    # This method returns the current user's area, based on the coordinates
    # It updatest the newContext

    def detectArea(self):
        currentPosition = LatLon(self.param.getUserCoordinates()[
            "lat"], self.param.getUserCoordinates()["long"])
        areas = self.loc.getAreas()
        for area in areas:
            a = LatLon(area["tl"][0], area["tl"][1]), LatLon(area["tr"][0], area["tr"][1]),  LatLon(
                area["br"][0], area["br"][1]),  LatLon(area["bl"][0], area["bl"][1])
            if currentPosition.isEnclosedBy(a) and area["name"] != self.ctx.getOldArea():
                print("Device::detectArea - the new user's area: ",
                      area["name"])
                # update user context
                self.ctx.setNewArea(area["name"])
                return True
        return False


    # This method returns the current user's pi, based on the coordinates
    # It updates the newContext
    def detectPI(self):
        currentPosition = LatLon(self.param.getUserCoordinates()[
                                 "lat"], self.param.getUserCoordinates()["long"])
        pis = self.loc.getPIs()
        for pi in pis:
            p = LatLon(pi["tl"][0], pi["tl"][1]), LatLon(pi["tr"][0], pi["tr"][1]),  LatLon(
                pi["br"][0], pi["br"][1]),  LatLon(pi["bl"][0], pi["bl"][1])
            if currentPosition.isEnclosedBy(p) and pi["name"] != self.ctx.getOldPi():
                print("Device::detectPI - the new user's pi: ", pi["name"])
                # update user context
                self.ctx.setNewPi(pi["name"])
                return True
        return False




    # With this method:
    # 1. the device extracts all the PP-SI sub-trees in the contextual_preferences.xml file;
    # 2. for each PP, if service name in PP equals a service name in newServices, the device computes the PSICA
    def getPPsToEnforce(self, ppFilename, newServices, testOutputFilename):

        if os.path.exists("%s.txt" %(testOutputFilename)):
            resultFileMode = 'a'  
        else:
            # Create the folder (and the file) if do not exist
            resultFileMode = 'w+'
            resultFileFolder = testOutputFilename.rsplit('/',1)[0]
            if not os.path.isdir(resultFileFolder):
                os.makedirs("%s" %(resultFileFolder))

        newPPs = []
        # Get the PP list.
        # It does not return the list of PP-SI sub-trees as it is useless in this testing
        ppList = self.ppPars.extractPPList(self.ctx, ppFilename)
        for pp in ppList:
            # print("Device::getPPsToEnforce - current pp from \'sub-tree\': ", pp)
            for service in newServices:
                ppName = self.pref.getServiceName(pp)
                # print("Device:getPPsToEnforce - service name in PP: ", ppName)
                if(ppName == service["s"]): # if yes, compute the PSICA
                    socialIgnore = self.ppPars.extractSI(self.ctx, pp, ppFilename)
                    # Get the user list and threshold from socialIgnore
                    userList = socialIgnore["siList"]
                    threshold = socialIgnore["threshold"]
                    # Get the intersection if there are some name in the SI list
                    cardinality = 0
                    startTime = time.time()
                    if len(userList): # If there are users in the socialIgnore list
                        # Write the user list in a .txt file
                        file = open("./client/social_ignore.txt", "w")
                        for user in userList:
                            u = str(int(hashlib.sha256(user.encode(
                                'utf-8')).hexdigest(), 16) % 10**10)
                            # print("Device::getPPsToEnforce - user to be written: ", user, ": ", u)
                            file.write(u + "\n")
                        file.close()

                        stTime = time.time()

                        # Compute the PSICA
                        # print("Device::getPPsToEnforce - PSICA ALG: ", self.param.getPSICAAlg())
                        if (self.param.getPSICAAlg() == "ECCUnbPSICA"):
                            cardinality = self.devPSICA.ECCUnbPSICA(
                                self.param.getPSICAAlg(), self.param.getFilter())
            
                        # To handle the situation where the user does not specify any element in the SI list
                        # if(cardinality > hInt):
                        #     hInt = cardinality

                        # It should be useless now because we have only 1 user list
                        file = open("%s.txt" %(testOutputFilename), resultFileMode)
                        file.write("\n\t" + self.ctx.getNewArea() + " " + self.ctx.getNewPi(
                        ) + " PSICA for service \"" + ppName + "\"; with list of size " + str(len(userList)) + ": " + str("{:.4f}".format(time.time() - stTime)) + "seconds")
                        file.close()
                    # print("Device:getPPsToEnforce - cardinality: ", cardinality)

                    if(cardinality < int(threshold)):
                        newPPs.append(pp)
                        print("Device:getPPsToEnforce - pp to enforce: ", pp)

                    # Store all PSICA time results
                    # print("Device::AcquirePPs - time required to compute all the PSICA: ", time.time() - startTime, "seconds")
                    file = open("%s.txt" %(testOutputFilename), resultFileMode)
                    file.write("\n\t" + self.ctx.getNewArea() + " " + self.ctx.getNewPi(
                    ) + " PSICA for all services: " + str("{:.4f}".format(time.time() - startTime)) + "seconds")
                    file.close()

        return newPPs
      
