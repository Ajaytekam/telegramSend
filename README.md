## telegramSend 

A simple python script to send files into your telegram Bot form your PC, Server etc.  

### How to Use 

* Install requirements.txt  

```
pip3 install -r requirements.txt  
```  

* Sending File 

```
./telegramSend.py -f 10840.pdf -c -m "This is the new test message" 

[+] Compressing File
[+] Message Sent.
[+] Sending file to Telegram Bot
[+] file sent successfully
``` 

* Help Menu  

``` 
./telegramSend.py -h

usage: telegramSend.py [-h] -f FILE [-m MESSAGE] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Filename to send your telegram chatbot
  -m MESSAGE, --message MESSAGE
                        Message to send with file
  -c, --compress        Compress the file
```   

### Telegram Bot Configuration file 

* Put your Telegram bot API Token and Chat Id into config.ini file and set path on `CONFIGPATH` variable `CONFIGPATH="/home/user/Config.ini"` on line 15.    
* Set `Config.ini` file like this :   

```   
[telegram]
apiToken = 1234567890:ABCDEFghijklMNOPqRSTUVZXyzABCdefG-H
chatId = 123456789
```   
