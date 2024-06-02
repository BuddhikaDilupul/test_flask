import logging
import subprocess


def execute_script(script_path, service_name):
    try:
        ansible_command = f"ansible-playbook {script_path} -e 'service={service_name}'"
        # Execute the Ansible playbook using subprocess
        subprocess.run(ansible_command, shell=True, check=True)


        print("Ansible playbook executed successfully.")
        logging.info("Ansible playbook executed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        error_message = e.stderr if e.stderr else str(e)
        print("Error executing Ansible playbook:", e)
        logging.error("Error happned while executing the script.")
        return True