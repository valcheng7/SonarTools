from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def makeProjectsIssues(data):

    fileName = 'src/static/downloads/pdf/Project_issues.pdf'
    pdf = SimpleDocTemplate(
        fileName,
        pagesize=letter
    )

    # Create Table with data
    table = Table(data)

    # Style Table
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), '#5e72e4'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1, -1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige)
    ])

    table.setStyle(style)

    # Alternare Background Color
    rowNum = len(data)
    for i in range(1, rowNum):
        if i % 2 == 0:
            bc = colors.whitesmoke
        else:
            bc = '#E9EBF5'
        alternateRow = TableStyle([
            ('BACKGROUND', (0,i), (-1,i), bc)
        ])
        table.setStyle(alternateRow)

    # Add Borders
    border_style = TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.white)
    ])
    table.setStyle(border_style)

    # Append list of table to list of elements for pdf to build
    elems = []
    elems.append(table)

    # Build PDF with the list of elements
    pdf.build(elems)


# data = [
#     ['Project', 'Status', 'Bugs', 'Vulnerabilities', 'Hotspots', 'Code Smells', 'Coverage', 'Duplications', 'Language'],
#     ['Argon Design System', 'Passed', '12', '0', '3.6', '500', '0%', '2.9%', '4.2k'],
#     ['Argon Design System', 'Passed', '12', '0', '3.6', '500', '0%', '2.9%', '4.2k'],
#     ['Argon Design System', 'Passed', '12', '0', '3.6', '500', '0%', '2.9%', '4.2k']
#     ]

# makeProjectsIssues(data)


