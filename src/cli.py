import json
import os
import sys

CONFIG_FILE = "deployments/config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {"projects": []}

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

def create_project(name, git, branch, directory, compose):
    config = load_config()
    if any(project["name"] == name for project in config["projects"]):
        print(f"Project '{name}' already exists.")
        return

    new_project = {
        "name": name,
        "git": git,
        "branch": branch,
        "directory": directory,
        "compose": compose
    }
    config["projects"].append(new_project)
    save_config(config)
    
    os.system(f'gh repo clone {git} {directory}')
    print(f"Project '{name}' created successfully.")

def read_projects():
    config = load_config()
    if not config["projects"]:
        print("No projects found.")
    for project in config["projects"]:
        print(f"Name: {project['name']}")
        print(f"  Git: {project['git']}")
        print(f"  Branch: {project['branch']}")
        print(f"  Directory: {project['directory']}")
        print(f"  Compose: {project['compose']}\n")

# TODO: updating a project should reflect some changes in the filesystem
# def update_project(name, git=None, branch=None, directory=None, compose=None):
#     config = load_config()
#     for project in config["projects"]:
#         if project["name"] == name:
#             if git:
#                 project["git"] = git
#             if branch:
#                 project["branch"] = branch
#             if directory:
#                 project["directory"] = directory
#             if compose:
#                 project["compose"] = compose
#             save_config(config)
#             print(f"Project '{name}' updated successfully.")
#             return

#     print(f"Project '{name}' not found.")

def delete_project(name):
    config = load_config()

    for project in config["projects"]:
        if project["name"] == name:
            os.system(f'rm -rf {project["directory"]}')

    config["projects"] = [project for project in config["projects"] if project["name"] != name]
    save_config(config)
    print(f"Project '{name}' deleted successfully.")

def main():
    if len(sys.argv) < 2:
        print("Usage: src/cli.py <command> [options]")
        return

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) != 7:
            print("Usage: src/cli.py create <name> <git> <branch> <directory> <compose>")
            return
        create_project(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

    elif command == "read":
        read_projects()

    # TODO: updating certain fields should reflect changes in the file structure
    # elif command == "update":
    #     if len(sys.argv) < 3:
    #         print("Usage: src/cli.py update <name> [git=<git>] [branch=<branch>] [directory=<directory>] [compose=<compose>]")
    #         return
    #     name = sys.argv[2]
    #     args = dict(arg.split('=') for arg in sys.argv[3:] if '=' in arg)
    #     update_project(name, **args)

    elif command == "delete":
        if len(sys.argv) != 3:
            print("Usage: src/cli.py delete <name>")
            return
        delete_project(sys.argv[2])

    else:
        print(f"Unknown command '{command}'. Available commands: create, read, delete.")

if __name__ == "__main__":
    main()
