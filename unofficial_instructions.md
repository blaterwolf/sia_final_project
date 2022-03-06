Creating a venv file (Virtual Environment) for VSCode

1. Run `python -m venv venv`
   * This creates what we call a Virtual Environment. Instead of downloading Python Packages on the global environment (i.e. `pip install <package_name>`) we can seperate an environment for a specific project so that when it is pushed through a repository, users can be able to create a seperate environment of the project.
2. Change directory to: `cd venv/Scripts`
   * this is the venv directory.
3. Run`source activate`
   * Run this command so that your Git console changes to the Virtual Environment.
4. `pip freeze`
   * For Git users sa VSCode, makikita mo dito na lalabas na yung `(venv)` sa baba don.
5. cd ../../ *(balik ka na)*

Optional
6. install ka ng gusto mong packages...
  6.1. update pip by:
    cd venv/Scripts
    python -m pip install --upgrade pip
  6.2 install autopep8 for vscode:
    pip install autopep8
  6.3 To download venv:
    pip install fastapi
    pip install "uvicorn[standard]"

7. pip freeze
    * check if fastapi at yung uvicorn ay nakainstall na.
8. pip freeze > requirements.txt *(for generating your own reqs.txt)*
  8.1 For pre-existing venv
    pip install -r requirements.txt *(if meron kang pre-existing venv ayan yung code na irurun para isang installan na lang ng packages)*

9. Run `uvicorn main:app --reload` to run the API to the localhost.
10. Don't forget to create your own database with the following details:
    * username: root
    * password: admin
    * server: localhost:3306
    * db_name: api_final_project_sia