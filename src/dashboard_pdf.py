from src.api import sonarAPI
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import matplotlib
from matplotlib.figure import Figure
from matplotlib import *
import matplotlib.backends.backend_pdf

def dashboard_PDF(login, password):
    client = sonarAPI(login,password)
    df = pd.DataFrame(client.allProject())

    matplotlib.rcParams['figure.subplot.right'] = 0.78

    df["maintainabilityRating"] = df["maintainabilityRating"].astype(float)
    df["code_smells"] = df["code_smells"].astype(int)
    df["Lines of Code"] = df["lines"]
    df["Project Name"] = df["projectName"]
    df["Maintainability Effort"] = df["maintainabilityEffort"].astype(int)
    df["Code smells"] = df["code_smells"].astype(int)
    df["Security Effort"] = df["securityEffort"].astype(int)
    df["Vulnerabilities"] = df["vulnerabilities"].astype(int)
    df["Reliability Effort"] = df["reliabilityEffort"].astype(int)
    df["Bugs"] = df["bugs"].astype(int)
    df["Duplication Percentage"] = df["duplicatePercentage"].astype(float)
    df["totalIssues"] = df["code_smells"].astype(int) + df["bugs"].astype(int) + df["vulnerabilities"].astype(int)
    df["bugs"] = df["bugs"].astype(int)
    df["vulnerabilities"] = df["vulnerabilities"].astype(int)
    df["code_smells"] = df["code_smells"].astype(int)

    ## Bar Chart ##
    sns.set() 
    plt.figure(figsize=(20,5), dpi=100)
    plt.title("Total number of issues for each project", fontsize = 25) # title of scatter plot
    sns.barplot(x = "totalIssues", y = "projectName", data = df,) 
    plt.grid()

    ## Pie Chart ##
    sns.set()
    plt.figure(figsize=(20,5))
    explode = (0, 0, 0)
    # Total number of bugs for all project combined 
    bugs = int(df["bugs"].sum())
    # Total number of vulnerabilties for all projects combined
    vulnerabilities = int(df["vulnerabilities"].sum())
    # Total number of code smells for all projects combined
    codeSmells = int(df["code_smells"].sum())
    labels = ["Bugs", "Vulnerabilities", "Code Smells"]
    values = [bugs, vulnerabilities, codeSmells]
    #add colors
    colors = ['#66b3ff','#ff9999','#99ff99','#ffcc99']
    plt.pie(values, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')
    plt.tight_layout()
    plt.title("Type of errors", fontsize = 20) # title of scatter plot

    ## Relibability Chart ##
    sns.set()
    plt.figure(figsize=(20,10), dpi=100)
    # create scatter plot
    sns.scatterplot(x = "Lines of Code", y = "Bugs", size="Reliability Effort", data = df, hue = "Project Name", palette = "magma")
    plt.title("Perspective: Reliability", fontsize = 25) # title of scatter plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    ## Security Chart ##
    plt.figure(figsize=(20,10), dpi=100)
    line = sns.scatterplot(x = "Lines of Code", y = "Vulnerabilities", size="Security Effort", data = df, hue = "Project Name", palette = "magma")
    plt.title("Perspective: Security", fontsize = 25) # title of scatter plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    ## Maintainbility Chart ##
    sns.set() 
    plt.figure(figsize=(20, 10), dpi=100)
    plt.title("Perspective: Maintainqbility", fontsize = 25) # title of scatter plot
    # create scatter plot
    sns.scatterplot(x = "Lines of Code", y = "Code smells", size="Maintainability Effort", data = df, hue = "Project Name", palette = "magma")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    ## Duplication Chart ##
    plt.figure(figsize=(20,10), dpi=100)
    sns.scatterplot(x = "Lines of Code", y = "Duplication Percentage", size="duplicated_blocks", data = df, hue = "Project Name", palette = "magma")
    plt.title("Perspective: Duplication", fontsize = 25) # title of scatter plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')


    pdf = matplotlib.backends.backend_pdf.PdfPages("dashboard.pdf")
    for fig in range(1, plt.gcf().number + 1): ## will open an empty extra figure :(
        pdf.savefig( fig , bbox_inches='tight' )
    pdf.close()
    message.txt
    return "done"
