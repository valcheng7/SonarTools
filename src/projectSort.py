def sortByName(listOfProjects):
    li = listOfProjects
    li.sort(key=lambda iteration:iteration["projectName"].lower())
    return li

def sortByReliability(listOfProjects):
    li = listOfProjects
    li.sort(key=lambda iteration:iteration["projectName"].lower())
    li.sort(key=lambda iteration:float(iteration["reliabilityRating"]))
    return li

def sortBySecurity(listOfProjects):
    li = listOfProjects
    li.sort(key=lambda iteration:iteration["projectName"].lower())
    li.sort(key=lambda iteration:float(iteration["securityRating"]))
    return li

def sortByMaintability(listOfProjects):
    li = listOfProjects
    li.sort(key=lambda iteration:iteration["projectName"].lower())
    li.sort(key=lambda iteration:float(iteration["maintabilityRating"]))
    return li

def sortByCoverage(listOfProjects):
    li = listOfProjects
    li.sort(key=lambda iteration:iteration["projectName"].lower())
    li.sort(key=lambda iteration:float(iteration["coverage"]))
    return li

def sortBySize(listOfProjects):
    li = listOfProjects
    li.sort(key=lambda iteration:iteration["projectName"].lower())
    li.sort(key=lambda iteration:int(iteration["languages"][1]))
    return li

def sortByDuplications(listOfProjects):
    li = listOfProjects
    li.sort(key=lambda iteration:iteration["projectName"].lower())
    li.sort(key=lambda iteration:float(iteration["duplicatePercentage"]))
    return li


# from api import sonarAPI

# client = sonarAPI("180972B", "08032021")
# project_data = client.allProject()

# collection = ProjectSort(project_data)
# li = collection.sortByDate()
# for j in li:
#     print(j["projectName"])
#     print()