import json
import os
import sys
from pathlib import Path

FOLDER_PATH = Path(__file__).resolve().parent

USER = {
    "NAME": "John Doe",
    "JOB": "Web Developer",
    "EMAIL": "johndoe@email.com",
    "PHONE_NUMBER": "+99 99 99 99 99"
}

def data_injection(path: str | None = None) -> str:
    if path == None:
        path = os.path.join(FOLDER_PATH.resolve().parent, "user.json")

    try:
        with open(path, 'r') as fs:
            user: dict = json.load(fs)
    except Exception as e:
        return f"Failed to load the data from : {path} - {e}"
    
    try:
        html_script = os.path.join(FOLDER_PATH, "index.html")
        with open(html_script, 'r') as fs:
            script = fs.read()
    except Exception as e:
        return f"Failed to read the HTML script : {html_script} - {e}"
    
    try:
        for key, data in user.items():
            script = script.replace(f"PERSONAL_{key}", data)
    except Exception as e:
        return f"Failed to inject the user data : {e}"

    try:
        file_name = f"CV_{user['NAME'].replace(' ', '_')}"

        script = script.replace("PERSONAL_CV", file_name)
        compiled_script = os.path.join(FOLDER_PATH, f"{file_name}.html")

        with open(compiled_script, 'w') as fd:
            fd.write(script)
    except Exception as e:
        return f"Failed to save the compiled script due to the error : {e}"
    
    return "Successfully injected the Personnal Data of the user."

def init_data_user(path: str | None = None, data: dict = USER) -> str:
    if path == None:
        path = os.path.join(FOLDER_PATH.resolve().parent, "user.json")

    try:
        with open(path, 'w') as fd:
            json.dump(data, fd)
        return f"Successfully initialise the empty user file : {path}"
    except Exception as e:
        return f"Failed to initialize the file {path} - {e}"
    
def parse_args(args: list[str]) -> dict:
    parsed_args = {
        "user_path": None,
        "interactive": False,
        "compile": False
    }

    for arg in args:
        if arg.startswith(("-user-path", "--user-path")):
            try:
                parsed_args['user_path'] = arg.split('=')[1]
            except Exception as e:
                print(f"Failed to parse the following arg '{arg}' : {e}")
        elif arg in ("-interactive", "--interactive"):
            parsed_args['interactive'] = True
        elif arg in ("-compile", "--compile"):
            parsed_args['compile'] = True
    
    return parsed_args

def cli(user_path: str | None, interactive: bool, compile: bool):
    if interactive:
        user_path = input("Specify the file path [for default setting press ENTER] :\n")
        user_path = user_path if user_path != "" else None
        
        name = input("\nEnter your Firstname and your Lastname separated by a single space:\n")
        job = input("\nEnter your Job Title :\n")
        email = input("\nEnter your email :\n")
        phone_number = input("\nEnter your phone number :\n")

        data = {
            "NAME": name,
            "JOB": job,
            "EMAIL": email,
            "PHONE_NUMBER": phone_number
        }

        res = init_data_user(user_path, data)
        print(res)
        if not res.startswith("Success"):
            exit(1)
        
        compile_in = input("\nDo you want to compile your personnals informations ? [yes/no]\n").lower().strip()
        match compile_in:
            case "yes":
                res = data_injection(user_path)
                print(res)
                if not res.startswith("Success"):
                    exit(1)
            case "no":
                print("You can inject your personnals informations at any time.")
            case default:
                print(f"It's a Yes or No question, why did you respond '{default}' ?!")
    elif compile:
        res = data_injection(user_path)
        print(res)
        if not res.startswith("Success"):
            exit(1)

if __name__ == '__main__':
    args = sys.argv[1:]
    parsed_args: dict = parse_args(args)

    cli(**parsed_args)