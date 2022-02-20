import os
from pathlib import Path
import sys

def main():
    def initProject(projectName):
        print(projectName)

        # 1. Create project directory, and
        # 2. Create empty functions/ directory
        Path(f"{projectName}/functions").mkdir(parents=True, exist_ok=True)

        # 3. Add transforms/ directory with scaffolded my_first_transform.py file
        Path(f"{projectName}/transforms").mkdir(parents=True, exist_ok=True)

        transformPath = f"{projectName}/transforms/my_first_transform.py"
        if not os.path.exists(transformPath):
            with open(transformPath, 'w') as f:
                initialTransform = """def transform():
    return f"select 'hello world!' as hello"

def test(self, rafa):
    # Set the expected result
    expected = [{ "hello": "hello world!" }]

    # Note that we use rafa.temp_transform() instead of rafa.transform() so that the output table is temporary
    res = rafa.temp_transform(self)
    assert rafa.select_all(res).to_dict('records') == expected
                """
                f.write(initialTransform)
        
        # 4. Add `project.py` with `from rafa import *` and `from transforms import my_first_transform`
        projectPath = f"{projectName}/project.py"
        if not os.path.exists(projectPath):
            with open(projectPath, 'w') as f:
                initialProject = """from rafa import Rafa
from transforms import my_first_transform

rafa = Rafa(demo=True)

### Run tests ###
rafa.test(my_first_transform)

### Run transforms ###
rafa.transform(my_first_transform)
                """
                f.write(initialProject)

        #5. Add config file, though it will be unused
        Path(f"{projectName}/profiles").mkdir(parents=True, exist_ok=True)
        configPath = f"{projectName}/profiles/.env.default"
        if not os.path.exists(configPath):
            with open(configPath, 'w') as f:
                f.write(f"""# dbtype is "redshift" | "postgres" | "sqlite"
RAFA_DBTYPE="redshift"

# use filename for SQLite, hostname for all others
RAFA_HOSTNAME="some-aws-hostname.us-east-1.aws.localhost"
RAFA_FILENAME="use_this_instead_of_hostname_for.sqlite"
RAFA_PORT=5439

RAFA_USERNAME="rafa"
RAFA_PASSWORD="fakepassword"
                """)
        
        # 6. add gitignore
        gitignorePath = f"{projectName}/.gitignore"
        if not os.path.exists(gitignorePath):
            with open(gitignorePath, 'w') as f:
                f.write("""
*__pycache__/
profiles/
*venv/
                """)
    
    def runProject():
        sys.path.append(os.getcwd())
        import project

    def runTests():
        pass

    if sys.argv[1] == 'init':
        initProject(sys.argv[2])
    elif sys.argv[1] == 'run':
        runProject()
    elif sys.argv[1] == 'test':
        runTests()
