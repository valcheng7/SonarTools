from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    data = ['maintainabilityRating', 'securityReviewRating', 'reliabilityRating', 'securityRating', 'hotspotNumber', 'hotspotPercentage', 'languages', 'duplicatePercentage', 'status', 'codeSmells', 'coverage', 'bugs', 'vulnerabilities', 'reliabilityEffort', 'securityEffort', 'maintainabilityEffort', 'duplicatedBlocks', 'lines']
    return render_template('test.html', data=data)

app.run(debug=True)

import requests

# username = '180972B'
# password = '08032021'

# funcRes, projectRatings = {}, []
# res = requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/measures/component?component=codecoverage&metricKeys=security_rating,reliability_rating,sqale_rating,security_review_rating,security_hotspots,security_hotspots_reviewed,duplicated_lines_density,ncloc_language_distribution,alert_status,code_smells,coverage,bugs,vulnerabilities,reliability_remediation_effort,security_remediation_effort,sqale_index,duplicated_blocks", auth=(username, password))
# sqaleRating, securiyReviewRating, securityRating, reliabilityRating,index = 0, 0, 0, 0,0 
# percentage, num = 0,0 
# duplicatePercentage, linesOfCode = 0,0
# if res.json()["component"]["measures"] != []:
#     for i in res.json()["component"]["measures"]:
#         if i["metric"] == "sqale_rating":
#             sqaleRating = i["value"]
#         if i["metric"] == "duplicated_blocks":
#             duplicated_blocks = i["value"]
#         elif i["metric"] == "reliability_remediation_effort":
#             time1 = int(i["value"])
#         elif i["metric"] == "security_remediation_effort":
#             time2 = int(i["value"])
#         elif i["metric"] == "sqale_index":
#             time3 = int(i["value"])
#         elif i["metric"] == "reliability_rating":
#             reliabilityRating = i["value"]
#         elif i["metric"] == "coverage":
#             coverage = i["value"]
#         elif i["metric"] == "security_rating":
#             securityRating = i["value"]
#         elif i["metric"] == "security_review_rating":
#             securiyReviewRating = i["value"]
#         elif i['metric'] == 'security_hotspots_reviewed':
#             percentage = i['value']
#         elif i['metric'] == "security_hotspots":
#             num = i['value']
#         elif i["metric"] == "duplicated_lines_density":
#             duplicatePercentage = i["value"]
#         elif i["metric"] == "ncloc":
#             linesOfCode = i["value"]
#         elif i["metric"] == "code_smells":
#             number = i["value"]
#         elif i["metric"] == "bugs":
#             bugs_number = i["value"]
#         elif i["metric"] == "vulnerabilities":
#             vul_num = i["value"]
#         elif i["metric"] == "ncloc_language_distribution":
#             values = i["value"].split(";")
#             languages = [{i[:i.index("=")]:i[i.index('=')+1:]} for i in values]
#             code_language = []
#             for i in languages:
#                 code_language.append(list(i.keys())[0])
#             total = 0
#             for i in languages:
#                 total += int(list(i.values())[0])
#         elif i["metric"] == "alert_status":
#             if i["value"] == "OK":
#                 status = "Passed"
#             else:
#                 status = "Failed"
#         proj_id = "a"+str(index)
#     projectRatings.append({"projectName":res.json()["component"]["key"], "maintainabilityRating":sqaleRating, "securityReviewRating": securiyReviewRating, "reliabilityRating":reliabilityRating, "securityRating":securityRating, "hotspotNumber":num, "hotspotPercentage": percentage, "languages":(languages,total), "duplicatePercentage":duplicatePercentage, "linesOfCodes":linesOfCode, "status":status, "code_smells":number, "coverage":coverage, "bugs":bugs_number, "vulnerabilities":vul_num, "codeLanguages":code_language, "reliabilityEffort":time1, "securityEffort":time2, "maintainabilityEffort":time3, "duplicated_blocks":duplicated_blocks, "proj_id":proj_id, "lines":total})

# print(projectRatings[0].keys())