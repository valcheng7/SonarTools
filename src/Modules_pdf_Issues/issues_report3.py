import jinja2
import pandas as pd
from xhtml2pdf import pisa
import sys,os
import time
# from src.api import sonarAPI
import json
def patch_time():
    return
import gevent.monkey
gevent.monkey.patch_time = patch_time 
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
    
# username = '180972B'
# password = '08032021'

# """Specific project's source code issues pertaining to each code file"""
# def specificProjectSourceCodeIssues(projectTitle):
#     start = time.time()
#     total = int(requests.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/issues/search?componentKeys={projectTitle}&ps=500&resolved=false&additionalFields=rules", auth=(username, password)).json()["total"])
#     pageSize, pageNumber = 500,1 
#     while total > pageSize: 
#         total -= pageSize
#         pageNumber += 1
#     with FuturesSession() as session:
#         futures = [session.get(f"http://sonarqubedev.southeastasia.cloudapp.azure.com/api/issues/search?componentKeys={projectTitle}&ps=500&p={j}&resolved=false&additionalFields=rules", auth=(username, password)) for j in range(1,pageNumber+1)]
#     raw, srcNames = [], {}
#     for res in as_completed(futures):
#         if res.result().json()["issues"] != []:
#             for secondIndex, con in enumerate(res.result().json()["issues"]):
#                 raw.append({
#                 "src":con["component"], 
#                 "severity":con["severity"], 
#                 "key": con["key"], 
#                 "startLine": con["textRange"]["startLine"] if "textRange" in con.keys() else None, 
#                 "endLine": con["textRange"]["endLine"]if "textRange" in con.keys() else None, 
#                 "status": con["status"], 
#                 "message":con["message"], 
#                 "effort":con["effort"] if "effort" in con else "0min", 
#                 "type":con["type"],
#                 "creationDate":con["creationDate"][:con["creationDate"].index('T')],
#                 "rule":con["rule"]
#                 })
#                 if con["component"] not in srcNames:
#                     srcNames[con["component"]] = []
#     for i in raw: 
#         if i["src"] in srcNames.keys():
#             srcNames[i["src"]].append(i)
#     return srcNames

# data = specificProjectSourceCodeIssues('eshoponweb')
# print(data)

def createIssuesPDF3(data):
    start = time.time()
    with open('src/rules.json', 'r+') as f:
        rules = json.load(f)

    for i in data:
        for j in data[i]:
            name = j["rule"].replace(':','')
            if '/' in name:
                name = name.replace('/','')
            j["rule"] = name

    counter = 0

    inBatches = 0
    notInBatches = 0

    for i in data:
        if len(data[i]) > 20:
            split_count = len(data[i])/20
            count = 20
            batches = []
            if split_count > int(split_count):
                print('float')
                count = 20
                batches = []
                for k in range(int(split_count)+1):
                    if k == (split_count - 1):
                        batch = data[i][count:]
                    elif k == 0:
                        batch = data[i][0:count]
                    else:
                        batch = data[i][count:count+20] 
                        count += 20
                    batches.append(batch)
            else:
                count = 20
                batches = []
                for k in range(int(split_count)):
                    if k == 0:
                        batch = data[i][0:count]
                    else:
                        batch = data[i][count:count+20] 
                        count += 20
                    batches.append(batch)
            for j in batches:
                inBatches += len(j)
                convert = {i:j}
                html = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='')).get_template("issues_report3.html").render(data=convert,codesmell = resource_path('./src/static/img/issues_pdf/code_smell.png'),bugs=resource_path('./src/static/img/issues_pdf/bug.png'),vulnerability = resource_path('./src/static/img/issues_pdf/vulnerability.png'), major = resource_path('./src/static/img/issues_pdf/major.png'), minor= resource_path('./src/static/img/issues_pdf/minor.png'), critical= resource_path('./src/static/img/issues_pdf/critical.png'), blocker= resource_path('./src/static/img/issues_pdf/blocker.png'),info = resource_path('./src/static/img/issues_pdf/info.png'), open = resource_path('./src/static/img/issues_pdf/open.png'), effort = resource_path('./src/static/img/issues_pdf/effort.png'), cal = resource_path('./src/static/img/issues_pdf/cal.png'), line = resource_path('./src/static/img/issues_pdf/error.png'), rules = rules, font=resource_path("./src/static/fonts/BAHNSCHRIFT.TTF"), logo = resource_path('./src/static/img/brand/cyros_logo.png'))
                counter += 1
                with open(f'src/static/downloads/pre_pdf/pdf{counter}.pdf', "w+b") as out_pdf_file_handle:
                    pisa.CreatePDF(
                        src=html,  # HTML to convert
                        dest=out_pdf_file_handle)  # File handle to receive result
        else:
            convert = {i:data[i]}
            notInBatches += len(data[i])
            html = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='')).get_template("issues_report3.html").render(data=convert,codesmell = resource_path('./src/static/img/issues_pdf/code_smell.png'),bugs=resource_path('./src/static/img/issues_pdf/bug.png'),vulnerability = resource_path('./src/static/img/issues_pdf/vulnerability.png'), major = resource_path('./src/static/img/issues_pdf/major.png'), minor= resource_path('./src/static/img/issues_pdf/minor.png'), critical= resource_path('./src/static/img/issues_pdf/critical.png'), blocker= resource_path('./src/static/img/issues_pdf/blocker.png'),info = resource_path('./src/static/img/issues_pdf/info.png'), open = resource_path('./src/static/img/issues_pdf/open.png'), effort = resource_path('./src/static/img/issues_pdf/effort.png'), cal = resource_path('./src/static/img/issues_pdf/cal.png'), line = resource_path('./src/static/img/issues_pdf/error.png'), rules = rules, font=resource_path("./src/static/fonts/BAHNSCHRIFT.TTF"), logo = resource_path('./src/static/img/brand/cyros_logo.png'))
            counter += 1
            with open(f'src/static/downloads/pre_pdf/pdf{counter}.pdf', "w+b") as out_pdf_file_handle:
                pisa.CreatePDF(
                    src=html,  # HTML to convert
                    dest=out_pdf_file_handle) 

    print(counter, "the number of files")
    print(notInBatches + inBatches, 'the total')
    import PyPDF2 
    import os
    

    def mergedPDF(counter):
        directory = 'src/static/downloads/pre_pdf'

        pdfWriter = PyPDF2.PdfFileWriter()
        for i in range(1, counter+1):
            # Open the files that have to be merged one by one
            pdf1File = open(f'{directory}/pdf{i}.pdf', 'rb')

            
            # Read the files that you have opened
            pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
            
            
            # Loop through all the pagenumbers for the first document
            for pageNum in range(pdf1Reader.numPages):
                pageObj = pdf1Reader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            
        # Now that you have copied all the pages in both the documents, write them into the a new document
        pdfOutputFile = open('src/static/downloads/created_pdf/test.pdf', 'wb')
        pdfWriter.write(pdfOutputFile)
        
        # Close all the files - Created as well as opened
        pdfOutputFile.close()
       
    mergedPDF(counter)
    print("Ending Time is: ", time.time()-start)
    


# createIssuesPDF3(data)



    