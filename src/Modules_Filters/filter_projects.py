def filter_projects(project_data2, parameters):
    project_data = project_data2
    for i in list(parameters.keys()):
        if i == "status" and parameters[i] != []:
            project_data = status(project_data, parameters)
        if i == "languages" and parameters[i] != []:
            project_data = languages(project_data, parameters)
        if i == "bugs" and parameters[i] != []:
            project_data = reliabilityRating(project_data, parameters)
        if i == "vulnerabilities" and parameters[i] != []:
            project_data = securityRating(project_data, parameters)
        if i == "code_smells" and parameters[i] != []:
            project_data = maintabilityRating(project_data, parameters)
        if i == "securityReview" and parameters[i] != []:
            project_data = securityReviewRating(project_data, parameters)
        if i == "size" and parameters[i] != []:
            project_data = size(project_data, parameters)
        if i == "coverage" and parameters[i] != []:
            project_data = coverage(project_data, parameters)
        if i == "duplicatePercentage" and parameters[i] != []:
            project_data = duplications(project_data, parameters)
    return project_data


def status(array, parameters):
    li = []
    for i, j in enumerate(array):
        if j["status"] in parameters["status"]:
            li.append(j)
    return li

def reliabilityRating(array, parameters):
    li = []
    for i, j in enumerate(array):
        if j["reliabilityRating"] in parameters["bugs"]:
            li.append(j)
    return li

def securityRating(array, parameters):
    li = []
    print(array)
    for i, j in enumerate(array):
        if j["securityRating"] in parameters["vulnerabilities"]:
            li.append(j)
    return li 

def securityReviewRating(array, parameters):
    li = []
    for i in parameters["securityReview"]:
        if len(i) == 1:
            if float(i[0]) == 30.0:
                for index, j in enumerate(array):
                    if j["hotspotPercentage"] != 0:
                        if float(j["hotspotPercentage"]) < float(i[0]):
                            li.append(j)
            else:
                for index, j in enumerate(array):
                    if float(j["hotspotPercentage"]) > float(i[0]):
                        li.append(j)
                    elif j["hotspotPercentage"] == 0:
                        li.append(j)
        else: 
            for index, j in enumerate(array):
                if float(j["hotspotPercentage"]) >= float(i[0]) and float(j["hotspotPercentage"]) <= float(i[1]):
                    li.append(j)
    return li   

def maintabilityRating(array, parameters):
    li = []
    for i, j in enumerate(array):
        if j["maintainabilityRating"] in parameters["code_smells"]:
            li.append(j)
    return li 

def coverage(array, parameters):
    li = []
    print('here')
    for i in parameters["coverage"]:
        if len(i) == 1:
            if float(i[0]) == 30.0:
                for index, j in enumerate(array):
                    if float(j["coverage"]) < float(i[0]):
                        li.append(j)
            else:
                for index, j in enumerate(array):
                    if float(j["coverage"]) > float(i[0]):
                        li.append(j)
        else: 
            for index, j in enumerate(array):
                if float(j["coverage"]) >= float(i[0]) and float(j["coverage"]) <= float(i[1]):
                    li.append(j)
    return li   
        
def size(array, parameters):
    li = []
    for i in parameters["size"]:
        print(i)
        if len(i) == 1:
            if int(i[0]) == 1000:
                for index, j in enumerate(array):
                    if int(j["languages"][1]) < int(i[0]):
                        li.append(j)
            else:
                for index, j in enumerate(array):
                    if int(j["languages"][1]) > int(i[0]):
                        li.append(j)
        else: 
            for index, j in enumerate(array):
                if int(j["languages"][1]) >= int(i[0]) and int(j["languages"][1]) <= int(i[1]):
                    li.append(j)
    return li   
    
def duplications(array, parameters):
    li = []
    for i in parameters["duplicatePercentage"]:
        if len(i) == 1:
            if float(i[0]) == 3.0:
                for index, j in enumerate(array):
                    if float(j["duplicatePercentage"]) < float(i[0]):
                        li.append(j)
            else:
                for index, j in enumerate(array):
                    if float(j["duplicatePercentage"]) > float(i[0]):
                        li.append(j)
        else: 
            for index, j in enumerate(array):
                if float(j["duplicatePercentage"]) >= float(i[0]) and float(j["duplicatePercentage"]) <= float(i[1]):
                    li.append(j)
    return li   

def languages(array, parameters):
    li = []
    for i, j in enumerate(array):
        added = False
        for z in [list(x.keys())[0] for x in j["languages"][0]]:
            if z in parameters["languages"]:
                added = True
        if added == True:
            li.append(j)
    return li

