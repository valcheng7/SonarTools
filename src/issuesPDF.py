from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from cgi import escape
from src.api import sonarAPI

# Data class
class Pin:
    project = ""
    message = ""
    date = ""
    error = ""
    types = ""
    serverity = ""
    status = ""
    effort = ""
    cal = ""
    line = ""
    typePath = ""
    serverityPath = ""
    statusPath = ""
    effortPath = ""


# Generate tables 
def genPinTable(pin):
    calender = Image(pin.cal)
    calender.drawWidth = 10
    calender.drawHeight = 10
    calTable = Table([[calender]], 10, 10)

    line = Image(pin.line)
    line.drawWidth = 10
    line.drawHeight = 10
    lineTable = Table([[line]], 10, 10)

    types = Image(pin.typePath)
    types.drawWidth = 10
    types.drawHeight = 10
    typesTable = Table([[types]], 10, 10)

    serverity = Image(pin.serverityPath)
    serverity.drawWidth = 10
    serverity.drawHeight = 10
    serverityTable = Table([[serverity]], 10, 10)

    status = Image(pin.statusPath)
    status.drawWidth = 10
    status.drawHeight = 10
    statusTable = Table([[status]], 10, 10)
    
    effort = Image(pin.effortPath)
    effort.drawWidth = 10
    effort.drawHeight = 10
    effortTable = Table([[effort]], 10, 10)


    projectTable = Table([
        [pin.project]
    ], 550)

    messageTable = Table([
        [pin.message, calTable, pin.date, lineTable, pin.error]
    ], [360, 25, 68, 25, 58])
    
    categoryTable = Table([
        [typesTable, pin.types, serverityTable, pin.serverity, statusTable, pin.status, effortTable, pin.effort]
    ], [22, 75, 22, 45, 22, 52, 22, 75])


    pinElemTable = Table([
        [messageTable],
        [categoryTable]
    ], 550)

    if pin.project == "":
        bigTable = Table([
            [pinElemTable]
        ], 550)
    else:
        bigTable = Table([
            [projectTable],
            [pinElemTable]
        ], 550)

    # Style
    messageTableStyle = ([
        ('ALIGN', (1, 0), (-1,-1), 'LEFT'),
        ('VALIGN', (1, 0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (1,0), (1,-1), 14),
        ('TOPPADDING', (3,0), (3,-1), 14),
        ('FONTNAME', (0,0), (-1,-1), 'Courier-Bold'),
        ('TEXTCOLOR', (0,0), (-1,-1), '#525f7f'),
        ('FONTSIZE', (0,0), (-1, -1), 9),
        
        # ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    messageTable.setStyle(messageTableStyle)

    categoryTableStyle = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0, 0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (1,-1), 0),
        ('LEFTPADDING', (2,0), (3,-1), 0),
        ('LEFTPADDING', (4,0), (5,-1), 0),
        ('LEFTPADDING', (6,0), (7,-1), 0),
        ('TOPPADDING', (0,0), (0,-1), 7),
        ('TOPPADDING', (2,0), (2,-1), 7),
        ('TOPPADDING', (4,0), (4,-1), 7),
        ('TOPPADDING', (6,0), (6,-1), 7),
        # ('ALIGN', (3, 0), (3,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,0), (-1, -1), 'Courier-Bold'),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('FONTSIZE', (0,0), (-1, -1), 9),
        # ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    categoryTable.setStyle(categoryTableStyle)

    pinElemTableStyle = TableStyle([
        ('BOX', (0,0), (-1,-1), 1, '#f2dede'),
        ('BACKGROUND', (0,0), (-1,-1), '#f2dede'),
    ])
    pinElemTable.setStyle(pinElemTableStyle)

    return bigTable



def createIssuesPDF(project):
    client = sonarAPI("180972B", "08032021")
    data = client.specificProjectSourceCodeIssues(project)

# print(main)


# data = {'CodeJam:Services/FileBlogService.cs': 

# [{'src': 'CodeJam:Services/FileBlogService.cs', 'severity': 'MAJOR', 'key': 'AXc45crkWnoiXpYu_wD9', 'startLine': 150, 'endLine': 150, 'status': 'OPEN', 'message': 'Split this method into two, one handling parameters check and the other handling the asynchronous code.','effort': '15min', 'type': 'CODE_SMELL', 'creationDate': '2020-03-02'}, 
# {'src': 'CodeJam:Services/FileBlogService.cs', 'severity': 'MAJOR', 'key': 'AXc45crkWnoiXpYu_wD-', 'startLine': 176, 'endLine': 176, 'status': 'OPEN', 'message': 'Split this method into two, one handling parameters check and the other handling the asynchronous code.', 'effort': '15min', 'type': 'CODE_SMELL', 'creationDate': '2020-02-25'}, 
# {'src': 'CodeJam:Services/FileBlogService.cs', 'severity': 'INFO', 'key': 'AXc45crkWnoiXpYu_wD8', 'startLine': 237, 'endLine': 237, 'status': 'OPEN', 'message': "Complete the task associated to this 'TODO' comment.", 'effort': '0min', 'type': 'CODE_SMELL', 'creationDate': '2020-02-25'}], 

# 'CodeJam:Controllers/BlogController.cs': 
# [{'src': 'CodeJam:Controllers/BlogController.cs', 'severity': 'MAJOR', 'key': 'AXc45cr4WnoiXpYu_wEC', 'startLine': 187, 'endLine': 187, 'status': 'OPEN', 'message': 'Split this method into two, one handling parameters check and the other handling the asynchronous code.', 'effort': '15min', 'type': 'CODE_SMELL', 'creationDate': '2020-02-25'}
# ]}


    styles = getSampleStyleSheet()


    pins = []

    for i in data:
        # print(i)
        pin1 = Pin()
        pin1.project = i
        pin1.message = Paragraph('''<font name="Courier-Bold" size=9 color="#525f7f"> {message} </font>'''.format(message=escape(data[i][0]["message"])), style=styles['Normal'])
        pin1.date = data[i][0]["creationDate"]
        pin1.error = f'L{data[i][0]["startLine"]}'
        pin1.types = data[i][0]["type"]
        pin1.serverity = data[i][0]["severity"]
        pin1.status = data[i][0]["status"]
        pin1.effort = f'{data[i][0]["effort"]} effort'
        pin1.cal = "src/static/img/issues_pdf/cal.png"
        pin1.line = "src/static/img/issues_pdf/error.png"
        if data[i][0]["type"] == "CODE_SMELL":
            pin1.typePath = 'src/static/img/issues_pdf/code_smell.png'
        elif data[i][0]["type"] == "BUG":
            pin1.typePath = 'src/static/img/issues_pdf/bug.png'
        else:
            pin1.typePath = 'src/static/img/issues_pdf/vulnerability.png'
        if data[i][0]["severity"] == "BLOCKER":
            pin1.serverityPath = 'src/static/img/issues_pdf/blocker.png'
        elif data[i][0]["severity"] == "CRITICAL":
            pin1.serverityPath = 'src/static/img/issues_pdf/critical.png'
        elif data[i][0]["severity"] == "MAJOR":
            pin1.serverityPath = 'src/static/img/issues_pdf/major.png'
        elif data[i][0]["severity"] == "MINOR":
            pin1.serverityPath = 'src/static/img/issues_pdf/minor.png'
        else:
            pin1.serverityPath = 'src/static/img/issues_pdf/info.png'
        if data[i][0]["status"] == "OPEN":
            pin1.statusPath = 'src/static/img/issues_pdf/open.png'
        elif data[i][0]["status"] == "CONFIRMED":
            pin1.statusPath = 'src/static/img/issues_pdf/confirmed.png'
        elif data[i][0]["status"] == "REOPENED":
            pin1.statusPath = 'src/static/img/issues_pdf/reopened.png'
        elif data[i][0]["status"] == "RESOLVED":
            pin1.statusPath = 'src/static/img/issues_pdf/resolved.png'
        else:
            pin1.statusPath = 'src/static/img/issues_pdf/closed.png'
        pin1.effortPath = 'src/static/img/issues_pdf/effort.png'
        pins.append(pin1)
        for x in range(1, len(data[i])):
            pin2 = Pin()
            pin2.project = ""
            pin2.message = Paragraph('''<font name="Courier-Bold" size=9 color="#525f7f"> {message} </font>'''.format(message=escape(data[i][x]["message"])), style=styles['Normal'])
            pin2.date = data[i][x]["creationDate"]
            pin2.error = f'L{data[i][x]["startLine"]}'
            pin2.types = data[i][x]["type"]
            pin2.serverity = data[i][x]["severity"]
            pin2.status = data[i][x]["status"]
            pin2.effort = f'{data[i][x]["effort"]} effort'
            pin2.cal = "src/static/img/issues_pdf/cal.png"
            pin2.line = "src/static/img/issues_pdf/error.png"

            if data[i][x]["type"] == "CODE_SMELL":
                pin2.typePath = 'src/static/img/issues_pdf/code_smell.png'
            elif data[i][x]["type"] == "BUG":
                pin2.typePath = 'src/static/img/issues_pdf/bug.png'
            else:
                pin2.typePath = 'src/static/img/issues_pdf/vulnerability.png'
            if data[i][x]["severity"] == "BLOCKER":
                pin2.serverityPath = 'src/static/img/issues_pdf/blocker.png'
            elif data[i][x]["severity"] == "CRITICAL":
                pin2.serverityPath = 'src/static/img/issues_pdf/critical.png'
            elif data[i][x]["severity"] == "MAJOR":
                pin2.serverityPath = 'src/static/img/issues_pdf/major.png'
            elif data[i][x]["severity"] == "MINOR":
                pin2.serverityPath = 'src/static/img/issues_pdf/minor.png'
            else:
                pin2.serverityPath = 'src/static/img/issues_pdf/info.png'
            if data[i][x]["status"] == "OPEN":
                pin2.statusPath = 'src/static/img/issues_pdf/open.png'
            elif data[i][x]["status"] == "CONFIRMED":
                pin2.statusPath = 'src/static/img/issues_pdf/confirmed.png'
            elif data[i][x]["status"] == "REOPENED":
                pin2.statusPath = 'src/static/img/issues_pdf/reopened.png'
            elif data[i][x]["status"] == "RESOLVED":
                pin2.statusPath = 'src/static/img/issues_pdf/resolved.png'
            else:
                pin2.statusPath = 'src/static/img/issues_pdf/closed.png'
            pin2.effortPath = 'src/static/img/issues_pdf/effort.png'
            pins.append(pin2)

    fileName = 'src/static/downloads/pdf/Issues.pdf'
    pdf = SimpleDocTemplate(
        fileName,
        pigesize=letter
    )



    # Generate Pins
    tables = []
    for i in pins:
        p1 = genPinTable(i)
        tables.append([p1])

# p1 = genPinTable(pins[0])
# p2 = genPinTable(pins[1])
# p3 = genPinTable(pins[2])
# p4 = genPinTable(pins[3])
# p5 = genPinTable(pins[4])

# Add all pins to the table

    mainTable = Table(tables)

# mainTable = Table([
    # [p1],
    # [p2],
    # [p3],
    # [p4],
    # [p5]
# ])

    mainTableStyle = TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        
    ])
    mainTable.setStyle(mainTableStyle)


    elems = []
    elems.append(mainTable)
    pdf.build(elems)




# for i in pins:
#     print(i.project)
#     print(i.message)
#     print(i.date)
#     print(i.error)
#     print(i.types)
#     print(i.serverity)
#     print(i.status)
#     print(i.effort)
#     print(i.cal)
#     print(i.line)
#     print(i.typePath)
#     print(i.serverityPath)
#     print(i.statusPath)
#     print(i.effortPath)
#     print('--------------------')


# Data
# def getPins():
    # pin1 = Pin()
    # pin1.project = "CodeJam:Services/FileBlogService.cs"
    # pin1.message = "This is an error message. This is an error message"
    # pin1.date = "2018-03-18"
    # pin1.error = 'L4'
    # pin1.types = 'Vulnerability'
    # pin1.serverity = "Info"
    # pin1.status = "Open"
    # pin1.effort = "1min effort"
    # pin1.cal = "src/static/img/issues_pdf/cal.png"
    # pin1.line = "src/static/img/issues_pdf/error.png"
    # pin1.typePath = 'src/static/img/issues_pdf/vulnerability.png'
    # pin1.serverityPath = 'src/static/img/issues_pdf/info.png'
    # pin1.statusPath = 'src/static/img/issues_pdf/open.png'
    # pin1.effortPath = 'src/static/img/issues_pdf/effort.png'

    # pin2 = Pin()
    # pin2.project = "CodeJam:Services/FileBlogService.cs"
    # pin2.message = "This is an error message. This is an error message"
    # pin2.date = "2018-03-18"
    # pin2.error = 'L4'
    # pin2.types = 'Code Smell'
    # pin2.serverity = "Minor"
    # pin2.status = "Confirmed"
    # pin2.effort = "1min effort"
    # pin2.cal = "src/static/img/issues_pdf/cal.png"
    # pin2.line = "src/static/img/issues_pdf/error.png"
    # pin2.typePath = 'src/static/img/issues_pdf/code_smell.png'
    # pin2.serverityPath = 'src/static/img/issues_pdf/minor.png'
    # pin2.statusPath = 'src/static/img/issues_pdf/confirmed.png'
    # pin2.effortPath = 'src/static/img/issues_pdf/effort.png'

    # pin3 = Pin()
    # pin3.project = "CodeJam:Services/FileBlogService.cs"
    # pin3.message = Paragraph(''' <font name="Courier-Bold" size=9 color="#525f7f"> Rename namespace SimplCommerce.Module.Pricing.Models so that it no longer conflicts with the reserved language keyword 'Module'. Using a reserved keyword as the name of a namespace makes it harder for consumers in other languages to use the namespace.</font>''', style=styles['Normal'])
    # pin3.date = "2018-03-18"
    # pin3.error = 'L4'
    # pin3.types = 'Bug'
    # pin3.serverity = "Major"
    # pin3.status = "Reopened"
    # pin3.effort = "1min effort"
    # pin3.cal = "src/static/img/issues_pdf/cal.png"
    # pin3.line = "src/static/img/issues_pdf/error.png"
    # pin3.typePath = 'src/static/img/issues_pdf/bug.png'
    # pin3.serverityPath = 'src/static/img/issues_pdf/major.png'
    # pin3.statusPath = 'src/static/img/issues_pdf/reopened.png'
    # pin3.effortPath = 'src/static/img/issues_pdf/effort.png'

    # pin4 = Pin()
    # pin4.project = ""
    # pin4.message = Paragraph(''' <font name="Courier-Bold" size=9 color="#525f7f"> Rename namespace SimplCommerce.Module.Pricing.Models so that it no longer conflicts with the reserved language keyword 'Module'. Using a reserved keyword as the name of a namespace makes it harder for consumers in other languages to use the namespace.</font>''', style=styles['Normal'])
    # pin4.date = "2018-03-18"
    # pin4.error = 'L4'
    # pin4.types = 'Bug'
    # pin4.serverity = "Critical"
    # pin4.status = "Resolved"
    # pin4.effort = "1min effort"
    # pin4.cal = "src/static/img/issues_pdf/cal.png"
    # pin4.line = "src/static/img/issues_pdf/error.png"
    # pin4.typePath = 'src/static/img/issues_pdf/bug.png'
    # pin4.serverityPath = 'src/static/img/issues_pdf/critical.png'
    # pin4.statusPath = 'src/static/img/issues_pdf/resolved.png'
    # pin4.effortPath = 'src/static/img/issues_pdf/effort.png'

    # pin5 = Pin()
    # pin5.project = ""
    # pin5.message = Paragraph(''' <font name="Courier-Bold" size=9 color="#525f7f"> Rename namespace SimplCommerce.Module.Pricing.Models so that it no longer conflicts with the reserved language keyword 'Module'. Using a reserved keyword as the name of a namespace makes it harder for consumers in other languages to use the namespace.</font>''', style=styles['Normal'])
    # pin5.date = "2018-03-18"
    # pin5.error = 'L4'
    # pin5.types = 'Bug'
    # pin5.serverity = "Blocker"
    # pin5.status = "Closed"
    # pin5.effort = "1min effort"
    # pin5.cal = "src/static/img/issues_pdf/cal.png"
    # pin5.line = "src/static/img/issues_pdf/error.png"
    # pin5.typePath = 'src/static/img/issues_pdf/bug.png'
    # pin5.serverityPath = 'src/static/img/issues_pdf/blocker.png'
    # pin5.statusPath = 'src/static/img/issues_pdf/closed.png'
    # pin5.effortPath = 'src/static/img/issues_pdf/effort.png'
    

    # return [pin1, pin2, pin3, pin4, pin5]
