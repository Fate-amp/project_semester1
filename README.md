# Flask App with Tailwind CSS & Chart.js
Simple website connected to MySQL server with database search and a dashboard. Implemented using Flask, Chart.js and SQLAlchemy

1. Prerequisites

Python 3.10 or higher installed
pip installed

2. Setup

**Step 1:**
Clone the repository:
`git clone 'https://github.com/Fate-amp/project_semester1.git'`

**Step 2: create the virtual environment**
`python -m pip install virtualenv env`
`python -m virtualenv env`

**Step 3: Activate the envirnoment**
- For Windows:
`.\env\Scripts\Activate.ps1`
Troubleshooting: in case you run into "cannot be loaded because the execution of scripts is disabled on this system" issue, run `Set-ExecutionPolicy Unrestricted -Scope Process`

- For Mac/Linux:
`source env/bin/activate`

**Step 4: Install the required packages from requirements.txt**
`pip install -r requirements.txt`

**Step5: Install JavaScript packages based on package-lock.json**
`npm i` (if you don't have node.js or npm, install them first)

**Step6: Change config.toml**
Input your database information

**Step 7: Run the flask app to see a demo of the project**
`flask run`
