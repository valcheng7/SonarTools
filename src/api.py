def patch_time():
    return
import gevent.monkey
gevent.monkey.patch_time = patch_time 
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests
import time 
import json



class sonarAPI:
    
    def __init__(self, username, password):
        self.__username = username
        self.__password = password 
        self.__listOfProjects = [i["key"] for i in requests.get("http://sonarqubedev.southeastasia.cloudapp.azure.com/api/components/search?qualifiers=TRK", auth=(username, password)).json()["components"]]

    """Retrieve all project quality gate"""     
    def getProjectNames(self):
        projectNames = []
        qualityGates = self.getProjectsQualityGate()['projects']
        for i in qualityGates:
            if i[1] != 'NONE':
                projectNames.append(i[0])
        return projectNames
    
    def getProjectOverview(self, projectTitle):
        total = int(requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/issues/search?componentKeys={projectTitle}&ps=500&resolved=false", auth=(self.__username, self.__password)).json()["total"])
        pageSize, pageNumber = 500,1 
        while total > pageSize: 
            total -= pageSize
            pageNumber += 1
        with FuturesSession() as session:
            futures = [session.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/issues/search?componentKeys={projectTitle}&ps=500&p={j}&resolved=false", auth=(self.__username, self.__password)) for j in range(1,pageNumber+1)]
        raw, srcNames = [], {}
        overview ={}
        for res in as_completed(futures):
            if res.result().json()["issues"] != []:
                for secondIndex, con in enumerate(res.result().json()["issues"]):
                    raw.append({
                    "src":con["component"], 
                    "effort":con["effort"] if "effort" in con else "0min", 
                    })
                    if con["component"] not in srcNames:
                        srcNames[con["component"]] = []
        for i in raw: 
            if i["src"] in srcNames.keys():
                srcNames[i["src"]].append(i)
        for i in srcNames:
            effort = 0
            overview[i] = []
            totalEffort, noOfIssues = 0, 0
            for x in srcNames[i]:
                totalEffort += int(x['effort'][:x['effort'].index('m')])
                noOfIssues += 1
            overview[i].append(totalEffort)
            overview[i].append(noOfIssues)
        return overview
    
    def getProjectSeverity(self, projectTitle):
        project = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/issues/search?facets=severities&componentKeys={projectTitle}&resolved=false", auth=(self.__username, self.__password))
        severity = json.loads(project.text)
        data = severity['facets'][0]['values']
        barGraph = {}
        for i in data:
            if i['val'] == 'MINOR':
                barGraph['MINOR'] = i['count']
            elif i['val'] == 'MAJOR':
                barGraph['MAJOR'] = i['count']
            elif i['val'] == 'INFO':
                barGraph['INFO'] = i['count']
            elif  i['val'] == 'CRITICAL':
                barGraph['CRITICAL'] = i['count']
            else:
                barGraph['BLOCKER'] = i['count']
        return barGraph
    
    def getProjectTypes(self, projectTitle):
        data1 = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/issues/search?facets=types&componentKeys={projectTitle}&resolved=false", auth=(self.__username, self.__password))
        data2 = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/qualitygates/project_status?projectKey={projectTitle}", auth=(self.__username, self.__password))
        status = json.loads(data2.text)['projectStatus']['status']
        types = json.loads(data1.text)['facets'][0]['values']
        blocks = {}
        if status == 'OK':
            blocks['STATUS'] = "Passed"
        else:
            blocks['STATUS'] = "Failed"
        for i in types:
            if i['val'] == 'CODE_SMELL':
                blocks['CODE_SMELL'] = i['count']
            elif i['val'] == 'BUG':
                blocks['BUG'] = i['count']
            else:
                blocks['VULNERABILITY'] = i['count']
        return blocks

    def getProjectMetrics(self, projectTitle):
        metricDic = {}
        dateData = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/components/show?component={projectTitle}", auth=(self.__username, self.__password))
        dateTime = json.loads(dateData.text)["component"]["analysisDate"]
        date = dateTime[:dateTime.index('T')]
        metricDic["date"] = date
        metricData = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={projectTitle}&metricKeys=coverage,duplicated_lines_density,ncloc_language_distribution,security_hotspots_reviewed,security_review_rating", auth=(self.__username, self.__password))
        metric = json.loads(metricData.text)["component"]["measures"]
        if "security_hotspots_reviewed" not in metric:
            metricDic["hotspotPercent"] = "-"
        for i in metric:
            if i["metric"] == "security_review_rating":
                metricDic["hotspotRating"] = i["value"]
            elif i["metric"] == "security_hotspots_reviewed":
                metricDic["hotspotPercent"] = f'{i["value"]}%'
            elif i["metric"] == "coverage":
                metricDic["coverage"] = f'{i["value"]}%'
            elif i["metric"] == "duplicated_lines_density":
                metricDic["duplication"] = f'{i["value"]}%'
            else:
                total = 0
                values = i["value"].split(";")
                languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
                for i in languages:
                    total += int(list(i.values())[0])
                metricDic["lines"] = total
        return metricDic

    def getProjectLanguages(self, projectTitle):
        data3 = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/issues/search?facets=languages&componentKeys={projectTitle}&resolved=false", auth=(self.__username, self.__password))
        languages = json.loads(data3.text)['facets'][0]['values']
        bar2, total = {}, 0
        for x in languages:
            total += int(x['count'])
        for i in languages:
            percentage = round((i['count'] / total) * 100)
            if i['val'] == 'cs':
                bar2["C#"] = [i['count'], percentage]
            elif i['val'] == 'css':
                bar2["CSS"] = [i['count'], percentage]
            elif i['val'] == 'js':
                bar2["JavaScript"] = [i['count'], percentage]
            elif i['val'] == 'web':
                bar2["HTML"] = [i['count'], percentage]
            elif i['val'] == 'ruby':
                bar2["Ruby"] = [i['count'], percentage]
            elif i['val'] == 'vbnet':
                bar2["VB.NET"] = [i['count'], percentage]
            elif i['val'] == 'xml':
                bar2["XML"] = [i['count'], percentage]
            else:
                bar2[i['val']] = [i['count'], percentage]
        return bar2

    def getProjectsQualityGate(self):
        
        funcRes, qualityGates, passed, failed = {} ,[], 0, 0
        with FuturesSession() as session:
            futures = [session.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/qualitygates/project_status?projectKey={j}", auth=(self.__username, self.__password)) for j in self.__listOfProjects]
        for future in as_completed(futures):
            response = future.result()
            sliced = response.url[response.url.index("=")+1:]
            if response.json()["projectStatus"]["status"] != "NONE":
                if response.json()["projectStatus"]["status"] == "ERROR": 
                    failed += 1
                else:
                    passed +=1 
            qualityGates.append((sliced,response.json()["projectStatus"]["status"]))
        funcRes["projects"] = qualityGates
        funcRes["status_numbers"] = {"passed_projects":passed, "failed_projects":failed}
        
        return funcRes
    
    """Retrieve all langauges that sonarQube can perfrom static code analysis"""
    def getSupportedLanguages(self):
        res = requests.get("http://sonarqubedev.southeastasia.cloudapp.azure.com/api/languages/list?ps=0", auth=(self.__username, self.__password))
        return res.json()["languages"]
    
    """Retrieve all project's security, maintainability, secuirty_review and reliability rating"""
    def allProjectRating(self):
        funcRes, projectRatings = {}, []
        with FuturesSession() as session:
            futures = [session.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={j}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating", auth=(self.__username, self.__password)) for j in self.__listOfProjects]
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating = 0, 0, 0, 0 
        for future in as_completed(futures):
            res = future.result()
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i["metric"] == "sqale_rating":
                        sqaleRating = i["value"]
                    elif i["metric"] == "reliability_rating":
                        reliabilityRating = i["value"]
                    elif i["metric"] == "security_rating":
                        securityRating = i["value"]
                    elif i["metric"] == "security_review_rating":
                        securiyReviewRating = i["value"]
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating})
        funcRes["projects"] = projectRatings
        return funcRes
          
    """Retrieve all project security hotspots number & percentage"""
    def allProjectSecurityHotspotNumberAndPercentage(self):
        funcRes, ratings = {}, []
        start = time.time()
        with FuturesSession() as session:
            futures = [session.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={j}&metricKeys=security_hotspots,security_hotspots_reviewed", auth=(self.__username, self.__password)) for j in self.__listOfProjects]
        for future in as_completed(futures):
            res = future.result()
            percentage, num = 0,0 
            if res.json()["component"]["measures"] != []:
                for i in res.json()["component"]["measures"]:
                    if i['metric'] == 'security_hotspots_reviewed':
                        percentage = i['value']
                    elif i['metric'] == "security_hotspots":
                        num = i['value']
                ratings.append({"projectName":res.json()["component"]["key"], "hotspotNumber":num, "hotspotPercentage": percentage})
        funcRes["projects"] = ratings
        print(time.time()-start)
        print(len(ratings))
        return funcRes
        
    """Specific project's security, maintainability, secuirty_review and reliability rating""" 
    def specificProjectRating(self, projectTitle):
        response = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={projectTitle}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating", auth=(self.__username, self.__password))
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating = 0, 0, 0, 0 
        if response.json()["component"]["measures"] != []:
            for i in response.json()["component"]["measures"]:
                if i["metric"] == "sqale_rating":
                    sqaleRating = i["value"]
                elif i["metric"] == "reliability_rating":
                    reliabilityRating = i["value"]
                elif i["metric"] == "security_rating":
                    securityRating = i["value"]
                elif i["metric"] == "security_review_rating":
                    securiyReviewRating = i["value"]
        return {"projectName":response.json()["component"]["key"], "maintabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating}
        
    """Specific project's langauges & number of lines associated with the language"""
    def specificProjectLangaugeAndAmtOfLines(self, projectTitle):
        response = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={projectTitle}&metricKeys=ncloc_language_distribution", auth=(self.__username, self.__password))
        if response.json()["component"]["measures"] != []:
            values = response.json()["component"]["measures"][0]["value"].split(";")
            languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values] 
        return languages
                
    """Specific project's coverage"""
    def specificProjectCoverage(self, projectTitle):
        response = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/search_history?component={projectTitle}&metrics=coverage", auth=(self.__username, self.__password))
        if response.json()["measures"][0]["history"] != []:
            return {"projectName":projectTitle,"coverage":response.json()["measures"][0]["history"][-1]["value"]}
    
    """Specific project's duplication"""
    def specificprojectDuplicationPercentageAndNumber(self, projectTitle):
        response = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={projectTitle}&metricKeys=ncloc,duplicated_lines_density", auth=(self.__username, self.__password))
        duplicatePercentage, linesOfCode = 0,0
        if response.json()["component"]["measures"] != []:
            for i in response.json()["component"]["measures"]:
                if i["metric"] == "duplicated_lines_density":
                    duplicatePercentage = i["value"]
                elif i["metric"] == "ncloc":
                    linesOfCode = i["value"]
        return {"projectName":projectTitle,  }
                    
    """Specific project's number of code smells"""
    def specificProjectNumberOfCodeSmells(self, projectTitle):
        response = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={projectTitle}&metricKeys=code_smells",auth=(self.__username, self.__password))
        return {"projectName":response.json()["component"]["key"],"codeSmellCount":response.json()["component"]["measures"][0]["value"]}
        
    """Specific project's number of bugs"""
    def specificProjectNumberOfBugs(self, projectTitle):
        response = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={projectTitle}&metricKeys=bugs",auth=(self.__username, self.__password))
        return {"projectName":response.json()["component"]["key"],"bugsCount":response.json()["component"]["measures"][0]["value"]}
    
    """Specific project's number of vulnerabilities"""
    def specificProjectNumberOfVulnerabilities(self, projectTitle):
        response = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={projectTitle}&metricKeys=vulnerabilities",auth=(self.__username, self.__password))
        return {"projectName":response.json()["component"]["key"],"vulnerabilitiesCount":response.json()["component"]["measures"][0]["value"]}
   
    
    """Specific project's number of security hotspots number & percentage"""
    def specificProjectSecurityHotspotNumberAndPercentage(self, projectTitle):
        response = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={projectTitle}&metricKeys=security_hotspots,security_hotspots_reviewed", auth=(self.__username, self.__password))
        percentage, num = 0,0 
        if response.json()["component"]["measures"] != []:
            for i in response.json()["component"]["measures"]:
                if i['metric'] == 'security_hotspots_reviewed':
                    percentage = i['value']
                elif i['metric'] == "security_hotspots":
                    num = i['value']
        return {"projectName":response.json()["component"]["key"], "hotspotNumber":num, "hotspotPercentage": percentage}
        
    """Specific project's source code issues pertaining to each code file"""
    def specificProjectSourceCodeIssues(self, projectTitle):
        total = int(requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/issues/search?componentKeys={projectTitle}&ps=500&resolved=false&additionalFields=rules", auth=(self.__username, self.__password)).json()["total"])
        pageSize, pageNumber = 500,1 
        while total > pageSize: 
            total -= pageSize
            pageNumber += 1
        with FuturesSession() as session:
            futures = [session.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/issues/search?componentKeys={projectTitle}&ps=500&p={j}&resolved=false&additionalFields=rules", auth=(self.__username, self.__password)) for j in range(1,pageNumber+1)]
        raw, srcNames = [], {}
        for res in as_completed(futures):
            if res.result().json()["issues"] != []:
                for secondIndex, con in enumerate(res.result().json()["issues"]):
                    raw.append({
                    "src":con["component"], 
                    "severity":con["severity"], 
                    "key": con["key"], 
                    "startLine": con["textRange"]["startLine"] if "textRange" in con.keys() else None, 
                    "endLine": con["textRange"]["endLine"]if "textRange" in con.keys() else None, 
                    "status": con["status"], 
                    "message":con["message"], 
                    "effort":con["effort"] if "effort" in con else "0min", 
                    "type":con["type"],
                    "creationDate":con["creationDate"][:con["creationDate"].index('T')],
                    "rule":con["rule"]
                    })
                    if con["component"] not in srcNames:
                        srcNames[con["component"]] = []
        for i in raw: 
            if i["src"] in srcNames.keys():
                srcNames[i["src"]].append(i)
        return srcNames

    """Specific file source code and errors"""
    def specificFileSourceCodeAndIssues(self, fileName):
        try:
            obj = self.specificProjectSourceCodeIssues(fileName[:fileName.index(":")])
            data =  requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/sources/raw?key={fileName}", auth=(self.__username, self.__password)).text
            formattedSourceCode = data.split('\n')
            obj[fileName].append({"sourceCode":formattedSourceCode})
        except:
            obj = self.specificProjectSourceCodeIssues(fileName)
            print(obj)
            data =  requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/sources/raw?key={fileName}", auth=(self.__username, self.__password)).text
            formattedSourceCode = data.split('\n')
            obj[fileName].append({"sourceCode":formattedSourceCode})
        return obj[fileName]


    def allProject(self):
        funcRes, projectRatings = {}, []
        with FuturesSession() as session:
            futures = [session.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component={j}&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(self.__username, self.__password)) for j in self.__listOfProjects]
        sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
        for future in as_completed(futures):
            index += 1
            res = future.result()
            percentage, num = 0,0 
            duplicatePercentage, linesOfCode = 0,0
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
                projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id})
        return projectRatings




project = sonarAPI('180972B', '08032021')
# print(project.getProjectMetrics('codecoverage'))
