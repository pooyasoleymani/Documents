import subprocess
import os


def runner(cmd: str):
    proc = subprocess.run([cmd])
    success = proc.returncode == 0
    if success:
        subprocess.run(["git", "commit", "-am" , "auto commit"], cwd=os.getcwd())
        subprocess.run(["git", "push"],cwd=os.getcwd())

def main():
    runner( "obsidian")

if __name__ == '__main__':
    main()


