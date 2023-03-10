# ENGLISH SENTENCE REMINDER
### For improving my english conversation skills, I made this project which repeatedly sends what I learned before.

![Reminder](./img/english_sentence_reminder.jpg)  
- English sentences are located in the `Notion database`
- Reminder mail is sent through `NAVER mail`

### So you can learn things below in this repository.
- How to query the information from `Notion database`
- How to send the mail through `NAVER mail`
  - [How to set naver mail for sending mail from python](https://sunandbean.tistory.com/416)


## Preparations
If you want to set independent environment, you can use virtual environment like virtualenv, conda and etc.

FYI, I run this project in `Python 3.9.13`

``` bash
pip3 install -r requirements.txt
```

## Configurations
You have to change the name of file `config_template.py` to `config.py` for running the `main.py`.

And also you have to fill out the information in the `config.py`.

> If you want to connect your google spread sheet for managing the mail list, bring the api key json file into the repository and change the name to `gspread_key.json`
\
> In that case, your customer list will be replaced to mail list in the google spread sheet.
## How to run
``` bash
python3 main.py
```
or after modifying the location in the `run_reminder.sh`
``` bash
./run_reminder.sh
```