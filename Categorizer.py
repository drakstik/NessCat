import pandas as pd
import sys
import time
from tabulate import tabulate

import Template
import UI


# Setting pandas options to show full dataframe.
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def clean_up(raw_scan_DF):
    # Select the duplicated rows in the raw scan.
    # duplicated = raw_scan_DF[raw_scan_DF.duplicated()]

    # # Then there are duplicated rows.
    # if duplicated.shape[0] > 0: 
        
    #     # Drop the duplicated rows.
    #     raw_scan_DF = raw_scan_DF.drop_duplicates().reset_index(drop=True)
        
    #     # Create a filename to store the duplicated rows under.
    #     filename = 'Duplicated_' + str(int(time.time())) + '.csv'
        
    #     # Save the duplicated rows into a csv.
    #     duplicated.to_csv(filename, index=False)
        
    #     # Warn the user that some rows were duplicated, therefor dropped, and that the rows were saved in a file.
    #     print('\n\33[31m' + str(duplicated.shape[0]) + '\33[0m rows were duplicated and dropped from the raw scan. ' \
    #         + filename + ' contains those duplicated rows.')
    
    # Lower characters and strip spaces of the string values in the Name column.
    raw_scan_DF = lower_and_strip(raw_scan_DF, cols=['Name'])
    
    # Select useful columns.
    raw_scan_DF = raw_scan_DF[['Risk', 'CVE', 'Host', 'Port', 'Name', 'Description', 'Solution','See Also' , 'Plugin Output']]
    
    # Select rows with relevant risk.
    relevant_scan_DF = raw_scan_DF[raw_scan_DF['Risk'] != "None"]
    
    # Find the number of raw scan rows that have a Severity of None.
    num_severity_none = raw_scan_DF.shape[0] - relevant_scan_DF.shape[0]

    if num_severity_none > 0: # Then some rows were irrelevant.

        # Warn the user that some rows were of irrelevant severity and that they were dropped.
        print('\n\33[31m' + str(num_severity_none) + '\33[0m rows were of irrelevant severity and dropped from the raw scan.')
    
    pd.set_option('mode.chained_assignment', None)
    # Combine Port and Host into one column called 'Affected System'
    relevant_scan_DF.loc[:,'Affected System'] = relevant_scan_DF['Host'].astype(str) + ':' + relevant_scan_DF['Port'].astype(str)
            
    # Combine Solution and See Also into one column called 'Solution'
    relevant_scan_DF.loc[:,'Solution'] = relevant_scan_DF['Solution'].astype(str) + ' See also [' + relevant_scan_DF['See Also'].str.replace('\n',', ').astype(str) + ']'
    pd.set_option('mode.chained_assignment', 'warn')
    
    # Drop the Host, Port and See Also columns.
    relevant_scan_DF = relevant_scan_DF[['Risk', 'Affected System', 'Name', 'CVE', 'Description', 'Solution', 'Plugin Output']]
    
    # Rename Risk column to Severity.
    relevant_scan_DF.columns = ['Severity', 'Affected System', 'Name', 'CVE', 'Description', 'Solution', 'Plugin Output']
    
    # Select for duplicated rows, again.
    duplicated = relevant_scan_DF[relevant_scan_DF.duplicated()]

    # There are duplicated rows, after selecting columns and relevant rows.
    if duplicated.shape[0] > 0: 
        
        # Drop the duplicated rows.
        relevant_scan_DF = relevant_scan_DF.drop_duplicates().reset_index(drop=True)
        
        # Create a filename to store the duplicated rows in.
        filename = 'Duplicated_2' + str(int(time.time())) + '.csv'
        
        # Save the duplicated rows into a csv.
        duplicated.to_csv(filename, index=False)
        
        # Warn the user that some rows were duplicated, therefor dropped, and that the rows were saved in a file.
        print('\n\33[31m' + str(duplicated.shape[0]) + '\33[0m rows were duplicated,' \
            + ' after selecting relevant columns and rows, and dropped from the raw scan. ' \
            + filename + ' contains those duplicated rows.')

    
    # Tell the user how many rows are left, after clean up.
    print('\nOnly \33[01m' + str(relevant_scan_DF.shape[0]) + '\33[0m rows left after clean up.\n')
    
    relevant_scan_DF.to_csv('test3.csv')
    
    return relevant_scan_DF

# [] Summarize a Categorized file.

#     1. Count "Affected Systems" per type of vulnerability [DONE]
#     2. Count "Affected Systems" per "Severity" values []
#     3. Unique "Solution" values per "Affected System"
#     4. List "Affected Systems" per type of vulnerability
def summarize(filename):
    fn = 'REPORT_SUMMARY_' + str(int(time.time())) + '.txt'
    f = open(fn, 'w')
    
    f.write('-----------------------------------------REPORT SUMMARY-----------------------------------------')
    print('\n-----------------------------------------' + UI.colors.Process_Headers \
        + 'REPORT SUMMARY' + UI.colors.reset +  '-----------------------------------------')

    categorized_df = pd.read_csv(filename, index_col=False)

    unique_systems = pd.unique(categorized_df['Affected System'])
    unique_systems.sort

    f.write('\n\n' + str(categorized_df.shape[0]) + ' vulnerabilities were discovered accross these ' \
        + str(len(unique_systems)) + ' unique systems:')
    print('\n' + str(categorized_df.shape[0]) + ' vulnerabilities were discovered accross these ' \
        + str(len(unique_systems)) + ' unique systems:')
    
    for system in unique_systems:
        f.write('\n - ' + system)
        print(' - ' + system)

    
    unique_severities = pd.unique(categorized_df['Severity'])

    f.write('\n\n-----------------------------------------SEVERITY REPORT-----------------------------------------')
    print('\n-----------------------------------------' + UI.colors.Informational_Headers + 'SEVERITY REPORT' + UI.colors.reset + '-----------------------------------------')
    
    for severity in unique_severities:
        a = categorized_df[categorized_df['Severity'] == severity]
        f.write('\n' + str(a.shape[0]) + ' of ' + str(categorized_df.shape[0]) + ' vulnerabilities were of \'' + severity + '\' severity.')
        print(str(a.shape[0]) + ' of ' + str(categorized_df.shape[0]) + ' vulnerabilities were of \'' + severity + '\' severity.')
        
    unique_categories = pd.unique(categorized_df['Category'])
    
    f.write('\n\n-----------------------------------------LIST OF CATEGORIES FOUND-----------------------------------------')
    print('\n-----------------------------------------' + UI.colors.Informational_Headers \
    + 'LIST OF CATEGORIES FOUND' + UI.colors.reset + '-----------------------------------------')
    
    count = 1
    for unique_category in unique_categories:
        f.write('\n(' + str(count) + ') ' + str(unique_category))
        print('(' + str(count) + ') ' + str(unique_category))
        count+=1

    count = 1
    for unique_category in unique_categories:
        f.write('\n\n-----------------------------------------(' + str(count) + ') ' \
            + str(unique_category) + '-----------------------------------------')
        print('\n-----------------------------------------' + UI.colors.Informational_Headers + '(' + str(count) + ') ' \
            + str(unique_category) + UI.colors.reset + '-----------------------------------------')
        count+=1
        
        a = categorized_df[categorized_df['Category'] == unique_category]
        
        f.write('\n\n' + str(len(pd.unique(a['Affected System']))) + ' of ' + str(len(unique_systems)) \
            + ' systems were affected by vulnerabilities of category \'' + unique_category + '\':')
        print('\n' + str(len(pd.unique(a['Affected System']))) + ' of ' + str(len(unique_systems)) \
            + ' systems were affected by vulnerabilities of category \'' + unique_category + '\':')
        
        f.write('\n\nList of unique Names:')
        print('\nList of unique Names:')
        
        c = 1
        for n in pd.unique(a['Name']):
            f.write('\n ' + str(c) + '. ' + n)
            print(' ' + str(c) + '. ' + n)
            c+=1

        f.write('\n\nList of unique Affected Systems:')
        print('\nList of unique Affected Systems:')
        
        c = 1
        for ip in pd.unique(a['Affected System']):
            f.write('\n ' + str(c) + '. ' + ip)
            print(' ' + str(c) + '. ' + ip)
            c+=1
        
        f.write('\n\nList of unique Solutions:')
        print('\nList of unique Solutions:')
        
        c = 1
        for s in pd.unique(a['Solution']):
            f.write('\n ' + str(c) + '. ' + s)
            print(' ' + str(c) + '. ' + s)
            c+=1
        
        a = a[['Affected System', 'Severity', 'Name', 'Solution']].sort_values('Name')
        
        a['Solution'] = a['Solution'].str.replace('\n',' ')
        a = a.sort_values('Severity')
        
        # b = a.set_index(['Name', 'Severity']).sort_index()
        
        f.write('\n\nHere are the specific names of the ' + unique_category + ', their CVE and Affected Systems:\n\n')
        f.write(tabulate(a, headers='keys', showindex=True, tablefmt='fancy_grid'))
        print('\nHere are the specific names of the ' + unique_category + ', their CVE and Affected Systems:\n\n',tabulate(a, headers='keys', showindex=True, tablefmt='fancy_grid'))
        
        # print('\nHere are the solutions for each vulnerability:\n')
        # for idx, row in b.itterrows():
        #     print('Solution for \"' + UI.colors.Names + row['Name'] + UI.colors.reset + '\": ' + row['Solution'])
    

    return


# This function is ran in the main function to categorize a raw scan dataframe.
def categorize(raw_scan_DF):

    # Clean up the raw scan. 
    clean_scan_DF = clean_up(raw_scan_DF)
    
    # Retrieve a template.
    t = Template.Template()
    
    # Use the template to categorize the clean raw scan.
    categorized, modified_template = t.categorize_scan_table(clean_scan_DF)

    # Then some rows were categorized.
    if categorized.shape[0] > 0:
        
        # Then the Template was modified.
        if modified_template:
            
            # Create a filename for categorized rows that mentions that the Template was modified.
            filename = 'Categorized_Modified_' + str(int(time.time())) + '.csv'

        # Then the Template was NOT modified.
        else:
            
            # Create a filename for categorized rows.
            filename = 'Categorized_' + str(int(time.time())) + '.csv'
        
        # Save categorized rows to a csv file.
        categorized.to_csv(filename, index=False)

        # Tell user that categorized rows were saved.
        print(UI.colors.Saved_files + 'Saved categorized rows as \"' + filename + '\".' + UI.colors.reset)

    summarize(filename)


# Init function.
def main():

    # Collect the arguments provided by the user in the terminal command.
    args = sys.argv[1:] 

    # Then the user forgot to provide a filename.
    if len(args) == 0:

        # Ask the user to give us the name of the file. File should be in this directory.
        print('You forgot to provide a filename as an argument.')

    # Then the user did provide filenames.
    else:

        # Create an empty DataFrame.
        raw_scan_DF = pd.DataFrame()

        # Turn each of the filenames into a DataFrame, and append them to the empty DataFrame above. 
        for filename in args:

            # Turn the csv file into a DataFrame.
            file_DF = pd.read_csv(filename, index_col=False)


            # if (raw_scan_DF.shape[0] > 0):
            #     if list(raw_scan_DF.columns) != list(file_DF.columns):
            #         # This error is usually caused by new columns created by Tenable, such as:
            #         #   1. When CVSS V2 was changed to CVSS V3.
            #         print(UI.colors.Saved_files + 'Multiple raw scans were given as input, and their columns do not match!\33[0m' \
            #             + '\n   Please contact David Mberingabo if you see this error.\n' + UI.colors.reset)
            
            # Append the file DataFrame to the initially empty DataFrame.
            raw_scan_DF = raw_scan_DF.append(file_DF, ignore_index=True)
        
        # Categorize all the filenames as one big DataFrame.
        categorize(raw_scan_DF)


if __name__ == "__main__":
    main()

# summarize('Categorized_1639997116.csv')