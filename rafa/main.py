import os
from pathlib import Path
import sys

def main():
    if sys.argv[1] == 'init':
        projectName = sys.argv[2]
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
                """
                f.write(initialTransform)
        
        # 4. Add `project.py` with `from rafa import *` and `from transforms import my_first_transform`
        projectPath = f"{projectName}/project.py"
        if not os.path.exists(projectPath):
            with open(projectPath, 'w') as f:
                initialProject = """from rafa import *
from transforms import my_first_transform

rafa.transform(my_first_transform)
                """
                f.write(initialProject)
