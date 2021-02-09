from SimsimiAPI import SimsimiAPI
import time
import pyfiglet 
from colorama import init, Fore

init(autoreset=True)


def simsimi_api():

    while True:
        bot = SimsimiAPI()
        try:
            bot.generate_email()
            time.sleep(10)
        except Exception as e:
            bot.error_handler(e)
            bot.quit()
            bot.sleep(10)
        except KeyboardInterrupt:
            bot.quit()


if __name__ == "__main__":
    result = pyfiglet.figlet_format("Simsimi") 
    print(Fore.LIGHTGREEN_EX + result +  Fore.RESET) 
    simsimi_api()
