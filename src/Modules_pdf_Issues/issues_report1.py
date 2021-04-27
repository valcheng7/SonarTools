from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Frame, Image, TableStyle, Table, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import utils
from reportlab.lib import colors
import seaborn as sns 
import matplotlib.pyplot as plt
import pandas as pd
import datetime

from src.api import sonarAPI

# Picture
def get_image(path, width=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

projectName = "CodeJam"

# Data class
class Pin:
    scannedDate = ""
    hotspotsRating = ""
    hotspotsReviewed = ""
    coverage = ""
    duplication = ""
    linesOfCode = ""

def genPinTable(pin):
    # hotspotRatingPic = Image(pin.hotspotsRating)
    pic = get_image(pin.hotspotsRating, width=0.6*cm)
    # hotspotRatingPic.drawWidth = 20
    # hotspotRatingPic.drawHeight = 20
    hotspotTable = Table([[pic]], 20, 30)


    projectDetailsTable2 = Table([
        [pin.scannedDate, hotspotTable, pin.hotspotsReviewed, pin.coverage, pin.duplication, pin.linesOfCode]
    ], [104, 50, 54, 104, 104, 104])

 

    projectDetailsTable2Style = ([
        ('ALIGN', (0, 0), (0,-1), 'CENTER'),
        ('ALIGN', (1, 1), (1,-1), 'RIGHT'),
        ('LEFTPADDING', (1,0), (1,-1), 20),
        ('LEFTPADDING', (2,0), (2,-1), 0),
        ('ALIGN', (3, 0), (-1,-1), 'CENTER'),
        ('VALIGN', (0, 0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), '#E9EBF5'),
        ('BOX', (0,0), (-1,-1), 1, colors.white),
        ('GRID', (0,0), (0,-1), 1, colors.white),
        ('GRID', (3,0), (-1,-1), 1, colors.white),
        # ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    projectDetailsTable2.setStyle(projectDetailsTable2Style)


    return projectDetailsTable2


# Data class
class boxes:
    field = ""
    value = ""
    picture = ""


def genBoxesTable(box):
    qualityTable = Table([
        [box.field]
    ], 100, rowHeights=(0.55*cm))


    # Style
    qualityStyle = ([
        
        ('FONTNAME', (0,0), (-1,-1), 'abc'),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        # ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1,-1), 'MIDDLE'),
        
        # ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    qualityTable.setStyle(qualityStyle)


    statusTable = Table([
        [box.value]
    ], 100, rowHeights=(0.56*cm))

    # Style
    statusTableStyle = ([
        
        ('FONTNAME', (0,0), (-1,-1), 'abc'),
        ('VALIGN', (0, 0), (-1,-1), 'MIDDLE'),
        # ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,0), (-1, -1), 14),
        ('BOTTOMPADDING', (0,0), (1,-1), 15),
        
        # ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    statusTable.setStyle(statusTableStyle)

    qualityStatusTable = Table([
        [qualityTable],
        [statusTable]
    ], 108)


    qualityStatusTableStyle = ([ 
        # ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,-1), "#E9EBF5"),
    ])
    qualityStatusTable.setStyle(qualityStatusTableStyle)


    qualityGateStatusTick = get_image(box.picture, width=1.04*cm)
    QualityGateStatusTickTable = Table([[qualityGateStatusTick]], 20, 30)

    qualityGateStatusTable = Table([
        [qualityStatusTable, QualityGateStatusTickTable]
    ], [115, 50])


    qualityGateStatusTableStyle = ([ 
        # ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,-1), "#E9EBF5"),
        ('VALIGN', (1, 0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1, 0), (-1,-1), 'LEFT'),
        ('LEFTPADDING', (1,0), (1,-1), 0),
    ])
    qualityGateStatusTable.setStyle(qualityGateStatusTableStyle)
    return qualityGateStatusTable 

def createIssuesPDF1(name, metric, projectName, projectDetails, severity):
    date = str(datetime.datetime.now())[:str(datetime.datetime.now()).index(" ")]
    time = str(datetime.datetime.now())[str(datetime.datetime.now()).index(" ")+1:str(datetime.datetime.now()).rindex(":")]
    fileName = "src/static/downloads/created_pdf/Project_Issues_Report.pdf"
    documentTitle = "SonarTools Project Report"
    title = "Project Overview"
    image = './src/static/img/brand/cyros_logo.png'

    pdf = canvas.Canvas(fileName)
    pdf.setTitle(documentTitle)

    pdfmetrics.registerFont(
        TTFont('abc', 'BAHNSCHRIFT.TTF')
    )

    value = metric["STATUS"]
    if value == "Passed":
        picture = "./src/static/img/issues_pdf/qualityGateTick.png"
    else:
        picture = "./src/static/img/issues_pdf/qualityGateCross.png"

    # pdf.line(50, 585, 550, 585)

    pdf.setFont('abc', 30)
    pdf.drawCentredString(300, 630, "Project Issues Report")
    pdf.setFont('abc', 25)
    pdf.drawCentredString(300, 590, "Sonar Tools")

    # pdf.line(50, 685, 550, 685)

    cover = Frame(1, 102, 593, 450, showBoundary=0)
    addCover = []
    addCover.append(get_image("./src/static/img/issues_pdf/cover.png", width=21*cm))
    cover.addFromList(addCover, pdf)

    logo = Frame(365, 10, 220, 50, showBoundary=0)
    addlogo = []
    addlogo.append(get_image("./src/static/img/brand/cyros.png", width=6.5*cm))
    logo.addFromList(addlogo, pdf)

    pdf.showPage()

    frame = Frame(0.6*cm, 27*cm, 2*cm, 1.5*cm, showBoundary=0)
    story = []
    story.append(get_image(image, width=1*cm))
    frame.addFromList(story, pdf)

    # Project Overview Title
    pdf.setFont('abc', 20)
    pdf.drawString(70, 780, title)

    pdf.line(230, 785, 550, 785)

    # Name, date
    # text = pdf.beginText(40, 730)
    # text.setFont("abc", 12)
    # text.setFillColor(colors.red)
    # for line in textLines:
    #     text.textLine(line)

    # pdf.drawText(text)

    # Table
    flow_obj = []
    style = getSampleStyleSheet()
    t = Table([["Name:", name], ["Date:", date]])
    ts=TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'abc'),
        ('FONTSIZE', (0,0), (-1, -1), 12)
    ])
    t.setStyle(ts)
    flow_obj.append(t)
    frame2 = Frame(43, 702, 165, 48, showBoundary=0)
    frame2.addFromList(flow_obj, pdf)


    projectDetailsTable = Table([
        ["Last Scanned", "Hotspots Reviewed", "Coverage", "Duplication", "No. of lines of code"]
    ], 104, rowHeights=(0.9*cm))


    # Style
    projectDetailsTableStyle = ([
        ('ALIGN', (0, 0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,0), (-1,0), '#5e72e4'),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.whitesmoke),
        ('VALIGN', (0, 0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,-1), 'abc'),
        ('BOX', (0,0), (-1,-1), 1, colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.white),
        ('FONTSIZE', (0,0), (-1, -1), 11),
        
        # ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    projectDetailsTable.setStyle(projectDetailsTableStyle)

    pin = Pin()
    pin.scannedDate = projectDetails["date"]
    if projectDetails["hotspotRating"] == "1.0":
        ratingPic = "src/static/img/letters/a.png"
    elif projectDetails["hotspotRating"] == "2.0":
        ratingPic = "src/static/img/letters/b.png"
    elif projectDetails["hotspotRating"] == "3.0":
        ratingPic = "src/static/img/letters/c.png"
    elif projectDetails["hotspotRating"] == "4.0":
        ratingPic = "src/static/img/letters/d.png"
    else:
        ratingPic = "src/static/img/letters/e.png"
    pin.hotspotsRating = ratingPic
    pin.hotspotsReviewed = projectDetails["hotspotPercent"]
    pin.coverage = projectDetails["coverage"]
    pin.duplication = projectDetails["duplication"]
    pin.linesOfCode = projectDetails["lines"]

    p1 = genPinTable(pin)

    flow_obj2 = []

    flow_obj2.append(projectDetailsTable)
    flow_obj2.append(p1)
    frame3 = Frame(16, 600, 570, 100, showBoundary=0)   
    frame3.addFromList(flow_obj2, pdf)


    # Project Name ----------------------------------------------------------------------

    # Table


    projName = Table([["Project Name:", projectName]])
    projNameStyle=TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'abc'),
        ('FONTSIZE', (0,0), (-1, -1), 12)  
    ])
    projName.setStyle(projNameStyle)

    flow_obj5 = []
    flow_obj5.append(projName)
    frame6 = Frame(43, 580, 135, 30, showBoundary=0)
    frame6.addFromList(flow_obj5, pdf)

    # Boxes ------------------------------------------------------------



    statusTable = Table([
            ["Quality Gate Status"]
        ], 100, rowHeights=(0.55*cm))


    # Style
    statusTableStyle = ([
        
        ('FONTNAME', (0,0), (-1,-1), 'abc'),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        # ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1,-1), 'MIDDLE'),
        
        # ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    statusTable.setStyle(statusTableStyle)


    valueStatusTable = Table([
        [value]
    ], 100, rowHeights=(0.56*cm))

    # Style
    valueStatusTableStyle = ([
        
        ('FONTNAME', (0,0), (-1,-1), 'abc'),
        ('VALIGN', (0, 0), (-1,-1), 'MIDDLE'),
        # ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,0), (-1, -1), 14),
        ('BOTTOMPADDING', (0,0), (1,-1), 15),
        
        # ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    valueStatusTable.setStyle(valueStatusTableStyle)

    statusValueTable = Table([
        [statusTable],
        [valueStatusTable]
    ], 108)

    if value == "Passed":
        bc = "#48d1cc"
    else:
        bc = "#EA6675"




    statusTick = get_image(picture, width=1.04*cm)
    statusTickTable = Table([[statusTick]], 20, 30)



    statusRowTable = Table([
        [statusValueTable, statusTickTable]
    ], [469, 50])


    statusRowTableStyle = ([ 
        # ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,-1), bc),
        ('VALIGN', (1, 0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1, 0), (-1,-1), 'LEFT'),
        ('LEFTPADDING', (1,0), (1,-1), 0),
    ])
    statusRowTable.setStyle(statusRowTableStyle)

    box2 = boxes()
    box2.field = "Bugs"
    box2.value = metric["BUG"]
    box2.picture = "./src/static/img/issues_pdf/typeBug.png"

    box3 = boxes()
    box3.field = "Vulnerabilties"
    box3.value = metric["VULNERABILITY"]
    box3.picture = "./src/static/img/issues_pdf/typeVulnerability.png"

    box4 = boxes()
    box4.field = "Code Smells"
    box4.value = metric["CODE_SMELL"]
    box4.picture = "./src/static/img/issues_pdf/typeCodeSmell.png"

    p2 = genBoxesTable(box2)
    p3 = genBoxesTable(box3)
    p4 = genBoxesTable(box4)


    mainTable = Table([
        [p2, p3, p4],
    ])

    flow_obj3 = []
    flow_obj3.append(statusRowTable)

    frame4 = Frame(42, 510, 520, 65, showBoundary=0)
    frame4.addFromList(flow_obj3, pdf)



    flow_obj4 = []

    flow_obj4.append(mainTable)
    frame5 = Frame(42, 450, 520, 70, showBoundary=0)
    frame5.addFromList(flow_obj4, pdf)


    # No. of issues for each severity level

    text = pdf.beginText(40, 430)
    text.setFont("abc", 12)
    text.setFillColor(colors.black)

    text.textLine('Number of issues for each severity level')

    pdf.drawText(text)


    # Severity table -------------------------------------------------------

    severityData = [severity["MAJOR"], severity["MINOR"], severity["CRITICAL"], severity["BLOCKER"], severity["INFO"]]

    severityTable = Table([
            ["Major", "Minor", "Critical", "Blocker", "Info"],
            severityData
        ], 104, rowHeights=(0.9*cm))

    severityTableStyle = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), '#5e72e4'),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1, -1), 'CENTER'),
            ('VALIGN', (0,0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0,0), (-1,0), 'abc'),
            ('FONTSIZE', (0,0), (-1, -1), 11),
            ('BACKGROUND', (0,1), (-1,-1), "#E9EBF5"),
            ('BOX', (0,0), (-1,-1), 1, colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.white)
        ])

    severityTable.setStyle(severityTableStyle)

    frame0 = Frame(42, 350, 520, 70, showBoundary=0)
    story0 = []
    story0.append(severityTable)
    frame0.addFromList(story0, pdf)

    # Severity Graph ----------------------------------------------------

    frame1 = Frame(42, 60, 520, 300, showBoundary=0)
    story1 = []

    # Chart
    severity_titles = ['Major', 'Minor', 'Critical', 'Blocker', 'Info']
    severity_list = [severity['MAJOR'], severity['MINOR'], severity['CRITICAL'], severity['BLOCKER'], severity['INFO']]

    dataset = pd.DataFrame([{"Severity":'MAJOR',"No. of issues":severity_list[0]}, {"Severity":'MINOR',"No. of issues":severity_list[1]},{"Severity":'CRITICAL', "No. of issues":severity_list[2]},{"Severity":'BLOCKER', "No. of issues":severity_list[3]},{"Severity":'INFO', "No. of issues":severity_list[4]}])

    sns.catplot(x="No. of issues", y='Severity', data=dataset, kind='bar')
    plt.savefig('src/static/img/issues_pdf/severity.png', bbox_inches='tight')

    story1.append(get_image("src/static/img/issues_pdf/severity.png", width=10*cm))

    frame1.addFromList(story1, pdf)


    pdf.save()


# name = "Valentia Cheng Le Xuan"

# client = sonarAPI("180972B","08032021")

# metrics = client.getProjectTypes("CodeJam")

# projectDetails = client.getProjectMetrics('CodeJam')

# severityNo = client.getProjectSeverity("CodeJam")

# projectName = "CodeJam"

# createIssuesPDF1(name, metrics, projectName, projectDetails, severityNo)