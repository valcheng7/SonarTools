from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Frame, Image, TableStyle, Table, PageBreak, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import utils
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 

# Variables ----------------------------------------------------------------------------------------------------------



def get_image(path, width=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

def createIssuesPDF2(langData, raw):

    styles = getSampleStyleSheet()

    pdfmetrics.registerFont(
        TTFont('abc', 'BAHNSCHRIFT.TTF')
    )

    fileName = 'src/static/downloads/created_pdf/issues2.pdf'
    pdf = SimpleDocTemplate(
        fileName,
        pagesize=letter
    )

    # Language Table Title -----------------------------------------------------

    langTitle = "Number of lines for each language"

    languageTitle = Paragraph('''<font name="abc" size=12 color="#000000"> <strong>{message} </strong></font>'''.format(message=langTitle), style=styles['Normal'])

    titleTable = Table([
            [languageTitle]
        ], 490, rowHeights=(0.9*cm))

    titleTableStyle = TableStyle([
        # ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (0,0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0,0), (1,-1), 0),
        ('VALIGN', (0,0), (-1, -1), 'TOP'),
    ])

    titleTable.setStyle(titleTableStyle)


    langTable = Table(langData, 104, rowHeights=(0.9*cm), hAlign='LEFT')

    langTableStyle = TableStyle([
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

    langTable.setStyle(langTableStyle)


    lTitleTable = Table([
            [titleTable],
            [langTable]
        ], 500)

    lTitleTableStyle = TableStyle([
        # ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])

    lTitleTable.setStyle(lTitleTableStyle)

    langTableAlign = Table([[lTitleTable]], 550)

    langTableAlignStyle = TableStyle([
            # ('GRID', (0,0), (-1,-1), 1, colors.black)
        ])

    langTableAlign.setStyle(langTableAlignStyle)

    dataset = pd.DataFrame([{'Language':j,"No. of lines":int(raw[j][0])} for j in raw])

    sns.catplot(x="No. of lines", y='Language', data=dataset, kind='bar',)
    plt.savefig('src/static/img/issues_pdf/language.png', bbox_inches='tight')


    langGraph = get_image("src/static/img/issues_pdf/language.png", width=10*cm)
    langGraphTable = Table([[langGraph]], 550)
    langGraphStyle = TableStyle([
            # ('GRID', (0,0), (-1,-1), 1, colors.black)
        ])

    langGraphTable.setStyle(langGraphStyle)


    s = Spacer(1, 0.5*cm)



    elems = []
    elems.append(langTableAlign)
    elems.append(s)
    elems.append(langGraphTable)
    # elems.append(topTable)



    # Build PDF with the list of elements


    pdf.build(elems)





# from src.api import sonarAPI

# client = sonarAPI("180972B","08032021")

# raw = client.getProjectLanguages(f'codecoverage')
# print(raw, type(raw))
# data = [[j,int(raw[j][0])] for j in raw]
# data.insert(0, ["Languages", "No. of lines"])

# createIssuesPDF2(data, raw)

