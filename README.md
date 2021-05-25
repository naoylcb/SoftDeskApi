# SoftDesk API

The SoftDesk API allows you to programmatically access data stored in SoftDesk database.

## Installation and Execution

If you've already installed Python, make sure it's up to date.
Otherwise, download and install Python. [Website] (https://www.python.org/downloads/)

Start by downloading the repository by clicking on the "Code" menu, then "Download ZIP".

Extract the folder.

In it, create and activate a virtual environment. For it :
- Open your terminal and go to the extracted folder,
- Run the command: `python -m venv env`,
- Then execute the command: `source env/bin/activate` (For Windows, the activation will be done with the file env/Scripts/activate.bat).

Still in the terminal, install the dependencies by running the command: `pip install -r requirements.txt`

Go to the "softdeskapi" folder and run the command : `python manage.py runserver`

You should use Postman to request the api.
Always start your endpoints with this domain : http://127.0.0.1:8000/

You can log in with this accounts to test the api: 
- yoan | test-test1
- luc | test/test2
- admin | admin