import logging
import subprocess
 
def execute_script(script_path, service_name):
    try:
        bash_command = f"sudo -u ubuntu bash {script_path} {service_name}"
        # Execute the bash script using subprocess
        subprocess.run(bash_command, shell=True, check=True)
 
        print("Bash script executed successfully.")
        logging.info("Bash script executed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        error_message = e.stderr if e.stderr else str(e)
        print("Error executing bash script:", error_message)
        logging.error("Error happened while executing the script: %s", error_message)
        return False
