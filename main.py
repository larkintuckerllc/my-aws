# pylint: disable=no-member
import boto3
import sys
import sys

iamClient = boto3.client('iam')
iamResource = boto3.resource('iam')

def create_user_and_creds(user_name, user_password):
    iamClient.create_user(
        UserName=user_name
    )
    user = iamResource.User(user_name)
    user.add_group(
        GroupName='MyDevelopers'
    )
    user.create_login_profile(
        Password=user_password,
        PasswordResetRequired=True
    )
    access_key_pair = user.create_access_key_pair()
    return access_key_pair


# READ IN USER NAME PASSWORDS
user_name_passwords = []

try:
    f = open('user_name_passwords.csv')
except IOError as err:
    sys.exit(err.strerror)

for line in f:
    stripped = line.strip()
    fields = stripped.split(',')
    if len(fields) != 2:
        raise Exception
    user_name = fields[0]
    user_password = fields[1]
    user_name_passwords.append((
        user_name,
        user_password
    ))

# CREATE USERS 
user_name_password_access_keys = []

try:
    for user_name_password in user_name_passwords:
        access_key_pair = create_user_and_creds(*user_name_password)
        user_name_password_access_keys.append((
            user_name,
            user_password,
            access_key_pair.id,
            access_key_pair.secret 
        ))
except:
    sys.exit(sys.exc_info()[0])

# WRITE OUT USER NAME PASSWORD ACCESS KEYS
try:
    f = open('user_name_password_access_keys.csv', 'w')
    for user_name_password_access_key in user_name_password_access_keys:
        line = ','.join(user_name_password_access_key) + '\n'
        f.write(line)
except IOError as err:
    sys.exit(err.strerror)
else:
    f.close()