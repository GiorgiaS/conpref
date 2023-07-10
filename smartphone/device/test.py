import os
import time

from parameters import Parameters
from context import Context
from location import Location
from device import Device
from userPath import UserPath
from deviceJava import DeviceJava


class Test:

    par = Parameters()
    ctx = Context()
    loc = Location()
    device = Device()
    path = UserPath()
    devJ = DeviceJava()
    
    # realisticTest parameters:
    # - testOutputFilename: .txt containing time log
    # - speed: denotes the user's movement speed (m/s);
    #         we use this value to decide how often trigger the changePosition() method
    # - cpsFilename: the .xml file containing the user CPs
    # - requestedServices: the numer of services requested by the user. It is related to preferences.py
    def realisticTest(self, testOutputFilename, speed, cpsFilename, requestedServices):
        
        # Send coordinates to start the JVM. Do not consider this computation in the tests.
        self.device.changePosition(
                    [-37.804283200082864, 144.9602075309404], testOutputFilename, cpsFilename, requestedServices)
        print("Test::realisticTest - starting JVM")
        
        filePath = open("./userPath_first.txt", "r")
        firstPath = []
        for line in filePath:
            point = line
            pl = list(map(float,point.split()))
            firstPath.append(pl)   
        print("Test::realisticTest - first path: ", firstPath)

        # The path P1 is 950m
        # timeInterval = (distance/number_of_coordinates)/speed
        timeInterval = (950/len(firstPath))/speed
        print("Test::realisticTest - len path: ", len(firstPath))
        print("Test:realisticTest - time interval: ", timeInterval)

        # to store some information from the testing phase
        negative = 0
        totRemainingTime = 0
        totComputationTime = 0
        totComputation = 0
        
        # Create new file to store the time
        file = open("./%s.txt" % (testOutputFilename), "w")
        file.write("First Path: College+University Areas \nFrom Ormond College Main Building to School of Chemistry (Melbourne University)\n")
        file.write("Time Interval: " + str(timeInterval) + "\n")
        file.close()
               
   
        overallTimeStart = time.time()
        
        for coord in firstPath:
            print("\n\nTest:realisticTest - coord: ", coord)
            file = open("./%s.txt" % (testOutputFilename), "a")
            timeStart = time.time()

            computation = self.device.changePosition(coord, testOutputFilename, cpsFilename, requestedServices)
            if(computation):
                compTime = (time.time() - timeStart)
                remTime = timeInterval - compTime
                file.write(
                    "\tRemaining time: " + str(remTime) + "\n")
                if(remTime < 0 ):
                    negative = negative + 1
                totRemainingTime = totRemainingTime + remTime
                totComputationTime = totComputationTime + compTime
                totComputation = totComputation + 1
                file.close()

        file = open("./%s.txt" % (testOutputFilename), "a")
        file.write("Total time for First Path: " + str("{:.4f}".format(time.time() - overallTimeStart)) + "seconds\n")
        file.write("Total negative results: " + str(negative) + "\n")
        file.write("Number of computation executed: " + str(totComputation) + "\n")
        try:
            file.write("Average remaining time: " + str(totRemainingTime/totComputation) + "\n")
            file.write("Average computation time: " + str(totComputationTime/totComputation))
        except:
            print("Test:realisticTest - no computation: ", totComputation)

        # Third path
        # 550m
        filePath = open("./userPath_third.txt", "r")
        thirdPath = []
        for line in filePath:
            point = line
            pl = list(map(float,point.split()))
            thirdPath.append(pl)   
        print(thirdPath)
           
        timeInterval = (550/len(thirdPath))/speed
        overallTimeStart = time.time()
        
        negative = 0
        totRemainingTime = 0
        totComputationTime = 0
        totComputation = 0

        file.write("\n\nThird Path: Melbourne CBD area\nFrom Melbourne State Library Forecourt to Tipo 00 Restaurant")
        file.write("\nTime Interval: " + str(timeInterval) + "\n")
        file.close()
        
        for coord in thirdPath:
            print("\n\nTest:realisticTest - coord: ", coord)
            file = open("./%s.txt" % (testOutputFilename), "a")
            timeStart = time.time()
            computation = self.device.changePosition(coord, testOutputFilename, cpsFilename, requestedServices)
            if(computation):
                compTime = (time.time() - timeStart)
                remTime = timeInterval - compTime
                file.write(
                    "\tRemaining time: " + str(remTime) + "\n")
                if(remTime < 0 ):
                    negative = negative + 1
                totRemainingTime = totRemainingTime + remTime
                totComputationTime = totComputationTime + compTime
                totComputation = totComputation + 1
                file.close()
                
        file = open("./%s.txt" % (testOutputFilename), "a")
        file.write("Total time for First Path: " + str("{:.4f}".format(time.time() - overallTimeStart)) + "seconds\n")
        file.write("Total negative results: " + str(negative) + "\n")
        file.write("Number of computation executed: " + str(totComputation) + "\n")
        try:
            file.write("Average remaining time: " + str(totRemainingTime/totComputation) + "\n")
            file.write("Average computation time: " + str(totComputationTime/totComputation))
        except:
            print("Test:realisticTest - no computation: ", totComputation)
        
        file.close()



    # syntheticTest parameters:
    # - density = how many edge per km2. Since we test over 1km, the density is the number of edge a user connects to along his (synthetic) path.
    #             Thus, rep (repetition) = density.
    # - testOutputFilename: .txt containing time log
    # - speed: denotes the user's movement speed (m/s);
    #         we use this value to decide how often trigger the changePosition() method
    # - cpsFilename: the .xml file containing the user CPs
    # - requestedServices: the numer of services requested by the user. It is related to preferences.py
    def syntheticTest(self, density, testOutputFilename, speed, cpsFilename, requestedServices):
        # Send coordinates to start the JVM. Do not consider this computation in the tests.
        self.device.changePosition(
                    [-37.79713182162259, 144.96755215516572], testOutputFilename, cpsFilename, requestedServices)
        print("test::syntheticTest - JVM started")
        
        
        # alternate 2 (random) coordinates to enforce every time the context change
        # use a flag (pos) to do that
        pos = 0

        # Walking speed = 125cm/s for a women between 40/49 years.
        # Electric scooter speed = 30km/h = 833cm/s
        # timeInterval: computes every when the user changes context (seconds)
        #               (area / number_of_edges_per_km2) / walking_speed
        #               Where "area" is 1km => 1000m
        timeInterval = (1000 / density) / speed

        totTime = 0
        totComputationTime = 0
        totRemainingTime = 0

        print("test::syntheticTest - timeInterval = ", timeInterval)

        if os.path.exists("%s.txt" %(testOutputFilename)):
            resultFileMode = 'a'  
        else:
            # Create the folder (and the file) if do not exist
            resultFileMode = 'w+'
            resultFileFolder = testOutputFilename.rsplit('/',1)[0]
            if not os.path.isdir(resultFileFolder):
                os.makedirs("%s" %(resultFileFolder))

        file = open("./%s.txt" % (testOutputFilename), resultFileMode)
        file.write("Synthetic Path " + str(density) + " with time interval: " + str(timeInterval) + "seconds\n")
        file.close()
        i = 0
        negative = 0
        while (i < density):
            file = open("./%s.txt" % (testOutputFilename), "a")
            if (pos == 0):
                timeStart = time.time()
                self.device.changePosition(
                    [-37.805265914024076, 144.9631387255518],testOutputFilename, cpsFilename, requestedServices)
                compTime = (time.time() - timeStart)
                remTime = timeInterval - compTime
                file.write(
                    "\tRemaining time: " + str(remTime) + "\n")
                if(remTime <0 ):
                    negative += 1
                pos = 1
                i += 1
            else:
                timeStart = time.time()
                self.device.changePosition(
                    [-37.79713182162259, 144.96755215516572],testOutputFilename, cpsFilename, requestedServices)
                remTime = timeInterval - (time.time() - timeStart)
                compTime = (time.time() - timeStart)
                file.write(
                    "\tRemaining time: " + str(remTime) + "\n")

                if(remTime <0 ):
                    negative += 1
                pos = 0
                i += 1
            totRemainingTime += remTime
            totComputationTime += compTime
            totTime += timeInterval
            # file.close()
        file.write("Average Remaining time: " + str(totRemainingTime/i) + "\n")    
        file.write("Average computation time: " + str(totComputationTime/i) + "\n")
        file.write("Total repetitions: " + str(i) + "\n\tTotal negatives: " + str(negative) + "\n\tTotal positives: " + str(i-negative))  
        file.close()
        print("Test::synteticTest - repeated times: ", i)
        print("Test::synteticTest - time elapsed: ", totTime)

 # Sistema i test prima di rifarli!!
    def main(self):
        ###############################################
        # Realistic Tests                             #
        # For Smartphone with 8GB RAM and 8 CPU cores #
        ###############################################
        # # Change speed
        # # 1.25m/s
        self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI10_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 1.25m/s it the speed
        self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI10_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI20_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI20_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI30_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI30_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # 5.56m/s = 20km/h
        self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI10_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 5.56m/s it the speed
        self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI10_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI20_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI20_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI30_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI30_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # 8.33m/s = 30km/h
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI10_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 8.33m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI10_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI20_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 8.33m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI20_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI30_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI30_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        ###################################
        # Connected users: 250

        # 1.25m/s
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI10_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI10_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI20_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI20_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI30_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI30_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # 5.56m/s = 20km/h
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI10_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 5.56m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI10_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI20_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI20_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI30_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI30_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # 8.33m/s = 30km/h
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI10_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 8.33m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI10_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI20_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 8.33m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI20_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI30_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI30_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        ###################################
        # Connected users: 500
        
        # # 1.25m/s
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI10_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI10_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI20_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI20_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI30_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI30_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # 5.56m/s = 20km/h
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI10_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 5.56m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI10_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI20_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI20_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI30_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI30_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # 8.33m/s = 30km/h
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI10_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 8.33m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI10_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI20_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 8.33m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI20_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI30_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI30_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        ###################################
        # Connected users: 750
        
        # # 1.25m/s
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI10_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI10_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI20_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI20_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI30_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI30_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # 5.56m/s = 20km/h
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI10_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 5.56m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI10_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI20_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI20_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI30_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI30_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # 8.33m/s = 30km/h
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI10_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 8.33m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI10_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI20_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 8.33m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI20_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI30_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI30_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        ###################################
        # Connected users: 1000
        
        # # 1.25m/s
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI10_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI10_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # 5.56m/s = 20km/h
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI10_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 5.56m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI10_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI20_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI20_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI30_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI30_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # 8.33m/s = 30km/h
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 8.33m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 8.33m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)


        ###############################################
        # Synthetic Tests                             #
        # For Smartphone with 8GB RAM and 8 CPU cores #
        ###############################################

        # Density: 50
        # # Change SI List dimension
        self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP1_SI10_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP5_SI10_ConnectedUsers100", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # 1.25m/s
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP1_SI10_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP5_SI10_ConnectedUsers100", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP1_SI20_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP5_SI20_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # Change speed 
        # 20km/h
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI10_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI10_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI20_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI20_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI30_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI30_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI10_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI10_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI20_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI20_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI30_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI30_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
  
        # Density: 75
        # Change SI List dimension
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI10_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI10_ConnectedUsers100", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI20_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI20_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP1_SI20_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP5_SI20_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP1_SI30_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP5_SI30_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # Change speed 
        # 20km/h
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI10_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI10_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI20_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI20_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI30_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI30_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI10_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI10_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI20_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI20_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI30_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI30_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # Density: 100
        # Change SI List dimension
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI10_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI10_ConnectedUsers100", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP1_SI20_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP5_SI20_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP1_SI30_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP5_SI30_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI10_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI10_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI20_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI20_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI30_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI30_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI10_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI10_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI20_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI20_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI30_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI30_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)


        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP1_SI20_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP5_SI20_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP1_SI30_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP5_SI30_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)


        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI20_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI20_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI30_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI30_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI10_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI10_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI20_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI20_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI30_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI30_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        #############################
        # 1000 connected users
        # 1.25m/s
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP1_SI10_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP5_SI10_ConnectedUsers1000", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP1_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP5_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP1_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed1.25_PP5_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI10_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI10_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI20_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI20_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP1_SI30_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed5.56_PP5_SI30_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)


        ###############
        # Density: 75 #
        ###############

        # 1.25m/s
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI10_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI10_ConnectedUsers100", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI20_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI20_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI30_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI30_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI10_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI10_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI20_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI20_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI30_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI30_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI10_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI10_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI20_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI20_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI30_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI30_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        
        ################################
        # Connected Users: 250
        # 1.25m/s
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI10_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI10_ConnectedUsers250", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI20_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI20_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI30_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI30_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI10_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI10_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI20_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI20_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI30_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI30_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI10_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI10_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI20_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI20_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI30_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI30_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        ################################
        # Connected Users: 500
        # # 1.25m/s
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI10_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI10_ConnectedUsers500", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI20_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI20_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI30_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI30_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI10_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI10_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI20_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI20_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI30_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI30_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI10_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI10_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI20_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI20_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI30_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI30_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        ################################
        # Connected Users: 750
        # # 1.25m/s
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI10_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI10_ConnectedUsers750", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI20_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI20_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI30_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI30_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI10_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI10_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI20_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI20_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI30_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI30_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI10_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI10_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI20_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI20_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI30_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI30_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        ################################
        # Connected Users: 1000
        # # 1.25m/s
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI10_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI10_ConnectedUsers1000", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP1_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed1.25_PP5_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI10_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI10_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI20_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI20_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP1_SI30_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed5.56_PP5_SI30_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP1_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(75, "TestingResultsSmartphone/Synthetic/synthetic75_speed8.33_PP5_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)


        ################
        # Density: 100 #
        ################
         
        # Speed 1.25m/s
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI10_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI10_ConnectedUsers100", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI20_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI20_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI30_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI30_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI10_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI10_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI20_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI20_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI30_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI30_ConnectedUsers100", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI10_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI10_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI20_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI20_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI30_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI30_ConnectedUsers100", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        ############################################
        # # # Connected users: 250
        # # Speed 1.25m/s
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI10_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI10_ConnectedUsers250", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI20_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI20_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI30_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI30_ConnectedUsers250", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI10_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI10_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI20_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI20_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI30_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI30_ConnectedUsers250", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI10_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI10_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI20_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI20_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI30_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI30_ConnectedUsers250", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        ################################################
        # # Connected users: 500
        # Speed 1.25m/s
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI10_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI10_ConnectedUsers500", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI20_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI20_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI30_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI30_ConnectedUsers500", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI10_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI10_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI20_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI20_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI30_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI30_ConnectedUsers500", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI10_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI10_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI20_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI20_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI30_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI30_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        ################################################
        # # Connected users: 750
        # Speed 1.25m/s
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI10_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI10_ConnectedUsers750", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI20_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI20_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI30_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI30_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI10_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI10_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI20_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI20_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI30_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI30_ConnectedUsers750", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI10_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI10_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI20_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI20_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI30_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI30_ConnectedUsers750", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        ################################################
        # # Connected users: 1000
        # Speed 1.25m/s
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI10_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI10_ConnectedUsers1000", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI10_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI10_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI20_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI20_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI30_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI30_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        ################
        # Density: 100 #
        ################
         
        # Speed 1.25m/s
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI10_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI10_ConnectedUsers100", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI20_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI20_ConnectedUsers100", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP1_SI30_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)  # 1.25m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP5_SI30_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed1.25_PP10_SI30_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)
        
        # # Change speed
        
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI10_ConnectedUsers2000", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 5.56m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI10_ConnectedUsers2000", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP10_SI10_ConnectedUsers2000", 5.56, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI20_ConnectedUsers2000", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI20_ConnectedUsers2000", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP10_SI20_ConnectedUsers2000", 5.56, "contextualPreferences/contextual_preferences_10PPs_20SIList.xml", 10)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP1_SI30_ConnectedUsers2000", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP5_SI30_ConnectedUsers2000", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed5.56_PP10_SI30_ConnectedUsers2000", 5.56, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)  # 8.33m/s it the speed
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP10_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI20_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI20_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP10_SI20_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_20SIList.xml", 10)

        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP1_SI30_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP5_SI30_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # self.realisticTest("TestingResultsSmartphone/Realistic/realistic_speed8.33_PP10_SI30_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)

        # #30km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI10_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI10_ConnectedUsers500", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)



        ################################################
        # # Connected users: 750
        # Speed 1.25m/s
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI10_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI10_ConnectedUsers750", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI20_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI20_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI30_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI30_ConnectedUsers750", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP10_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)

        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP1_SI20_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP5_SI20_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
        # self.syntheticTest(50, "TestingResultsSmartphone/Synthetic/synthetic50_speed8.33_PP10_SI20_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_20SIList.xml", 10)


        ################################################
        # # Connected users: 1000
        # Speed 1.25m/s
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI10_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI10_ConnectedUsers1000", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # # Change speed 
        # # 20km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI10_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI10_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI20_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI20_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
 
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP1_SI30_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed5.56_PP5_SI30_ConnectedUsers1000", 5.56, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)

        # #30km/h
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)

        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
  
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP10_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)

        # #Change Connected list
        # #Change SI List dimension        
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI10_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI10_ConnectedUsers2000", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP10_SI10_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)

        # # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI30_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI30_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP10_SI30_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)


        # # Change speed
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # self.syntheticTest(100, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP10_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)



        # # Density: 250
        # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP1_SI10_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP5_SI10_ConnectedUsers1000", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP10_SI10_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)

        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP1_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP5_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP10_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_10PPs_20SIList.xml", 10)

        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP1_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP5_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP10_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)

        # # # Change speed
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP1_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP5_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP10_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)

        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP1_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP5_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP10_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_10PPs_20SIList.xml", 10)

        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP1_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP5_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP10_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)

        # # #Change Connected list
        # # #Change SI List dimension        
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP1_SI10_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP5_SI10_ConnectedUsers2000", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP10_SI10_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)

        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP1_SI20_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP5_SI20_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP10_SI20_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_10PPs_20SIList.xml", 10)

        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP1_SI30_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP5_SI30_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed1.25_PP10_SI30_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)

        # # # Change speed
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP1_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP5_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP10_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)

        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP1_SI20_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP5_SI20_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP10_SI20_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_20SIList.xml", 10)

        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP1_SI30_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP5_SI30_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # # self.syntheticTest(250, "TestingResultsSmartphone/Synthetic/synthetic250_speed8.33_PP10_SI30_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)

        # # # Density: 500
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI10_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI10_ConnectedUsers1000", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP10_SI10_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)

        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP10_SI20_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_10PPs_20SIList.xml", 10)

        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP1_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP5_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed1.25_PP10_SI30_ConnectedUsers1000", 1.25, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)

        # # # Change speed
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP10_SI10_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)

        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP10_SI20_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_10PPs_20SIList.xml", 10)

        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP1_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP5_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic100_speed8.33_PP10_SI30_ConnectedUsers1000", 8.33, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)

        # #Change Connected list
        # #Change SI List dimension        
        # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed1.25_PP1_SI10_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed1.25_PP5_SI10_ConnectedUsers2000", 1.25,  "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed1.25_PP10_SI10_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)

        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed1.25_PP1_SI20_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed1.25_PP5_SI20_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed1.25_PP10_SI20_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_10PPs_20SIList.xml", 10)

        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed1.25_PP1_SI30_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed1.25_PP5_SI30_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed1.25_PP10_SI30_ConnectedUsers2000", 1.25, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)

        # # # Change speed
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed8.33_PP1_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_10SIList.xml", 1)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed8.33_PP5_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_10SIList.xml", 5)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed8.33_PP10_SI10_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_10SIList.xml", 10)

        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed8.33_PP1_SI20_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_20SIList.xml", 1)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed8.33_PP5_SI20_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_20SIList.xml", 5)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed8.33_PP10_SI20_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_20SIList.xml", 10)

        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed8.33_PP1_SI30_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_1PP_30SIList.xml", 1)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed8.33_PP5_SI30_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_5PPs_30SIList.xml", 5)
        # # self.syntheticTest(500, "TestingResultsSmartphone/Synthetic/synthetic500_speed8.33_PP10_SI30_ConnectedUsers2000", 8.33, "contextualPreferences/contextual_preferences_10PPs_30SIList.xml", 10)

        self.devJ.stopJVM()


if __name__ == "__main__":
    test = Test().main()
    
