# This class extracts the preferences related to the current context.
# It's called by the Device once it detects a changes in the context

import xml.etree.ElementTree as ET

from context import Context

class PPParser:

    def openFile(self, ppFilename):
        tree = ET.parse(ppFilename)
        root = tree.getroot()
        return root

    def extractPPList(self, ctx: Context, ppFilename):
        ppList = []

        root = self.openFile(ppFilename)
    
        timeList = root.findall("./situation/[@situation='" + ctx.getNewSituation() + "']/city/[@city_name='" +
                                ctx.getNewCity() + "']/area/[@area_name='" + ctx.getNewArea() + "']/pi/[@pi_name='" + ctx.getNewPi() + "']/time/[@al_time='" + ctx.getNewCurrentTime() +
                                "']")
        # remove from the list the element with "ex_time" == newCurrentTime
        # ps. it would has more sense with realistic time
        for time in timeList:
            if(time.get("ex_time") == ctx.getNewCurrentTime()):
                timeList.remove(time)

        # Check the activities
        for time in timeList:
            actList = time.findall(
                "./activity/[@al_activity='" + ctx.getNewActivity() + "']")
            # remove from the list the element with "ex_activity" == newActivity
            # ps. it would has more sense with a better representation of the activity. But it is out of scope
            for act in actList:
                if(act.get("ex_activity") == ctx.getNewActivity()):
                    actList.remove(act)
                subTrees = act.findall("./privacypreference/[@pp].")
                # print("PPParser::extractPPList - sub-tree: ", subTrees)
                for tree in subTrees:
                    pp = tree.get("pp")
                    ppList.append(pp)
        return ppList


    def extractSI(self, ctx: Context, pp, ppFilename):
        socialIgnResult = {
            "siList": [],
            "threshold": 0
        }

        root = self.openFile(ppFilename)

        # parse the xml preferences file to find all the SI list
        timeList = root.findall("./situation/[@situation='" + ctx.getNewSituation() + "']/city/[@city_name='" +
                                ctx.getNewCity() + "']/area/[@area_name='" + ctx.getNewArea() + "']/pi/[@pi_name='" + ctx.getNewPi() + "']/time/[@al_time='" + ctx.getNewCurrentTime() +
                                "']")
        # remove from the list the element with "ex_time" == newCurrentTime
        
        for time in timeList:
            if(time.get("ex_time") == ctx.getNewCurrentTime()):
                timeList.remove(time)

        # Check the activities
        for time in timeList:
            actList = time.findall(
                "./activity/[@al_activity='" + ctx.getNewActivity() + "']")
            # remove from the list the element with "ex_activity" == newActivity
            for act in actList:
                if(act.get("ex_activity") == ctx.getNewActivity()):
                    actList.remove(act)
                socialIgn = act.findall("./privacypreference/[@pp='"+ pp + "']/social_ignore/.")
                # print("PPParser::estractSI - socialIgn size (it should be always 1): ", len(socialIgn))
                for si in socialIgn: 
                    siList = si.get("list")
                    siTh = si.get("threshold")
                    # print("ppParser::EstractSI - SI list: ", siList, " th: ", siTh)
                    socialIgnResult["siList"] = list(siList.split(" "))
                    socialIgnResult["threshold"] = siTh

        return socialIgnResult



