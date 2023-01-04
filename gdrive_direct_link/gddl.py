import requests


link = input('Paste the link -> ')
url_sample = 'https://drive.google.com/uc?export=download&id='

direct_link = url_sample + [i for i in link.split('/') if len(i) > 17][0]

response = requests.get(direct_link)
if response.status_code == 200:
    print(direct_link)
else:
    print('Something went wrong. Please try again.')
