# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

import requests


username = '180972B'
password = '08032021'

metric = {
    "1.0":"A",
    "2.0":"B",
    "3.0":"C",
    "4.0":"D",
    "5.0":"E",
}

class GetProjectProjectName(Action):

    def name(self) -> Text:
        return "getProjectProjectName"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                proj_id = "a"+str(index)
            projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The project name for {project} is {projectRatings[0]['projectName']}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectMaintainabilityRating(Action):

    def name(self) -> Text:
        return "getProjectMaintainabilityRating"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The maintainability rating for {project} is {metric[projectRatings[0]['maintainabilityRating']]}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectSecurityReviewRating(Action):

    def name(self) -> Text:
        return "getProjectSecurityReviewRating"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            pass
        if projectRatings != []:
            dispatcher.utter_message(text=f"The security review Rating for {project} is {metric[projectRatings[0]['securityReviewRating']]}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectReliabilityRating(Action):

    def name(self) -> Text:
        return "getProjectReliabilityRating"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The reliability rating for {project} is {metric[projectRatings[0]['reliabilityRating']]}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectSecurityRating(Action):

    def name(self) -> Text:
        return "getProjectSecurityRating"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The security rating for {project} is {metric[projectRatings[0]['securityRating']]}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectHotspotNumber(Action):

    def name(self) -> Text:
        return "getProjectHotspotNumber"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The hotspot reviewed rating for {project} is {metric[projectRatings[0]['securityReviewRating']]}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectHotspotPercentage(Action):

    def name(self) -> Text:
        return "getProjectHotspotPercentage"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            if projectRatings[0]['hotspotPercentage'] == 0:
                hotspotPercentage = "-"
            else:
                hotspotPercentage = f"{projectRatings[0]['hotspotPercentage']}%"
            dispatcher.utter_message(text=f"The hotspots reviewed percentage for {project} is {hotspotPercentage}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
        
class GetProjectDuplicatePercentage(Action):

    def name(self) -> Text:
        return "getProjectDuplicatePercentage"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The duplications percentage for {project} is {projectRatings[0]['duplicatePercentage']}%")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectStatus(Action):

    def name(self) -> Text:
        return "getProjectStatus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The Status for {project} is {projectRatings[0]['status']}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
        return []
    
class GetProjectCode_smells(Action):

    def name(self) -> Text:
        return "getProjectCode_smells"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The number of code smells for {project} is {projectRatings[0]['code_smells']}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectCoverage(Action):

    def name(self) -> Text:
        return "getProjectCoverage"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The coverage percentage for {project} is {projectRatings[0]['coverage']}%")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectBugs(Action):

    def name(self) -> Text:
        return "getProjectBugs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                    
            projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The number of bugs for {project} is {projectRatings[0]['bugs']}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
        return []
    
class GetProjectVulnerabilities(Action):

    def name(self) -> Text:
        return "getProjectVulnerabilities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The number of vulnerabilities for {project} is {projectRatings[0]['vulnerabilities']}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    

  ## TO DO ##  
class GetProjectCodeLanguages(Action):

    def name(self) -> Text:
        return "getProjectCodeLanguages"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})

                string = "" 
                i = 1

                for j in projectRatings[0]['codeLanguages']:
                    if j == "cs":
                        lang = "C#"
                    elif j == "css":
                        lang = "CSS"
                    elif j == "flex":
                        lang = "Flex"
                    elif j == "go":
                        lang = "Go"
                    elif j == "web":
                        lang = "HTML"
                    elif j == "jsp":
                        lang = "JSP"
                    elif j == "java":
                        lang = "Java"
                    elif j == "js":
                        lang = "JavaScript"
                    elif j == "kotlin":
                        lang = "Kotlin"
                    elif j == "php":
                        lang = "PHP"
                    elif j == "py":
                        lang = "Python"
                    elif j == "ruby":
                        lang = "Ruby"
                    elif j == "scala":
                        lang = "Scala"
                    elif j == "ts":
                        lang = "TypeScript"
                    elif j == "vbnet":
                        lang = "VB.NET"
                    elif j == "xml":
                        lang = "XML"
                    else:
                        lang = j
                    string += f"\n{i}. {lang}"
                    i += 1
        except: 
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The language(s) used for {project} is/are: {string}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")

            return []
    
class GetProjectReliabilityEffort(Action):

    def name(self) -> Text:
        return "getProjectReliabilityEffort"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
            
            hours = int(projectRatings[0]['reliabilityEffort'])//60
            if(hours > 8):
                days = hours//8
                corhours = hours
                while corhours > 8:
                    corhours -= 8
                string = f'{days}d{corhours}h'
            else:
                mins = i%60
                string = f'{hours}h{mins}m' 
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The reliability effort for {project} is {string}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectSecurityEffort(Action):

    def name(self) -> Text:
        return "getProjectSecurityEffort"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
            
            hours = int(projectRatings[0]['securityEffort'])//60
            if(hours > 8):
                days = hours//8
                corhours = hours
                while corhours > 8:
                    corhours -= 8
                string = f'{days}d{corhours}h'
            else:
                mins = i%60
                string = f'{hours}h{mins}m'
        except:
            projectRatings = [] 
        if projectRatings != []:
            dispatcher.utter_message(text=f"The security effort for {project} is {string}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectMaintainabilityEffort(Action):

    def name(self) -> Text:
        return "getProjectMaintainabilityEffort"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
            
            hours = int(projectRatings[0]['maintainabilityEffort'])//60
            if(hours > 8):
                days = hours//8
                corhours = hours
                while corhours > 8:
                    corhours -= 8
                string = f'{days}d{corhours}h'
            else:
                mins = i%60
                string = f'{hours}h{mins}m' 
        except:
            projectRatings = []        
        if projectRatings != []:
            dispatcher.utter_message(text=f"The maintainability effort for {project} is {string}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectDuplicated_blocks(Action):

    def name(self) -> Text:
        return "getProjectDuplicated_blocks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The number of duplicated blocks for {project} is {projectRatings[0]['duplicated_blocks']}")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []
    
class GetProjectLines(Action):

    def name(self) -> Text:
        return "getProjectLines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project = tracker.get_slot("project_name")
        funcRes, projectRatings = {}, []
        res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={project}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        percentage, num = 0,0 
        duplicatePercentage, linesOfCode = 0,0
        try:
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    if i["metric"] == "duplicated_blocks":
                        duplicated_blocks = i["value"]
                    elif i["metric"] == "reliability_remediation_effort":
                        time1 = int(i["value"])
                    elif i["metric"] == "security_remediation_effort":
                        time2 = int(i["value"])
                    elif i["metric"] == "sqale_index":
                        time3 = int(i["value"])
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "coverage":
                        coverage = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                    elif i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                    elif i["metric"] == "duplicated_lines_density":
                        duplicatePercentage = i["value"]
                    elif i["metric"] == "ncloc":
                        linesOfCode = i["value"]
                    elif i["metric"] == "code_smells":
                        number = i["value"]
                    elif i["metric"] == "bugs":
                        bugs_number = i["value"]
                    elif i["metric"] == "vulnerabilities":
                        vul_num = i["value"]
                    elif i["metric"] == "ncloc_language_distribution":
                        values = i["value"].split(";")
                        languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                        code_language = []
                        for i in languages:
                            code_language.append(list(i.keys())[0])
                        total = 0
                        for i in languages:
                            total += int(list(i.values())[0])
                    elif i["metric"] == "alert_status":
                        if i["value"] == "OK":
                            status = "Passed"
                        else:
                            status = "Failed"
                    proj_id = "a"+str(index)
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})
        except:
            projectRatings = []
        if projectRatings != []:
            dispatcher.utter_message(text=f"The total number of lines for {project} is {projectRatings[0]['lines']} lines")
        else:
            dispatcher.utter_message(text=f"{project} is not a valid project")
            return []

from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ValidateProjectNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_projectName_form"

    def validate_project_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""
        listOfProjects = [i["key"] for i in requests.get("http://sonarqubedev.southeastasia.cloudapp.azure.com/api/components/search?qualifiers=TRK", auth=(username, password)).json()["components"]]
        # If the name is super short, it might be wrong.
        print(f"First name given = {slot_value} length = {len(slot_value)}")
        if slot_value not in listOfProjects:
            dispatcher.utter_message(text=f"{slot_value} is an invalid project name, please retype again")
            return {"project_name": None}
        else:
            return {"project_name": slot_value}

class moreProjectInfo(Action):

    def name(self) -> Text:
        return "moreProjectInfo"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_moreProjectInfo",
                                 project_name=tracker.get_slot("project_name"))

class ActionResetAllSlots(Action):

    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]

    