# Instructions for GitHub Command Line Editing Tool


## Installation and Set-Up


#### Installing Python

Skip this section if you have already installed Python. Check if you have installed Python by running **python** in the command line. If Python is installed, information about the version will print into the console.

Step 1: Open https://www.python.org/downloads/ and download Python 3.10.6.

Step 2: Run the Python installer, and be sure to click "Add Python to PATH" and "Install launcher for all users" before clicking Install.

Step 3: Verify that Python was successfully installed by running **python** in the command line. If the installation was successful, information about the version will print into the console.

#### Creating a GitHub Enterprise account

Skip this section if you have already created a GitHub Enterprise account. Otherwise, follow the instructions here:
https://confluence.tomtomgroup.com/pages/viewpage.action?spaceKey=DVS&title=GitHub+Enterprise+onboarding

#### Installing Git for Windows

Step 1: Open https://git-scm.com/download/win and download the Standalone Installer.

Step 2: Open the downloaded Git installer and click Install.

#### Installing GitHub CLI

Step 1: Open https://github.com/cli/cli/releases/tag/v2.17.0 and download the file named gh_2.17.0_windows_amd64.msi.

Step 2: Run the file (GitHub CLI Setup Wizard). Be sure to pay attention to the installation location.

Step 3: Navigate to the installation location and copy-paste the file path of the GitHub CLI folder. 

Step 4: Open the System Properties app, search for environment variables, and open "Edit the system environment variables". Click on "Environment Variables" and double click on "Path". Select "New" and paste the GitHub CLI file path. Click OK and close the app.

Step 5: Restart your computer.

Step 6: Verify that GitHub CLI installed by running **gh** in the command line.


#### Authenticate with your GitHub account

Step 1: Authenticate with your GitHub Enterprise account by running **gh auth login** in the command line. 

Step 2: Hit enter while "GitHub.com" is selected (when asked which account to log into).

Step 3: Hit enter while "HTTPS" is selected (when asked your preferred protocol).

Step 4: Answer Yes to the question "Authenticate Git with your GitHub credentials".

Step 5: Hit enter while "Login with a web browser" is selected. Follow instructions for online login.


#### Cloning the Repo

Step 1: Open command line and navigate to your desired location using **pushd LOCATION**.

Example: pushd F:\OneDrive - TomTom

Step 2: Open https://github.com/tomtom-international/open-data and click the green "Code" button. Select "GitHub CLI" and click the copy icon to the right of the gray text box "gh repo clone...".

Step 3. Paste the gh repo clone command into the command line and run it.


## Running the command line tool.

Step 1: Navigate to the clones repository using **pushd LOCATION**. Make sure that you navigate inside of the repository and not its host folder.

Example: pushd F:\OneDrive - TomTom\open-data

Step 2: Run **python command_tool.py** followed by your desired flags. 

Example: python command_tool.py -c "Brazil","New Zealand" -m "NOTE: This project has been paused until further notice."


## Flags


#### Selecting desired issues for editing.

-a
Indicates that all issues in the repository should be edited.

-n [list of issue numbers separated by commas]
Example: -n 1,4,5

-c [list of country names separated by commas]
Example: -c "Brazil","United Kingdom","New Zealand"
Note: the names must be spelled exactly as they are in the GitHub issue title

-e [list of issue numbers to exclude from editing]
Example: -e 10,11,12
Note: In this example, all issues in the repository besides numbers 10, 11, and 12 will be edited.

-g [issue number to copy body to file]
Copies body of issue 10 to file issue_10.md
Example: -g 10


#### Performing edits.

-m "Message to add to top of issue"
Example: -m "NOTE: This project has been paused until further notice."

-d
Indicates that the most recent message added to the top of the issue (in gray text) should be deleted.

-f "Phrase to find." -r "Phrase to replace."
Example: -f "HOT Tasking Manager" -r "MapRoulette"
Note: Find phrase must be formatted identically to issue body for tool to work. Use -g to copy an issue body to a file for easy copy-paste of find phrase.
