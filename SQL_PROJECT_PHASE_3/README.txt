======= REQUIREMENTS TO USE AND INTERACT WITH 'valorant_tracker' DATABASE =======
1. Python 3.x installed
2. MySQL server installed and running
3. MySQL Python Connector
    -- Installing Python Connector -- 
        in cmd
            "pip install mysql-connector-python"



======= SETUP INSTRUCTIONS =======
1. Download the project files (zip file in Canvas Submission)
    a. Python files
    b. SQL file

2. Create the Datebase
    a. Open the sql file from the zip file on canvas titled similarly to 'valorant_database'
    using MySQL

3. Configure Database Connection
    a. Open Python files folder
    b. Create virtual environment 
        i. If you do not have one created already, run...
            "python -m venv venv"
        ii. If you already have the Scripts run them...
            "venv\Scripts\activate"
    
        Terminal entry should begin with (venv)
        i.e. "(venv) C:\Users\YourName\PathtoFolder>
    c. ensure the connection parameters match your local SETUP
        (i.e.
            DB_CONFIG = {
                'user': 'root',
                'password': 'YOUR_PASSWORD',
                'host': '127.0.0.1',
                'database': 'valorant_tracker'  # or your chosen database name
            }
    )

        run "python test_db.py" in order to test if the connection is working

4. Load basic/sample information into the database
    a. Run python seeding script
        "python seed_data.py"

        NOTE: If you have already run seed_data before, you will recieve an error when 
        trying to run again

======= RUNNING THE CLI =======
1. run command "python cli.py" to start interacting with the database

--> the following functionalities are available 
    1. List Teams
    2. List Players
    3. View Player Details
    4. List Matches
    5. View Match Details
    6. Add a Note to a VOD
    7. Add a player 
    0. Exit

User will be prompted with input instructions upon selection
