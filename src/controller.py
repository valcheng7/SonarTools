## Required for future_request module else it will go haywire ##
def patch_time():
    return
import gevent.monkey
gevent.monkey.patch_time = patch_time 

## Flask Modules & setup ##
from src import app
from flask import render_template, request, send_file, redirect, url_for, flash, session, make_response  

## Custom sonarqube api module ##
from src.api import sonarAPI

## Filters for projects tab ##
from src.Modules_Filters.filter_issues import FilterProjectIssues

## Filters for issues tab ##
from src.Modules_Filters.filter_projects import filter_projects

## Old pdf ##
from src.pdf import makeProjectsIssues
from src.pdfFilter import pdfFilterProjects
from src.pdfFilter2 import pdfFilterProjectIssues
from src.issuesPDF import createIssuesPDF

## PDF for Issues tab##
from src.Modules_pdf_Issues.issues_report1 import createIssuesPDF1
from src.Modules_pdf_Issues.issues_report2 import createIssuesPDF2
from src.Modules_pdf_Issues.issues_report3 import createIssuesPDF3
from src.Modules_pdf_Issues.mergedPDF import mergedPDF

## Dashboard PDF ##
from src.dashboard_pdf import dashboard_PDF

## Excel For projects tab ##
from src.Modules_Excel.excelProjects import exportExcelProjects

## Excel For issues tab ##
from src.Modules_Excel.excel_issues import exportExcel

## Sorting Function  for projects tab##
from src.projectSort import *

## Other modules ## 
import time
import os 
import string
from datetime import timedelta
from src.forms import LoginForm
import json
import requests
import gc
import gevent
import ast
import shutil
from collections import Counter
from functools import reduce
import pandas as pd
from greenlet import greenlet  

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

@app.context_processor
def inject_username():
    global curr_user
    return dict(user=curr_user)

@app.context_processor
def inject_botResponse():
    global output
    return dict(result=output)

# For project route
project_data = []

# For issues route
project_issues_data = []
projectName = None
issues_languages = []

# For code issues route
project_file_data = []
project = None
line = None
fileName = None

# for filters route (csv file) (projects route)
params = None

# for filter2 route (csv file) (issues route)
params2 = None

# User Credentials

curr_login = None
curr_password = None
curr_user = None

# Dashboard analytics Data 
bugs = None 
codeSmells = None
vulnerabilities = None
numOfProjects = None
horizontalChartData = None
all_languages = None
projs = None

# all project names
allProjects = None

# Project Overview variables
scatterplot = None
projectTitle = None
severity = None
types = None
languages = None

# Project Sorting route 
sortMethod = None

# Chatbot variables #
output = [("message stark", {"text": "Hi, how may I assist you?"})]
latest = []

# Search Bar routes
@app.route('/autocomplete')
def autocomplete():
    client = sonarAPI(curr_login, curr_password)
    global allProjects
    allProjects = client.getProjectNames()
    return 'success'

@app.route('/getAllProjects')
def getAllProjects():  
    global allProjects
    return dict(allProjects=allProjects)

@app.route('/search',methods=['POST'])
def search():
    global allProjects
    if request.method == 'POST':
        data=request.form
        projectName = dict(data)['searchBar']
        if projectName in allProjects:
            return redirect(url_for('load2', source=projectName))
        else:
            print('Project not found...')
    # return "hello"
    # if request.method == 'POST':
    #     data = request.form
    #     get_game_id = conn.execute('select prod_id from products where prod_name = ?',data['myCountry']).fetchone()
    #     if get_game_id:
    #         return redirect(url_for('single_product',id=get_game_id[0]))
    #     else:
    #         print("Game not found!")


# Set Session Lifetime to 1hr
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)


# Index Route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    global bugs
    if "bugs" == None:
        return redirect(url_for('load5'))
    global vulnerabilities
    global codeSmells
    global numOfProjects
    global horizontalChartData
    global all_languages
    global projs
    global bubbleData
    data = [horizontalChartData[0][0:10], horizontalChartData[1][0:10]]
    # numOfProjects = 10
    # codeSmells = 5002
    # vulnerabilities = 600
    # bugs = 860
    # horizontalChartData = [['Android Patient Tracker','Android task monitoring','Fingerprint-based ATM system','Data leakage detection system','Credit card fraud detection','AI shopping system','Camera motion sensor system','Bug tracker','e-Learning platform','Smart health prediction system','Software piracy protection system'],[3229, 3651, 345, 250, 3203, 2227, 4738, 851, 5154, 5958, 200]]
    if request.method == 'GET':
        if "user_id" not in session:
            return redirect(url_for('login'))
        else:
            return render_template('dashboard.html', bugs=bugs, vulnerabilities=vulnerabilities, codeSmells=codeSmells, numOfProjects=numOfProjects, horizontalChartData=data, languages=all_languages,projs=projs,bubbleData=bubbleData)



@app.route('/getDashboardPDF')
def dashboard_pdf():
    global curr_login
    global curr_password 
    downloadpdf = dashboard_PDF(curr_login, curr_password)
    if downloadpdf == "done":
        fname = "dashboard"
        file_dest = "static/downloads/pdf/dashboard.pdf"
        response = make_response(send_file(file_dest, cache_timeout=0))
        response.headers['my_filename'] = fname # I had problems with how the native "filename" key
        return response

@app.route('/zipFile')
def zipFile():
    global curr_login
    global curr_password
    client = sonarAPI(curr_login, curr_password)
    sample = {"data":f"{client.allProject()}"}
    with open('software/result.json', 'w') as fp:
        json.dump(sample,fp)
    print(os.getcwd())
    path = str(os.getcwd())
    shutil.make_archive("src/software", 'zip', f"{path}\software")
    fname = 'software'
    response = make_response(send_file('software.zip', cache_timeout=0))
    response.headers['my_filename'] = fname # I had problems with how the native "filename" key
    return response        

@app.route('/dashboard_pdfLoad')
def download_pdfLoad():
    return render_template('dashboardPdfLoad.html')

# /project route loading screen 
@app.route('/project_loading')
def load():
    if request.method == 'GET':
        if "user_id" not in session:
            return redirect(url_for('login'))
        else:
            return render_template('project_loading.html')

# /issues route loading screen
@app.route('/project_issues_loading')
def load2():
    if request.method == 'GET':
        if "user_id" not in session:
            return redirect(url_for('login'))
        else:
            global projectName
            projectName = request.args.get("source")
            return render_template('project_issues_loading.html')

# /code_issues route loading screen
@app.route('/project_issues_file_loading')
def load3():
    if request.method == 'GET':
        if "user_id" not in session:
            return redirect(url_for('login'))
        else:
            global project
            global line
            global fileName
            try:
                project = request.args.get('source')[0:request.args.get('source').index(':')]
                fileName = request.args.get('file')
                line = request.args.get('line')
            except: 
                print(request.args.get('source'))
                project = request.args.get('source')[:-1]
                line = None 
                fileName = request.args.get('source')[:-1]
            return render_template('project_file_loading.html')

# Issues filter loading screen 
@app.route('/issuesfiltering')
def load4():
    return render_template('filter_loading_issues.html')  

# Dashboard loading screen
@app.route('/dashboardLoading')
def load5():
    return render_template('dashboard_loading.html')

# Account page loading screen
@app.route('/accountLoading')
def load6():
    return render_template('account_loading.html')

# Porject Filtering loaidng screen
@app.route('/projectsfiltering')
def load7():
    return render_template('filter_loading_projects.html')  

# Sorting projects
@app.route('/sortprojectsLoading') 
def load8():
    global sortMethod 
    sortMethod = request.args.get('sort')
    return render_template('projectSortingLoading.html')

# Ajax route to do the api calling for sorting projects at /projects
@app.route('/sortprojects')
def sortProjects():
    global sortMethod
    global project_data
    data = project_data
    if sortMethod == "coverage":
        data = sortByCoverage(data)
    elif sortMethod == "reliability":
        data = sortByReliability(data)
    elif sortMethod == "duplication":
        data = sortByDuplications(data)
    elif sortMethod == "maintainability":
        data = sortByMaintability(data)
    elif sortMethod == "name":
        data = sortByName(data)
    elif sortMethod == "security":
        data = sortBySecurity(data)
    elif sortMethod == "size":
        data = sortBySize(data)
    project_data = data
    return "success"

# Ajax route to do the api calling for /projects
@app.route('/getprojects')
def retieve():
    global project_data
    global languages
    client = sonarAPI(curr_login, curr_password)
    project_data = client.allProject()
    df = pd.DataFrame(project_data)
    b = []
    for i in list(df["codeLanguages"]):
        for j in i:
            b.append(j)
    a = dict(Counter(b))
    total = int(reduce(lambda x1,y2:x1+y2, a.values()))
    for i in a.keys():
        temp = a[i]
        a[i] = [temp, (int(temp)/total)*100]
    languages = a
    return "success"

# Ajax route to do the api calling for /issues
@app.route('/getProjectIssues')
def retrieve2():
    global project_issues_data
    global issues_languages
    client = sonarAPI(curr_login, curr_password)
    project_issues_data = client.specificProjectSourceCodeIssues(projectName)
    print(project_issues_data)
    issues_languages = []
    for i in project_issues_data:
        try:
            lang = i[i.rindex(".")+1:]
            if lang != 'net':
                issues_languages.append(lang)
        except:
            print('name error')
    issues_languages = list(set(issues_languages))
    return "success"


# Ajax route to do the api calling for /code_issues
@app.route('/getprojectsFileIssues')
def retieve3():
    client =  sonarAPI(curr_login, curr_password)
    formattedSourceCode = client.specificFileSourceCodeAndIssues(fileName)
    # print(formattedSourceCode[-1]["sourceCode"])
    if formattedSourceCode[-1]["sourceCode"] != ['']:
        global project_file_data
        project_file_data= []
        for index, content in enumerate(formattedSourceCode[-1]["sourceCode"]):
            added = False
            for i in range(len(formattedSourceCode)-1):
                if formattedSourceCode[i]["startLine"] == index +1:
                    project_file_data.append((content, formattedSourceCode[i]))
                    added = True
            if added == False:
                project_file_data.append((content, {}))
    else:
        project_file_data = [({},formattedSourceCode[0])]
    return "success"

# Ajax route for /issues (filtering)
@app.route('/filterProcessing')
def filterProcess():
    global params2
    global projectName
    global project_issues_data
    client = sonarAPI(curr_login, curr_password)
    orginal_data = client.specificProjectSourceCodeIssues(projectName)
    print(params2)
    if params2 != {"type":[], "severity":[], "languages":[], "date":[]}:
        data = FilterProjectIssues(orginal_data, params2)
        project_issues_data = data
    else:
        project_issues_data = orginal_data
    return "success"

# Ajax route for /projects (filtering)
@app.route('/filterProcessing2')
def filterProcess2():
    global params
    global project_data
    client = sonarAPI(curr_login, curr_password)
    orginal_data = client.allProject()
    if params != {"status":[], "bugs":[], "vulnerabilities":[], "code_smells":[],"securityReview":[], "coverage":[], "size":[], "languages":[], "duplicatePercentage":[]}:
        project_data = filter_projects(orginal_data, params)
    else:
        project_data = orginal_data
    return "success"

# Ajax route for /dashboard
@app.route('/analyticsProcessing')
def analyticsDashboardProcess():
    global bugs
    global vulnerabilities
    global codeSmells
    global numOfProjects
    global horizontalChartData
    global all_languages
    global projs
    global bubbleData
    client = sonarAPI(curr_login, curr_password)
    project_data = client.allProject()
    # Total number of projects
    numOfProjects = len(project_data)
    df = pd.DataFrame(project_data)
    # Converted dataframe columns values into int as they are string currently 
    df["bugs"] = df["bugs"].astype(int)
    df["vulnerabilities"] = df["vulnerabilities"].astype(int)
    df["code_smells"] = df["code_smells"].astype(int)
    # Total number of bugs for all project combined 
    bugs = int(df["bugs"].sum())
    # Total number of vulnerabilties for all projects combined
    vulnerabilities = int(df["vulnerabilities"].sum())
    # Total number of code smells for all projects combined
    codeSmells = int(df["code_smells"].sum())
    # Counting the number of issues each project has (total is consist of vulnerabilities + bugs + code smells)
    titles = []
    numOfIssues = []
    for j in project_data:
        total = 0
        total += int(j["bugs"])
        total += int(j["vulnerabilities"])
        total += int(j["code_smells"])
        numOfIssues.append(total)
        titles.append(j["projectName"])
    horizontalChartData = [titles, numOfIssues]
    # Counting the number of languages used in for all project in total - cs, js, css etc & percentage 
    b = []
    for i in list(df["codeLanguages"]):
        for j in i:
            b.append(j)
    a = dict(Counter(b))
    total = int(reduce(lambda x1,y2:x1+y2, a.values()))
    for i in a.keys():
        temp = a[i]
        a[i] = [temp, (int(temp)/total)*100]
    all_languages = a
    projs = project_data
    # getting records for bubble chart 
    bubbleData = [{"projectName":i["projectName"], "bugs":i["bugs"],"vulnerabilities":i["vulnerabilities"],"code_smells":i["code_smells"],"linesOfCodes": i["languages"][1], "maintainabilityRating": i["maintainabilityRating"], "reliabilityEffort":i["reliabilityEffort"], "securityEffort":i["securityEffort"], "duplicatePercentage":i["duplicatePercentage"], "duplicateBlocks":i["duplicated_blocks"], "reliabilityRating":i["reliabilityRating"], "maintainabilityRating":i["maintainabilityRating"], "securityRating":i["securityRating"], "maintainabilityEffort":i["maintainabilityEffort"]} for i in project_data]
    return "success"

# Filters route for /project
@app.route('/filters')
def filter():
    global params
    params = ast.literal_eval(request.args.get('dict'))
    print(params)   
    return "success"

@app.route('/porjectIssuesChart')
def projectIssuesChart():
    global horizontalChartData
    return render_template('projectIssuesChart.html', horizontalChartData=horizontalChartData)

# Filters route for /issues 
@app.route('/filters2')
def filter2():
    global params2
    params2 = ast.literal_eval(request.args.get('dict'))   
    return "success"

# Login Route
@app.route('/login', methods=["POST", "GET"])
def login():
    if "user_id" in session:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if request.method == "POST":
        print('post request')
        if form.validate_on_submit():
            login = form.login.data
            password = form.password.data
            r = requests.post('http://sonarqubedev.southeastasia.cloudapp.azure.com/api/authentication/login', data={'login':login, 'password': password})
            if r.status_code == 200:
                session["user_id"] = login
                global curr_login 
                curr_login = login
                global curr_password
                curr_password = password
                global curr_user
                r = requests.get('http://sonarqubedev.southeastasia.cloudapp.azure.com/api/users/current', auth=(curr_login, curr_password))
                data = json.loads(r.text)
                login = data['login']
                name = data['name']
                email = data['email']
                groups = data['groups']
                curr_user = {'name': name, 'login': login, 'email': email, 'groups': groups}
                flash('You have successfully logged into Sonar Tools!', 'success')
                return redirect(url_for('load5'))
            else:
                flash('Incorrect login or password, please check your credentials again.', 'danger')
                return render_template('login.html', form=form)
    return render_template('login.html', form=form)

# Logout Route
@app.route("/logout")
def logout():
    session.pop('user_id', None)
    global curr_login 
    global curr_password
    curr_login = None
    curr_password = None
    return redirect(url_for('login'))

# Download CSV file
@app.route('/download_CSVfile')
def download_CSVfile():
    global curr_user
    global project_data
    exportExcelProjects(curr_user['name'], project_data)
    file_dest = "../src/static/downloads/csv/projects.xlsx"
    fname = 'Projects'
    response = make_response(send_file(file_dest, cache_timeout=0))
    response.headers['my_filename'] = fname # I had problems with how the native "filename" key
    return response

# Download CSV file
@app.route('/download_CSVfile2')
def download_CSVfile2():
    global params2
    global curr_user
    global projectName
    global project_issues_data
    file_dest = "../src/static/downloads/csv/issues.xlsx"
    if params2 == None:
        parameters = {"type":[], "severity":[], "languages":[], "date":[]}
    else:
        parameters = params2
    exportExcel(projectName, project_issues_data, curr_user['name'], parameters)
    fname = 'ProjectIssues'
    response = make_response(send_file(file_dest, cache_timeout=0))
    response.headers['my_filename'] = fname # I had problems with how the native "filename" key
    return response

# Download Projects PDF file
@app.route('/download_PDFfile')
def download_PDFfile():
    global params
    client = sonarAPI(curr_login, curr_password)
    main = client.allProject()
    if params == None:
        data = [
        ['Project', 'Status', 'Bugs', 'Vulnerabilities', 'Hotspots Reviewed', 'Code Smells', 'Coverage', 'Duplications', 'Language']
        ]
        for j in main:
            dic = []
            dic.append(j["projectName"])
            dic.append(j["status"])
            dic.append(j["bugs"])
            dic.append(j["vulnerabilities"])
            if j["hotspotPercentage"] == 0:
                dic.append(f'-')
            else:
                dic.append(f'{j["hotspotPercentage"]}%')
            dic.append(j["code_smells"])
            dic.append(f'{j["coverage"]}%')
            dic.append(f'{j["duplicatePercentage"]}%')
            dic.append(f'{j["languages"][1]} lines')
            data.append(dic)
    else:
        data = pdfFilterProjects(main, params)
    makeProjectsIssues(data)
    file_dest = './static/downloads/pdf/Project_issues.pdf'
    return send_file(file_dest, as_attachment=True, cache_timeout=0)


# Download Issues PDF file
@app.route('/download_PDFfile2')
def download_PDFfile2():
    global projectName
    global params2
    global project_issues_data
    global curr_user
    client = sonarAPI(curr_login, curr_password)
    file_dest = './static/downloads/pdf/ProjectIssues.pdf'
    metrics = client.getProjectTypes(f"{projectName}")
    projectDetails = client.getProjectMetrics(f"{projectName}")
    severityNo = client.getProjectSeverity(f"{projectName}")
    name = curr_user['name']
    createIssuesPDF1(name,metrics, projectName, projectDetails, severityNo)
    raw = client.getProjectLanguages(f'codecoverage')
    data = [[j,int(raw[j][0])] for j in raw]
    data.insert(0, ["Languages", "No. of lines"])
    createIssuesPDF2(data, raw)
    createIssuesPDF3(project_issues_data)
    mergedPDF()
    fname = 'ProjectIssues'
    response = make_response(send_file(file_dest, cache_timeout=0))
    response.headers['my_filename'] = fname # I had problems with how the native "filename" key
    return response    
    # return send_file(file_dest, as_attachment=True, cache_timeout=0)

# @app.route('/getUsername')
# def getUsername():
#     global curr_login
#     global curr_password
#     global curr_user
#     r = requests.get('http://sonarqubedev.southeastasia.cloudapp.azure.com/api/users/current', auth=(curr_login, curr_password))
#     data = json.loads(r.text)
#     login = data['login']
#     name = data['name']
#     email = data['email']08032021
#     groups = data['groups']
#     curr_user = {'name': name, 'login': login, 'email': email, 'groups': groups}
#     return 'success'

# Account Route
@app.route('/account')
def account():
    if request.method == 'GET':
        if "user_id" not in session:
            return redirect(url_for('login'))
        else:
            if allProjects == None:
                return redirect(url_for('load6'))
            return render_template('account.html')

# Projects route
@app.route('/projects')
def projects():
    global all_languages
    if request.method == 'GET':
        if "user_id" not in session:
            return redirect(url_for('login'))
        else:
            global project_data
            global params
            if project_data == []:
                return redirect(url_for('load'))
            if params == None:
                parameters = {"status":[], "bugs":[], "vulnerabilities":[], "code_smells":[],"securityReview":[], "coverage":[], "size":[], "languages":[], "duplicatePercentage":[]}
            else: 
                parameters = params
            return render_template('projects.html', data=project_data, languages=all_languages, params=parameters)

# Issues Route
@app.route('/issues')
def issues():
    if request.method == 'GET':
        if "user_id" not in session:
            return redirect(url_for('login'))
        else:
            global project_issues_data
            global projectName
            if project_issues_data == None:
                return redirect(url_for('load'))
            if params2 == None:
                parameters = {"type":[], "severity":[], "languages":[], "date":[]}
            else:
                parameters = params2
            return render_template('issues.html', data=project_issues_data, languages=issues_languages, projectName=projectName, params=parameters)

# Project Overview Route
@app.route('/project_overview')
def project_overview():
    if request.method == 'GET':
        if "user_id" not in session:
            return redirect(url_for('login'))
        else:
            global scatterplot
            global projectTitle
            global severity
            global types
            global languages
            if scatterplot == None:
                return redirect(url_for('projectOverviewLoad'))
    return render_template('project_overview.html', scatterplot=scatterplot, projectTitle=projectTitle, severity = severity, types=types, languages = languages)

@app.route('/projectOverviewLoad')
def projectOverviewLoad():
    if "user_id" not in session:
        return redirect(url_for('login'))
    else:
        global projectTitle
        projectTitle = request.args.get('projectTitle') 
        return render_template('project_overview_loading.html')

@app.route('/getProjectOverview')
def getProjectOverview():
    global scatterplot
    global projectTitle
    global severity
    global types
    global languages
    client = sonarAPI(curr_login, curr_password)
    scatterplot = client.getProjectOverview(projectTitle)
    severity = client.getProjectSeverity(projectTitle)
    types = client.getProjectTypes(projectTitle)
    languages = client.getProjectLanguages(projectTitle)
    return 'success'

# Code Issues Route
@app.route('/code_issues')
def code_issues():
    if request.method == 'GET':
        if "user_id" not in session:
            return redirect(url_for('login'))
        else:
            global project_file_data
            global projectName
            return render_template('code_issues.html', data=project_file_data, file=fileName, line=line, project=project, projectName=projectName)

@app.route('/test')
def test():
    client = sonarAPI(curr_login, curr_password)
    data = client.getProjectsQualityGate()
    return render_template('test.html', text=data)

# Chatbot #
@app.route('/result', methods=["POST", "GET"])
def Result():
    global output
    global latest
    if request.method == "POST":
        result = list(request.form.values())[0]
        if request.args.get('game') != None:
            result = request.args.get('game')
        if result.lower() == "restart":
            output = [("message stark", {"text": "Hi, how may I assist you?"})]
        elif result == '':
            output.extend([("message parker", {"text": result})])
            output.extend([("message stark", {"text": "Sorry I didn't get that..."})])
        else:
            try:
                r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": result})
                li = []
                latest = []
                for i in r.json():
                    if 'image' in i:
                        li.append({"pic": i['image']})
                    if 'text' in i:
                        li.append(i['text'])
                        latest.append(i['text'])
                    if 'buttons' in i:
                        for x in i['buttons']:
                            li.append((x['title'], "button"))
                count = 0
                for i in li:
                    if "I'm sorry, I didn't quite understand that. Could you rephase?" == i:
                        count += 1
                if count > 1:
                    li = [li[0]]
                # print(li)
                sample = [("message parker", {"text": result})]
                buttons = []
                for count, msg in enumerate(li):
                    if count != len(li) - 1 and type(li[count + 1]) is dict:
                        sample.append(("message stark", {"text": msg, "pic": li[count + 1]["pic"]}))
                    elif type(li[count]) is tuple:
                        buttons.append(msg[0])
                    elif type(li[count]) is not dict:
                        sample.append(("message stark", {"text": msg}))
                if buttons != []:
                    sample.append(("message stark", {"button": buttons}))
                output.extend(sample)
                print(output)
                # for i in sample:
                #     if
            except:
                output.extend([("message parker", result), (
                    "message stark", "We are unable to process your request at the moment. Please try again...")])
        return redirect(request.referrer)
        # return render_template(request.path, result=output)

# ajax fetch route to retrive latest bot rrsponse #
@app.route('/latest', methods=['GET', 'POST'])
def fetch():
    if request.method == 'GET':
        global latest
        count = 0
        for i in latest:
            if "I'm sorry, I didn't quite understand that. Could you rephase?" == i:
                count += 1
            if count > 1:
                latest = [latest[0]]
        return str(latest)

"""Error Handling Routes"""


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


@app.errorhandler(500)
def page_not_found500(x):
    return render_template('error500.html'), 500