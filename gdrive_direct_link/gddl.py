import requests
import pyperclip
from time import sleep


link = input('Paste the link -> ')
url_sample = 'https://drive.google.com/uc?export=download&id='


def get_close_output():
    sec = 5
    for _ in range(sec):
        print(f'The script will close after {sec} sec ...')
        sec -= 1
        sleep(1)


try:
    direct_link = url_sample + [i for i in link.split('/') if len(i) > 17][0]

    response = requests.get(direct_link)
    if response.status_code == 200:
        pyperclip.copy(direct_link)
        print('The direct link was copied to the clipboard')
        get_close_output()
    else:
        print('Something went wrong. Please try again.')
        get_close_output()

except Exception:
    print('It does not look like Google link')
