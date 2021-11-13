#!/usr/bin/python3  
####
# telegramSend : Send file to telegram bot
# Author : Ajay kumar tekam | github.com/ajaytekam | https://sec-art.net
####
import argparse 
import configparser
import requests 
import sys
import os 
from zipfile import ZipFile
from halo import Halo

## Global vars 
CONFIGPATH = "/root/Config.ini"  
TELEGRAM_KEYS = {}  
## 

def CompressFile(FName, Files):
    print("[+] Compressing File")
    with ZipFile(FName, mode="w") as zf:
        for f in Files:
            zf.write(f)

def CheckTokens(ConfigPath): 
    config = configparser.RawConfigParser()
    if os.path.isfile(ConfigPath):
        config.read(ConfigPath)
        if config.has_option("telegram","apiToken") and config.has_option("telegram","chatId"): 
            return 1 # key found 
        else:
            return 2 # config file found but key not found
    else:
        return 3 # config file not found

def GetTokens(ConfigPath):
    config = configparser.RawConfigParser()
    if os.path.isfile(ConfigPath):
        config.read(ConfigPath)
        if config.has_option("telegram","apiToken") and config.has_option("telegram","chatId"): 
            apiToken = config.get("telegram","apiToken")
            chatId = config.get("telegram","chatId")
            return apiToken, chatId
        else:
            print("[-] Error : no credentials are setted for Telegram bot (API token and ChatId)")
            return 
    else:
        print("[-] Error : There is no config file available '/root/notificationConfig.ini'")
        return 

def NotifyBot(TelegramKeys, textMessage):
    #print("[+] Sending notification to telegram bot") 
    send_text = 'https://api.telegram.org/bot'+TelegramKeys['apiToken']+'/sendMessage?chat_id='+TelegramKeys['chatID']+'&parse_mode=Markdown&text='+textMessage
    response = requests.post(send_text)
    if response.status_code == 200:
        print("[+] Message Sent.")
        pass

def SendDocumentBot(TelegramKeys, FilePath):
    print("[+] Sending file to Telegram Bot")
    ## Some spinner actions
    spinner = Halo(text='Sending file..', spinner='dots')
    spinner.start()
    file = open(FilePath, "rb")
    file_bytes = file.read()
    file.close()
    url = 'https://api.telegram.org/bot{}/sendDocument'.format(TelegramKeys['apiToken']) 
    response = requests.post(url, params={'chat_id':TelegramKeys['chatID']}, files={'document':(file.name, file_bytes)}) 
    spinner.stop()
    if response.status_code == 200:
        print("[+] file sent successfully")
        pass
    else:
        print("[-] OOPS!! file does not sent.")
        print("[-] There is problem in sending file..")

def main():
    # start coding from here
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Filename to send your telegram chatbot", type=str, required=True)
    parser.add_argument("-m", "--message", help="Message to send with file", type=str)
    parser.add_argument("-c", "--compress", help="Compress the file", action="store_true")
    args = parser.parse_args()
    if not os.path.isfile(args.file):
        parser.print_help()
        sys.exit(1)
    global CONFIGPATH
    global TELEGRAM_KEYS
    retVal = CheckTokens(CONFIGPATH)
    if retVal == 1:
        apiToken, chatId = GetTokens(CONFIGPATH)
        TELEGRAM_KEYS['apiToken'] = apiToken
        TELEGRAM_KEYS['chatID'] = chatId
    elif retVal == 2:
        print("[-] Telegram Bot keys not found.!")
        sys.exit(1)
    elif retVal == 3:
        print("[-] Telegram Bot Config File not found.!")  
        sys.exit(1)
    # compress file 
    FILENAME = args.file
    if args.compress:
        FILENAME = "{}.zip".format(args.file)
        CompressFile(FILENAME, [args.file])
    # check the name of file
    if os.path.getsize(FILENAME) >= 52428800:
        print("[-] File size is bigger then 50MB size limit.!")  
        sys.exit(1)
    if args.message:
        NotifyBot(TELEGRAM_KEYS, args.message)
    # send file
    SendDocumentBot(TELEGRAM_KEYS, FILENAME)
    # deleting zip file if exists 
    if args.compress:
        os.remove(FILENAME)

if __name__ == "__main__":
    main()
