import json, subprocess


def check_user(message) -> bool:
    __user = subprocess.check_output(f"if [[ -e ./Users/{message.chat.id}.json ]]; then cat ./Users/{message.chat.id}.json; else echo 'Err!'; fi", shell=True).decode()
    if __user == "Err!":
        return False
    __user_dict = json.loads(__user)
    __user_status = __user_dict.get("account", "Err!").get("status", "Err!")
    if __user_status == "Err!":
        return False
    return True