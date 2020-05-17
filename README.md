# UIWeekly
Python Selenium webdriver for filing state Unemployment weekly claims.

# Contribution
If you would like to contribute your own state site, please name the fork and directory your state's abbreviation and create a json config and python script.

# How to use.
The config.json file has all the questions (as seen on the website/form) so that the script can verify it is answering the correct questions. The answer should be changed each week to your proper responses. If "save" is set to true it will fill out the answers and save the document before closing the browser. If "save" is false it will fill out the answers and finish on the claim's summary page for you to manually submit.

If you add your username and password to the config, make sure you don't make any git commits. I am not responsible for you leaking your own credentials accidentally. Personally, I wouldn't put the credentials in the config. The script will still ask you for your username and password in terminal if those fields are left at "none".
