import requests
import time
import os
import random
import json
import string
from concurrent.futures import ThreadPoolExecutor
from Logger import logging


mails = open('./Input/Mails.txt', 'r').read().splitlines()
config = json.load(open('./config.json', 'r'))

session = requests.Session()
session.headers = {"X-API-KEY": config["Main"]["X-Api-Key"],"content-type": "application/json"}

def generate_password():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + ''.join(random.choices(string.ascii_uppercase, k=1)) + '!' + ''.join(random.choices(string.digits, k=4))


def format_line(line):
    if ":" in line:
        parts = str(line).split(":")
        
    elif "|" in line:
        parts = str(line).split("|")
        
    else:
        print("Incorrect mail format.")
        exit(1)
        
    if len(parts) <= 1 or len(parts) >= 4:
        print("Incorrect mail format.")
        exit(1)
            
    return parts[0], parts[1]
    
    
class Firstmail():
    def change_password(mail, cpass, npass):
        while True:
            try:
                payload = {
                    "username": mail,
                    "cpassword": cpass,
                    "npassword": npass
                }
                
                resp = session.post("https://api.firstmail.ltd/v1/mail/change/password", json=payload)
                response = resp.text
                
                if resp.status_code == 200:
                    if "Password was updated" in response:
                        logging.success("Succesfully changed password.", mail, resp.status_code)
                        return True, 'Completed'
                    
                    elif "The password was changed less than a day ago" in response:
                        logging.error("The password was changed less than a day ago.", mail, resp.status_code)
                        return True, 'Password_was_changed_less_than_a_day_ago'
                    
                    elif "wrongPassword" in response:
                        logging.error("Password does not match.", mail, resp.status_code)
                        return True, 'Password_does_not_match'
                    
                    elif "Required username and cpassword and npassword" in response:
                        logging.error("Required username and cpassword and npassword (probably some of config values are missing).", mail, resp.status_code)
                        return False, None

                    else:
                        logging.error(f"Unknown error {resp.text}", mail, resp.status_code)
                        return True, 'Unknown_error'
                
                elif resp.status_code == 403:
                    if "IP missmatch" in response:
                        logging.error("ApiKey IP missmatch.", mail, resp.status_code)
                        return False, None
                    
                    elif "Api rate limit reached" in response:
                        logging.ratelimit("Resource has been ratelimited. Sleeping for 30 seconds...", mail, resp.status_code)
                        time.sleep(30)
                        continue
                    
                    elif "Api user not found" in response:
                        logging.error("Invalid ApiKey.", mail, resp.status_code)
                        return False, None
                    
                elif resp.status_code == 500:
                    logging.error("Internal server error.", mail, resp.status_code)
                    return True, 'Internal_server_error'
                
                else:
                    logging.error(f"Unknown error {resp.text}", mail, resp.status_code)
                    return True, 'Unknown_error'
                
                
            except Exception as e:
                print(e)
                time.sleep(1)
                continue
            
            
def thread(line):
    mail, cpass = format_line(line)
    if config["Password"]["Generate_password"] == "True":
        npass = generate_password()
    
    else:
        npass = config["Password"]["new_password"]
    
    result, file = Firstmail.change_password(mail, cpass, npass)
    if result:
        if not os.path.exists(f'./Output/{file}.txt'):
            with open(f'./Output/{file}.txt', 'a') as file:
                file.write(f"{mail}:{npass}\n")
                
        else:
            with open(f'./Output/{file}.txt', 'a') as file:
                file.write(f"{mail}:{npass}\n")


with ThreadPoolExecutor(max_workers=config["Main"]["Threads"]) as executor:
    for mail in mails:
        executor.submit(thread, mail)

                    
