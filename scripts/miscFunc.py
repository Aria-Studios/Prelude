from cryptography.fernet import Fernet
import csv, secrets, smtplib, ssl, string

def keyGen():
    key = Fernet.generate_key()
    key = key.decode('UTF-8')

    print('\ncopy the entire string of characters below and paste it into the cryptKey field within config.py.\n\n' + key)

def sendEmails():
    iniFile = open('data.csv')
    csvReader = csv.reader(iniFile)
    next(csvReader)
    alphabet = string.ascii_letters + string.digits

    for name, email, password in csvReader:
        print(f'Generating password for {name}')
        password = ''.join(secrets.choice(alphabet) for i in range(12))
        print(password)

    iniFile.close()

def testEmail():
    print('test.')

def pwdGen():
    number = int(input('\nhow many passwords are needed? '))
    pwdFile = open('passwords', 'w')
    alphabet = string.ascii_letters + string.digits

    for temp in range(number):
        password = ''.join(secrets.choice(alphabet) for i in range(12))
        pwdFile.write(password + '\n')

    pwdFile.close()
    print('\npasswords generated. you will upload the created file to your server for users to authenticate against.')

def main():
    print('\nmiscellaneous functions companion script (v1)')
    print('------------------------------')
    print('1 - generate passwords for script.')
    print('2 - send test invitation.')
    print('3 - send invitations.')
    print('4 - generate encryption key.')
    command = int(input('\nplease select an action above: '))

    if (command == 1):
        pwdGen()
    elif (command == 2):
        print('send test invitation.')
    elif (command == 3):
        print('send invitations.')
    elif (command == 4):
        keyGen()
    else:
        print('please try again.')

main()
