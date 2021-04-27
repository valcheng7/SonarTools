# def defaultCase(arr, param):
#     print("This is the default case")
#     return arr 

# def typeOnly(arr, param):
#     print('Only the type filter is being applied here')
#     li = []
#     srcNames = {}
#     for i, j in enumerate(arr):
#         for k in arr[j]:
#             dic = []
#             if k["type"] in param["type"]:
#                 li.append(k)
#                 if k["src"] not in srcNames:
#                     srcNames[k["src"]] = []
#     for i in li: 
#         if i["src"] in srcNames.keys():
#             srcNames[i["src"]].append(i)
#     return srcNames

# def severityOnly(arr, param):
#     print('Only the severity filter is beign applied here')
#     li = []
#     srcNames = {}
#     for i, j in enumerate(arr):
#         for k in arr[j]:
#             dic = []
#             if k["severity"] in param["severity"]:
#                 li.append(k)
#                 if k["src"] not in srcNames:
#                     srcNames[k["src"]] = []
#     for i in li: 
#         if i["src"] in srcNames.keys():
#             srcNames[i["src"]].append(i)
#     return srcNames

# def typeAndSeverity(arr, param):
#     print('The type and severity filter is being applied here')
#     li = []
#     srcNames = {}
#     for i, j in enumerate(arr):
#         for k in arr[j]:
#             dic = []
#             if k["type"] in param["type"]:
#                 if k["severity"] in param["severity"]:
#                     li.append(k)
#                     if k["src"] not in srcNames:
#                         srcNames[k["src"]] = []
#     for i in li: 
#         if i["src"] in srcNames.keys():
#             srcNames[i["src"]].append(i)
#     return srcNames

# Filterconditions = {
#     "00": defaultCase,
#     "10": typeOnly,
#     "01": severityOnly,
#     "11": typeAndSeverity      
#     }

def FilterProjectIssues(project_issues_data, parameters):
    for i in list(parameters.keys()):
        if i == "type" and parameters[i] != []:
            project_issues_data = Type(project_issues_data, parameters)
        if i == "severity" and parameters[i] != []:
            project_issues_data = severity(project_issues_data, parameters)
        if i == "languages" and parameters[i] != []:
            project_issues_data = languages(project_issues_data, parameters)
        if i == "date" and parameters[i] !=[]:
            project_issues_data = filterDate(project_issues_data, parameters)
    return project_issues_data


def severity(obj, parameters):
    li = []
    srcNames = {}
    for i, j in enumerate(obj):
        for k in obj[j]:
            if k["severity"] in parameters["severity"]:
                li.append(k)
                if k["src"] not in srcNames:
                    srcNames[k["src"]] = []
    for i in li: 
        if i["src"] in srcNames.keys():
            srcNames[i["src"]].append(i)
    return srcNames

def Type(obj, parameters):
    li = []
    srcNames = {}
    for i, j in enumerate(obj):
        for k in obj[j]:
            if k["type"] in parameters["type"]:
                li.append(k)
                if k["src"] not in srcNames:
                    srcNames[k["src"]] = []
    for i in li: 
        if i["src"] in srcNames.keys():
            srcNames[i["src"]].append(i)
    return srcNames
    
def languages(obj, parameters):
    li = []
    srcNames = {}
    for i, j in enumerate(obj):
        if j[j.rindex(".")+1:] in parameters["languages"]:
            for k in obj[j]:
                li.append(k)
                if k["src"] not in srcNames:
                    srcNames[k["src"]] = []
    for i in li: 
        if i["src"] in srcNames.keys():
            srcNames[i["src"]].append(i)
    return srcNames

def filterDate(obj, parameters):
    li = []
    srcNames = {}
    if len(parameters["date"]) == 2:
        for i, j in enumerate(obj):
            for k in obj[j]:
                if k["creationDate"] >= parameters["date"][0] and k["creationDate"] <= parameters["date"][1]:
                    li.append(k)
                    if k["src"] not in srcNames:
                        srcNames[k["src"]] = []
    elif len(parameters["date"]) == 1:
        if parameters["date"][0][:parameters["date"][0].index(':')] == 'StartDate':
            for i, j in enumerate(obj):
                for k in obj[j]:
                    if k["creationDate"][1] > parameters["date"][0][:parameters["date"][0].index(':')+1:]:
                        li.append(k)
                        if k["src"] not in srcNames:
                            srcNames[k["src"]] = []
        else:
            for i, j in enumerate(obj):
                for k in obj[j]:
                    if k["creationDate"][1] < parameters["date"][0][:parameters["date"][0].index(':')+1:]:
                        li.append(k)
                        if k["src"] not in srcNames:
                            srcNames[k["src"]] = []
    for i in li: 
        if i["src"] in srcNames.keys():
            srcNames[i["src"]].append(i)
    return srcNames


