# How To Install NessCat
Simply run clone this repository to your local machine and ensure the requirements below are fulfilled before running the tool.

# Requirements
## Python3
All users will require Python3 to be installed on their machine, including latest versions of Pandas, sys, time, subprocess and other libraries required. Make sure you read the given errors so you can install the required python3 and its libaries.
## Git and GitHub Account (For Template Keepers only.)
Template Keepers will need a GitHub account with their Template stored in a public repository.
## Windows or Linux
This manual assumes you are using a Windows or Linux machine that has access to the GitHub; and any other Git or Python 3 dependencies.
## wget
This manual assumes you have installed the wget command on you machine.
## tabulate (Python Library)
## pandas (Python Library)

# Design
## The Template
The Template is composed of a Name and Category column. It is used as a reference to auto-categorize a New Nessus Scan. It is stored online to track and maintain any changes made to it accross all machines. Changes to the Template should be go through rigorous examination and should require a good level of awareness and agreement amongst the Template Keepers, in order to avoid categorization errors and conflicts, as well as poor service.
## The Categorizer
The Categorizer is responsible of auto-categorizing a New Nessus Scan. During the automated categorization, the Categorizer may come across new names and new categories.

# How to Use and Types of Users
## 1. Template-Keepers
These users have authorized write access to both the online and offline Templates. They can update the Template with proposed changes or archived categorized scans. Here are some usage examples:

`python3 ./Template.py <Proposed_Changes_1.csv> <Historical_Scan_1.csv> ...` 

## 2. Categorizers
These users can categorize and summarize uncategorized Nessus scan results using the online Template. They can also create proposed changes to their Working Template.

`python3 ./Categorizer <Uncategorized_Scan_1.csv> <Uncategorized_Scan_2.csv> ...`

## 3. How to Initialize Template
Please watch the attached demo video on Template.py. 

# Code
This section will explain how the code works and how the user activity flow should go. In cases where the user activity flow is stuck, simply quit
## Template
## Categorizer

# CSV Files Involved
This section discusses the data structures and files used in this project.
## Template
There are two templates.
### Working Template:
The DataFrame that is temporarily created as long as Categorizer.py is running.
### Template.csv:
A csv file stored on a Template-Keeper's GitHub that can only be updated by a Template-Keeper with the right authentication.
## Uncategorized Nessus Scan:
This is a Nessus scan csv that has not been categorized yet.
## Categorized_xxxxxxxxxx.csv:
This is a Nessus scan csv that has been categorized using the Online Template. This is the output of Categorizer.py.
## Categorized_Locally_xxxxxxxxxx.csv:
This is a Nessus scan csv that has been categorized using the Local Template. This should not be presented to the client, wiretrieve_command = ['wget', 'https://raw.githubusercontent.com/drakstik/Template/main/Template.csv']
        # remove_template = ['rm', 'Template.csv']
        # if exists('Template.csv'):
        #     retrieve_commands = [remove_template, retrieve_command]
        # else:
        #     retrieve_commands = [retrieve_command]
        # # Run the retrieve command.
        # for c in retrieve_commands:
        #     terminal(c, '-----------------------------------------' + UI.colors.Process_Headers \
        #         + 'DOWNLOADING THE TEMPLATE' + UI.colors.reset + '----------------------------------------')thout Template Keeper approval.
## Proposed_Changes_xxxxxxxxxx.csv:
These are the changes made to the Local Template that are made by a Categorizer and sent to a Template-Keeper to update the Online Template. Columns required: [Name, Category]











# TODO
[DONE] Accept multiple Proposed Changes or Historical Scans, when updating the template.

    1. python3 Template.py 'Historical Nessus Scan_1.csv' 'Historical Nessus Scan_2.csv' 'Porposed Changes.csv'

[DONE] Summarize a Categorized file. 
    
    0. Total number of vulnerabilities and affected systems.
    1. List all Affected Systems
    2. Count vulnerabilities for each severity.
    3. List and count Affected systems per Category.
    4. List of Affected System and CVE for each vulnerability Name. (Files)
    5. List of each vulnerability Name, Description and its Solution. (Files)

[] Color coordinate and format the different aspects of the process:
    
    1. Questions: \033[92m, bold at the end.
    2. Tables (use tabulate library https://www.geeksforgeeks.org/display-the-pandas-dataframe-in-table-style/): \033[40m, tabulate(df, headers='keys', showindex=True, tablefmt='fancy_grid')
    3. Saved files: \033[95m
    4. Informational Headers (Gives information for decision making): \033[96m\33[4m, all caps.
    5. Process Headers (indicates which part of the process you are in): \033\1m\033[7m
    6. Errors: \033[31m
    7. Categories = fgBlue
    8. Names = fgYellow

[] Check requirements before running them.
    - Check OS requirements
    - Check wget requirements
    - Check Git requirements
    - Python3 and libraries have their own requirement checking, so no need to check these ones.

[] Optomize this tool for windows:
    - All terminal commands must be in the windows cmd script language.

[] Check with co-workers if it fulfills their needs.

[] Make an activity flow chart and tutorial videos.

[] Ensure the template is the most updated version by adding all the historical scans to it (See Bolu for these historical scans).

[] How many Nessus (Tenable) vulnerability names are there anyways? How many new ones per year?

[] Read about "Feature Extraction/Engineering" for NLP (and "count vectorizer", "fit on text", "tokenization", "Word Embeding", "tf-idf").

[] Use database instead of csv for the Template.

[] Read up on Flask web-app framework.

[] Should you give it for free to KPMG???

USER MANUAL:

If you want to update the template, by rewriting some rows, then do it manually. But if you want to update the template by appending new rows,
use the 
    $ `python3 Template.py 'new rows.csv'`


The user can create a categorized or categorized_modded file. Categorized_modded files are accompanied by Proposed Changes files.
