import jinja2
import pandas as pd
from xhtml2pdf import pisa
import sys,os
from src.api import sonarAPI
import json

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
    
client = sonarAPI('180972B', '08032021')

data = client.specificProjectSourceCodeIssues('CodeJam')

def createIssuesPDF3(data):

    with open('src/rules.json', 'r+') as f:
        rules = json.load(f)

    for i in data:
        for j in data[i]:
            name = j["rule"].replace(':','')
            if '/' in name:
                name = name.replace('/','')
            j["rule"] = name


    html = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='')).get_template("issues_report3.html").render(data=data,codesmell = resource_path('./src/static/img/issues_pdf/code_smell.png'),bugs=resource_path('./src/static/img/issues_pdf/bug.png'),vulnerability = resource_path('./src/static/img/issues_pdf/vulnerability.png'), major = resource_path('./src/static/img/issues_pdf/major.png'), minor= resource_path('./src/static/img/issues_pdf/minor.png'), critical= resource_path('./src/static/img/issues_pdf/critical.png'), blocker= resource_path('./src/static/img/issues_pdf/blocker.png'),info = resource_path('./src/static/img/issues_pdf/info.png'), open = resource_path('./src/static/img/issues_pdf/open.png'), effort = resource_path('./src/static/img/issues_pdf/effort.png'), cal = resource_path('./src/static/img/issues_pdf/cal.png'), line = resource_path('./src/static/img/issues_pdf/error.png'), rules = rules, font=resource_path("./src/static/fonts/BAHNSCHRIFT.TTF"), logo = resource_path('./src/static/img/brand/cyros_logo.png'))
    with open('src/static/downloads/created_pdf/test.pdf', "w+b") as out_pdf_file_handle:
        pisa.CreatePDF(
            src=html,  # HTML to convert
            dest=out_pdf_file_handle)  # File handle to receive result

# createIssuesPDF3(data)