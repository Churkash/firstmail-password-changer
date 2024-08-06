from colorama import Fore
import datetime

blue = Fore.LIGHTBLUE_EX
green = Fore.LIGHTGREEN_EX
red = Fore.LIGHTRED_EX
yellow = Fore.YELLOW
black = Fore.LIGHTBLACK_EX
basic = Fore.RESET


@staticmethod
def success(msg: str, mail: str, status: int):
    print(f"{black}{datetime.datetime.now().strftime("%I:%M:%S %p")} ~ {blue}[FIRSTMAIL-CHANGER]{black} ~{green} {msg} {black}Mail={basic}{mail} {black}Status={basic}{status}")
    

@staticmethod
def error(msg: str, mail: str, status: int):
    print(f"{black}{datetime.datetime.now().strftime("%I:%M:%S %p")} ~ {blue}[FIRSTMAIL-CHANGER]{black} ~{red} {msg} {black}Mail={basic}{mail} {black}Status={basic}{status}")


@staticmethod
def ratelimit(msg: str, mail: str, status: int):
    print(f"{black}{datetime.datetime.now().strftime("%I:%M:%S %p")} ~ {blue}[FIRSTMAIL-CHANGER]{black} ~{yellow} {msg} {black}Mail={basic}{mail} {black}Status={basic}{status}")
