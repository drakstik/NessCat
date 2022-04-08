import pandas as pd
import time as time
import sys
import subprocess
import UI
from os.path import exists
from tabulate import tabulate
import platform

# Setting pandas options to show full dataframe.
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 100)

# Run the given command in the terminal and return the output.
def terminal(command, msg):
    res = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, _error = res.communicate()

    if not _error:
        print(msg)
    else:
        print(_error)
    
    return str(output)[2:-1]


def check_system_requirements():
    OS = platform.system()

    if OS == 'Windows':
        print('This application has not been optimized for Windows, yet. Please try running it in a Virtual Machine or Windows Subsystem for Linux')
        
        # Check for wget.
        output = terminal(['wget', '--version'], '')
        if output[0:8] == 'GNU Wget':
            print('wget requirement check passed successfully.')
        else:
            print('wget requirement check failed, so you might encounter issues when downloading the template.')
    
    elif OS == 'Linux':
        print('OS requirement check passed successfully.')

        # Check for wget.
        output = terminal(['wget', '--version'], '')
        if output[0:8] == 'GNU Wget':
            print('wget requirement check passed successfully.')
        else:
            print('wget requirement check failed, so you might encounter issues when downloading the template.')
    
    output = terminal(['git','--version'],'')
    
    if output[0:11] == 'git version':
        print('Git requirement check passed successfully.')
    else:
        print('Git may not be installed on this computer, so this tool might not work as intended when it comes to uploading the template.')


    return OS


# Returns true if given string s is a number (0, 1, -1.33, 1e10).
# Implementation of isNumber() function
def is_number(s):
     
    # handle for negative values
    negative = False
    if(s[0] =='-'):
        negative = True
         
    if negative == True:
        s = s[1:]
     
    # try to convert the string to int
    try:
        n = int(s)
        return True
    # catch exception if cannot be converted
    except ValueError:
        return False

# df is assumed to be a dataframe with all string values.
# df's values in columns 'cols' are stripped of spaces and its characters all lowered.
def lower_and_strip(df, cols):
    pd.set_option('mode.chained_assignment', None)
    for col in cols:
        df.loc[:,col] = df[col].str.lower()
        df.loc[:,col] = df[col].str.strip()
        df.loc[:,col] = df[col].str.replace('\n', ' ')
    pd.set_option('mode.chained_assignment', 'warn')
    return df  


class Template:

    # Defines how a template shall be initialized.
    def __init__(self):
        # Terminal commands required.
        retrieve_command = ['wget', 'https://raw.githubusercontent.com/drakstik/Template/master/Template.csv']
        remove_template = ['rm', 'Template.csv']
        if exists('Template.csv'):
            retrieve_commands = [remove_template, retrieve_command]
        else:
            retrieve_commands = [retrieve_command]
        # Run the retrieve command.
        for c in retrieve_commands:
            terminal(c, '-----------------------------------------' + UI.colors.Process_Headers \
                + 'DOWNLOADING THE TEMPLATE' + UI.colors.reset + '----------------------------------------')
        # The template's filename.
        self.template_filename = 'Template.csv' 
        # The template as a DataFrame.
        self.working_template = pd.read_csv(self.template_filename, index_col=False)
        # The changes the user makes during manual categorization of uncategorized names.
        self.changes = pd.DataFrame(columns=['Name', 'Category'])

        

    # A function that raises a value error and gives a hint.
    def value_error(self, hint = ''):
        if hint == '':
            print(UI.colors.Errors + 'WRONG VALUE ENTERED:' + UI.colors.reset + ' you entered the wrong value')
        else:
            print(UI.colors.Errors + 'WRONG VALUE ENTERED:' + UI.colors.reset + hint)

    # A function that if a name is categorizeable and uncategorizeable.
    # params:
    #        name = a Nessus vulnerability name.
    # Returns:
    #        True or False = categorizeable or uncategorizeable
    #        categorization = row from working_template with name (only if name is categorizeable) 
    def is_name_in_template(self, name):
        if name in list(self.working_template['Name']):
            return (True, list(self.working_template[self.working_template['Name'] == name]['Category'])[0])
        else:
            return (False,)

    # A function that seperates tables into categorizeable and uncategorizeable.
    # Params:
    #        rows = DataFrame with column [Name], at least.
    # Returns:
    #        categorizeable = DataFrame with column [Name], at least.
    #        uncategorizeable = DataFrame with column [Name], at least.
    def is_categorizeable(self, scan_results):
        categorizeables = pd.DataFrame()
        uncategorizeables = pd.DataFrame()
        already_in_template = {}
        for idx, row in scan_results.iterrows():
            # print(idx)
            name = row['Name']
            name_is_in_template = self.is_name_in_template(name)
            if name_is_in_template[0]:
                # Add the 'Template Category' for update_template
                row['Template Category'] = name_is_in_template[1]
                categorizeables = categorizeables.append(row, ignore_index=True)
                already_in_template[name] = name_is_in_template[1]
            else:
                uncategorizeables = uncategorizeables.append(row, ignore_index=True)
        return categorizeables, uncategorizeables, already_in_template

    # A function that saves changes to a file.
    def save_changes(self):
        ans = input(UI.colors.Questions + '\nWould you like to save the changes as a seperate file? (y|n) > ' + UI.colors.reset)
        rtrn = 1
        while(True):
            if ans == 'y':
                # Naming the proposed_changes file.
                changes_filename = 'Proposed_Changes_' + str(int(time.time())) + '.csv'
                # Saving the changes in a csv.
                self.changes.to_csv(changes_filename, index=False)
                print('\nSaved the changes you made to the working template under the filename \"' \
                    + UI.colors.Saved_files + changes_filename + UI.colors.reset \
                        + '\", please send it to a Template Keeper for review.')
                break
            elif ans == 'n':
                rtrn = 0
                break
            else:
                self.value_error(hint='User must chose either \'y\' or \'n\'.')
        return rtrn
        

    # A function that adds self.changes to self.working_template, and maintains the second rule of a template:
    #   - "User must verify changes before adding them to the template"
    # Returns:
    #        1 = successfully updated template
    #        0 = Failure to update template
    def add_changes_to_working_template(self):
        # User must verify changes before adding them to the template
        print('\n-----------------------------------------' + UI.colors.Informational_Headers \
            + 'CAREFULLY REVIEW CHANGES YOU WANT TO ADD TO WORKING TEMPLATE' \
                + UI.colors.reset +'-----------------------------------------')
        print(tabulate(self.changes, headers='keys', showindex=True, tablefmt='fancy_grid'))
        # Ask the user if they are sure the changes are OK.
        ans = input(UI.colors.Questions + '\nAre you sure you want to add the above changes to the working template? (y|n) > ' + UI.colors.reset)
        # While loop for error handling.
        while(True):
            if ans == 'y':
                # Append changes to working template.
                self.working_template = self.working_template.append(self.changes, ignore_index=True)\
                                        .drop_duplicates().sort_values('Category').reset_index(drop=True)
                print('\nSuccessfully added changes to the working template (NOTE: no changes were made to the online template).')
                self.save_changes()
                break
            # Ask user if they would like to save the changes to a file and Return 0
            elif ans == 'n':
                self.save_changes()
                return 0
            else:
                self.value_error(hint='User must chose either \'y\' or \'n\'.')
        # If code reaches this line, then the changes were successfully added to the working template.
        return 1


    # A function that asks the user to a categorize uncategorizeable row,
    # by adding the user's categorizations to self.changes.
    # Params:
    #        uncategorizeable = vulnerability row that is uncategorizeable
    # Return:
    #       1 = Successfully categorized the row.
    #       0 = Failed to categorize the row.
    def add_to_changes(self, uncategorizeable, remove_from_template = False):
        vuln_name = uncategorizeable
        if not self.is_name_in_template(vuln_name)[0]:
            official_categories = pd.unique(self.working_template['Category'])
            # Print official categories
            print('\n-----------------------------------------' + UI.colors.Informational_Headers \
                + 'OFFICIAL CATEGORIES FOUND IN WORKING TEMPLATE' + UI.colors.reset + '----------------------------------------')
            for o_cat in range(0, len(official_categories)):
                print('(' + str(o_cat) + ') ' + UI.colors.Categories + official_categories[o_cat] + UI.colors.reset)
            # Have the user categorize the row.
            ans = input(UI.colors.Questions + 'Please chose from the above printed official categories or ' \
                + 'create a new category for \"' + UI.colors.Names + vuln_name + UI.colors.Questions + '\". (number|new) > ' + UI.colors.reset)
            while(True):
                if (not is_number(ans)) and ans == 'new':
                    # If a mistake is made here, quit and restart,
                    # or fix the template, after, using fix_template.
                    new_category = input(UI.colors.Questions + 'Carefully type the new category for \"' + UI.colors.Names + vuln_name \
                                        + UI.colors.Questions + '\" and make sure it is not the same as an official category. > ' + UI.colors.reset)
                    # If template needs fixing, then remove vuln_name from template before adding to changes
                    if remove_from_template:
                        self.working_template = self.working_template[self.working_template.Name != vuln_name]
                    # Add the new_category to self.changes.
                    change = {'Name':vuln_name, 'Category':new_category}
                    self.changes = self.changes.append(change, ignore_index=True)
                    print('\n' + UI.colors.Names + vuln_name + UI.colors.reset + ' was successfully categorized as \"' \
                        + UI.colors.Categories + new_category + UI.colors.reset + '\".')
                    break
                elif int(ans) in range(0, len(official_categories)):
                    # If template needs fixing, then remove vuln_name from template before adding to changes
                    if remove_from_template:
                        self.working_template = self.working_template[self.working_template.Name != vuln_name]
                    # Add official category chosen to self.changes.
                    change = {'Name':vuln_name, 'Category':official_categories[int(ans)]}
                    self.changes = self.changes.append(change, ignore_index=True)
                    print('\n\"' + UI.colors.Names + vuln_name + UI.colors.reset \
                        + '\" was successfully categorized as \"' + UI.colors.Categories \
                            + official_categories[int(ans)] + UI.colors.reset + '\".')
                    break
                else:
                    self.value_error(hint='Please enter the number representing an official category (0-' \
                    + str(len(self.official_categories) - 1) + '), or the word \'new\'.')
            return 1
        else:
            return 0


    # A function that has the user manually chose a category or create one for a Nessus scan result row.
    # This function can change the working template, if duplicated names are found to be present.
    # NOTE: This function Maintains the first rule of a template:
    #   - "No duplicate names"
    # If a duplicated name is found, the user has 3 options:
    #   (1) Do nothing
    #   (2) Delete the name from the working template, before adding the name with a new category to self.changes
    #   (3) Delete the name from the working template, before add the name with an official category to self.changes
    #
    # Params:
    #        row = Series with column [Name], at least.
    # Returns:
    #        1 = Successfully added to changes.
    #        0 = Failed to add to changes.
    def handle_uncategorizeable(self, vuln_name):
        rtrn = 1
        is_duplicated = self.is_name_in_template(vuln_name)
        if is_duplicated[0]:
            # Then name is already categorizeable.
            print('Your attempt to manually add the vulnerability by the name ' + UI.colors.Names \
                    + vuln_name + UI.colors.reset + ' to the working template was unsuccessful' \
                        + ', because that vulnerability is already categorized as ' + UI.colors.Categories \
                            + is_duplicated[1] + UI.colors.reset + '.')
            # Ask the user if they would like to re-categorize it.
            ans = input(UI.colors.Questions + 'Is the vulnerability by the name ' + UI.colors.Names \
                + vuln_name + UI.colors.Questions + ' appropriately categorized? (y|n) > ' + UI.colors.reset)
            while(True):
                if ans == 'n':
                    # Recategorize a name in the working template, by removing it from template and adding it to changes.
                    self.add_to_changes(vuln_name, remove_from_template = True)
                    break
                elif ans == 'y':
                    rtrn = 0
                    break
                else:
                    self.value_error(hint='User must chose either \'y\' or \'n\'.')
        else:
            # Then name is uncategorizeable, which means you should just categorize it.
            # Add to changes.
            self.add_to_changes(vuln_name)

        return rtrn

    
    # A function that handles uncategorizeable rows in scan_table, before categorizing scan_table.
    # Params:
    #        scan_table = DataFrame with column [Name], at least.
    # Returns:
    #        categorized = DataFrame with columns [Name, Category], at least.
    #        modified_template = Boolean that indicates the template was modified or not.
    def categorize_scan_table(self, scan_table):
        
        # Boolean value to be used as indicator for whether this scan was categorized with modifications to Template or not. 
        modified_template = 0
        
        while(True):
            
            # Find the categorizeable and uncategorizeable rows in scan_results.
            categorizeables, uncategorizeables, a = self.is_categorizeable(scan_table)
                        
            # Drop unnecessary column.
            categorizeables.drop('Template Category', axis=1)
            
            # If there are any uncategorizeable rows in scan_table.
            if uncategorizeables.shape[0] > 0:
                
                # Then show the user the uncategorizeable names.
                unique_names = pd.unique(uncategorizeables['Name'])
                
                print('\n-----------------------------------------' + UI.colors.Process_Headers + 'UNCATEGORIZEABLE NAME(S) DETECTED' \
                + UI.colors.reset + '-----------------------------------------')
                
                print('\nWe have found ' + UI.colors.Names + str(len(unique_names)) \
                    + UI.colors.reset + ' uncategorizeable unique names, i.e. names that are not currently found in the Template')
                
                # Print each unique name
                for u in unique_names:
                    print(' - ' + UI.colors.Names + u + UI.colors.reset)

                # Then ask the user if they would like to manually add the uncategorizeable names to the template.
                ans = input(UI.colors.Questions + '\nWould you like to manually add ' + UI.colors.Names + str(len(unique_names)) \
                    + UI.colors.Questions + ' uncategorizeable name(s) to the working template before categorizing? NOTE: If you chose no,' \
                        + ' only the categorizeable row(s) shall be categorized and summarized. (y|n) > ' + UI.colors.reset)
                
                # If the user choses yes.
                if ans == 'y':
                    # Then manually add each of the uncategorizeable names to the changes.
                    for name in unique_names:
                        self.handle_uncategorizeable(name) # The user should add this row to changes.
                    # Then add the changes to the working_template
                    self.add_changes_to_working_template()
                    modified_template = 1
                
                # If the user chooses no, then escape the while-loop.
                elif ans == 'n':
                    uncat_name = 'Uncategorized' + str(int(time.time())) + '.csv'
                    uncategorizeables.to_csv(uncat_name, index=False)
                    print('\nSaved the uncategorizeable names, to the filename \"' \
                        + UI.colors.Saved_files + uncat_name + UI.colors.reset + '\".')
                    break
                
                else:
                    self.value_error(hint='User must chose either \'y\' or \'n\'.')
            # If there are no uncategorizeable rows, then escape the while-loop.
            else:
                break
        
        # Now that you have handled uncategorized rows, you can now categorize the categorizeable rows, 
        # save them in a file and return them.
        merged = categorizeables.merge(self.working_template, how='left', on="Name")\
                    .sort_values(['Severity']).drop_duplicates().reset_index(drop=True)
        
        # Selecting only the categorized rows.
        categorized = merged[merged['Category'].notnull().values].reset_index(drop=True)[['Severity', 'Affected System', 'Name', 'CVE', 'Description', 'Solution', 'Plugin Output', 'Category']]
        # Combine Name and CVE into one column called 'Name'
        categorized = categorized.fillna('')
        categorized['Name'] = categorized['Name'].astype(str) + ' ' + categorized['CVE'].astype(str)
        
        return categorized, modified_template


    # A function that gives the user a final chance to rewrite the proposed changes categories, before updating.
    def rewrite_changes_categories(self, proposed_changes_DF):
        
        while(True):
            
            proposed_categories = pd.unique(proposed_changes_DF['Category'])
            
            proposed_new_categories = []
            
            official_categories = pd.unique(self.working_template['Category'])
            
            for pc in list(proposed_categories):
                
                if pc not in list(official_categories):
                    proposed_new_categories.append(pc)
            
            if len(proposed_new_categories) > 0:
                
                print('\n-----------------------------------------' + UI.colors.Informational_Headers \
                    + 'PROPOSED NEW CATEGORIES' + UI.colors.reset + '-----------------------------------------')
                
                # Print each proposed new category
                for idx in range(0, len(proposed_new_categories)):
                    print('(' + str(idx) + ') ' + UI.colors.Categories + proposed_new_categories[idx] + UI.colors.reset)

                ans = input(UI.colors.Questions + '\nWould you like to rewrite any of the proposed new categories above,' \
                    + ' before adding them to the template? \nNOTE: This is your chance to fix any spelling errors.\n(number|n) > ' + UI.colors.reset)
                
                if not is_number(ans) and ans == 'n':
                    break
                
                elif is_number(ans) and (int(ans) in range(0, len(proposed_new_categories))):
                    
                    # This is the proposed new category the user chose to correct.
                    cat_to_change = proposed_new_categories[int(ans)]
                    
                    # Get the correct category from the user.
                    ans2 = input(UI.colors.Questions + '\nCarefully rewrite \"' + UI.colors.Categories \
                        + cat_to_change + UI.colors.Questions + '\" > ' + UI.colors.reset)
                    
                    # Replace each instance of the cat_to_change into the correct category
                    proposed_changes_DF = proposed_changes_DF.replace(cat_to_change, ans2)
                    
                    print('\nThe category \"' + UI.colors.Categories + cat_to_change + UI.colors.reset \
                        + '\", in proposed changes, was re-written to \"' + UI.colors.Categories + ans2 + UI.colors.reset + '\".')
                                    
                else:
                    self.value_error(hint='Please enter either a number from the above proposed new categories or \'n\'')
            
            else:
                break
        
        return proposed_changes_DF


    def upload(self, message):
        remove_folder = ['rm', '-rf', 'Template']
        git_clone = ['git', 'clone', 'https://github.com/drakstik/Template.git']
        remove_git = ['rm', '-rf', '.git']
        copy_git = ['cp', '-r', 'Template/.git', '.']
        git_add_tempalte = ['git', 'add', 'Template.csv']
        git_commit = ['git', 'commit', '-m', message]
        git_push = ['git', 'push']

        upload_commands = [remove_folder, git_clone, remove_git, copy_git, git_add_tempalte, git_commit, git_push, remove_folder]
        print('\n-----------------------------------------' + UI.colors.Process_Headers \
                + 'UPLOADING THE TEMPLATE' + UI.colors.reset + '----------------------------------------')
        for c in upload_commands:
            terminal(c, 'GOOD')
        print('\n-----------------------------------------' + UI.colors.Process_Headers \
                + 'UPLOADING THE TEMPLATE' + UI.colors.reset + '----------------------------------------')
    
    
    # This function recategorizes rows in the Template with the user's help, 
    # only if there is a conflict between Proposed Changes and the Template.
    def recategorize(self, categorizeable):
        # If there are any categorizeable rows, then it means some names are already in the template.
        # And the user MUST decide between the official or recategorizing them to proposed categories, before proceeding.
        recategorized = pd.DataFrame()
        while(True):
            if categorizeable.shape[0] > 0:
                # Retain only the Proposed Categories that are not equal to the Template Category,
                # because we want to see the conflicting categories only.
                categorizeable = categorizeable[categorizeable['Proposed Category'] != categorizeable['Template Category']]
                categorizeable = categorizeable.reset_index(drop=True)

                # Show user the names that are already categorized in the Template
                print('\n' + UI.colors.Names + str(categorizeable.shape[0]) + UI.colors.reset \
                    + ' names in the Proposed Changes were already categorized in the Template. Please review them below:')
                
                print(tabulate(categorizeable, headers='keys', showindex=True, tablefmt='fancy_grid'))
                
                # Ask the user if they would prefer to keep the template categories for the 
                ans = input(UI.colors.Questions + '\nPick a number from the above table to ' \
                    + ' chose the Proposed Category first, then type \"keep\" ' \
                        + 'to chose the Template Category for ALL THE NAMES listed above. (number|keep) > ' + UI.colors.reset)
                
                # The user chose to keep the Template the way it is.
                if not is_number(ans) and ans == 'keep':
                    break
                
                # The user chose to recategorize a name in the Template.
                elif is_number(ans) and (int(ans) in range(0, len(categorizeable))):
                    # Drop row at index ans.
                    row = categorizeable.iloc[int(ans)]
                    name = row.values[0]
                    cat_in_proposed_changes = row.values[1]
                    # Delete the row in working template
                    self.working_template = self.working_template[self.working_template['Name'] != name]

                    # Change the working template to the proposed category.
                    self.working_template = self.working_template.append({'Name':name, 'Category':cat_in_proposed_changes}, ignore_index=True)
                    self.working_template = self.working_template.sort_values('Category').reset_index(drop=True)
                    # TODO: Is this print necessary???? Or was it just for testing purposes?? If necessary, then tabulate.
                    print(self.working_template[self.working_template['Name'] == name])
                    
                    recategorized = recategorized.append({'Name':name, 'Category':cat_in_proposed_changes}, ignore_index=True)
                    categorizeable = categorizeable.drop(categorizeable.index[int(ans)])
                    
                    print('\n' + UI.colors.Names + name + UI.colors.reset + ' was recategorized to ' \
                        + UI.colors.Categories + cat_in_proposed_changes + UI.colors.reset)
                
                else:
                    self.value_error(hint='Type a number from the above proposed changes to rewrite ' \
                        + 'the template to the proposed change or type keep to retain the Template category.')
            
            else:
                break

        return recategorized

    # Sub-function for update_template
    def update_template_sub(self, proposed_changes_DF):
        # Clean up the filenames into a DataFrame.
        proposed_changes_DF = proposed_changes_DF[['Name', 'Category']]
        proposed_changes_DF = lower_and_strip(proposed_changes_DF, ['Name', 'Category']).sort_values('Category').reset_index(drop=True)
        proposed_changes_DF = proposed_changes_DF.drop_duplicates()
        
        # Dropping rows without any Category values.
        b4 = proposed_changes_DF.shape[0]
        proposed_changes_DF = proposed_changes_DF.dropna(subset=['Category'])
        uncategorized = b4 - proposed_changes_DF.shape[0]
        if uncategorized > 0:
            print(UI.colors.Errors + str(uncategorized) + ' rows were uncategorized (i.e. had no Category value) and therefor dropped! If you would like to categorize them, use the categorizer.' + UI.colors.reset)
        
        # Dropping rows with the wrong Severity
        if 'Severity' in proposed_changes_DF.columns:
            proposed_changes_DF = proposed_changes_DF[proposed_changes_DF['Severity'] != 'None']
        
        
        # Give the user an opportunity to rewrite proposed new categories and correct spelling errors.
        proposed_changes_DF = self.rewrite_changes_categories(proposed_changes_DF)
        
        # Seperate categorizeable with uncategorizeable.
        categorizeable, uncategorizeable, in_template = self.is_categorizeable(proposed_changes_DF)
        if categorizeable.shape[0] > 0:
            categorizeable = categorizeable.rename(columns={'Category':'Proposed Category'})
            categorizeable = categorizeable[['Name', 'Proposed Category', 'Template Category']]
        
        
        # Ask the user to either recategorize some rows according to the proposed changes or ignore the proposed changes,
        # If there is a conflict between the Template and Proposed Changes.
        recategorized = self.recategorize(categorizeable)
        
        msg = ''
        # Uncategorizeable is a table of names that havent yet been seen by the template, so we can simply add them with a final check from the user.
        if uncategorizeable.shape[0] > 0:
            
            print('\n-----------------------------------------' + UI.colors.Informational_Headers \
                + 'NEW ROWS TO ADD TO THE TEMPLATE' + UI.colors.reset + '-----------------------------------------')
            
            print(tabulate(uncategorizeable, headers='keys', showindex=True, tablefmt='fancy_grid'))
            
            while(True):
                ans = input(UI.colors.Questions + '\nAre you sure you want to add all these rows to the Template? (y|n) > ' + UI.colors.reset)
                
                # Add uncategorizeable to Template, if the user said 'y'
                if ans == 'y':
                    
                    self.working_template = pd.concat([self.working_template, uncategorizeable[['Name', 'Category']]])
                    
                    print(str(uncategorizeable.shape[0]) + ' row(s) added to the Template:')
                    
                    print(tabulate(uncategorizeable, headers='keys', showindex=True, tablefmt='fancy_grid'))
                    
                    msg = str(uncategorizeable.shape[0]) + ' rows added.'
                    break
                # Just escape loop
                elif ans == 'n':
                    break
                else:
                    self.value_error(hint='Please type \'y\' or \'n\'.')
        else:
            print('\nNo new rows were added to the Template.')
        
        # Alert the user of the recategorized names.
        num_recategorized = recategorized.shape[0]
        if num_recategorized > 0:
            print('\nRecategorized ' + str(num_recategorized) + ' name(s) in the Template.')
            msg += '/' + str(num_recategorized) + ' recategorized.'
        
        # Update the template.csv and upload it.
        self.working_template = self.working_template.sort_values('Category').reset_index(drop=True)
        self.working_template.to_csv('Template.csv', index=False)
        print('\nSaved the working template as \"' + UI.colors.Saved_files + 'Template.csv' + UI.colors.reset + '\".')
        
        return msg

    def update_template(self, filenames):
        # Handle multiple filenames or 1 filename.
        if len(filenames) == 1:
            proposed_changes_DF = pd.read_csv(filenames[0], index_col=False)
            msg = self.update_template_sub(proposed_changes_DF)
        elif len(filenames) > 1:
            # Attach the files together into one proposed_changes_DF
            proposed_changes_DF = pd.DataFrame()
            for i in range(len(filenames)):
                csv = pd.read_csv(filenames[i], index_col=False)
                # csv = csv[["Risk","Host","Name","Description","Solution","Plugin Output","Category"]]
                # csv.columns = ['Severity', 'Host']
                proposed_changes_DF = pd.concat([proposed_changes_DF, csv]).reset_index(drop=True)
                msg = self.update_template_sub(proposed_changes_DF)
        else:
            print("You forgot to add a filename.")
            return
        self.upload(msg)
        print('\nSuccessfully uploaded \"' + UI.colors.Saved_files + 'Template.csv' + UI.colors.reset + '\" to online repository.')

        
# Runs when you call 'python3 Categorize.py' with the filename as an argument in your terminal command
# Example: 
#       $ python3 Categorize.py 'Raw Nessus Scan.csv'
def main():
    args = sys.argv[1:] 
    t = Template()
    # args is a list of the command line args
    # TODO: Accept a list of filenames.
    print(args)
    t.update_template(args)

if __name__ == "__main__":
    main()

# check_system_requirements()