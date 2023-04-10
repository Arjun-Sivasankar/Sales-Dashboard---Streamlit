import yaml
import streamlit_authenticator as stauth
from yaml import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    print(config)

    passwords = []
    for i in config['credentials']['usernames']:
        passwords.append(str(config['credentials']['usernames'][i]['password']))

print(passwords)

hashed_password = stauth.Hasher(passwords).generate()
print(hashed_password)

for hashed_pw, prev_pw in zip(hashed_password, config['credentials']['usernames'].items()):
    prev_pw[1]['password'] = hashed_pw

print(config)

with open('config_hashpassw.yaml', 'w') as outfile:
    yaml.dump(config, outfile)