import httplib2
import os
import argparse
import googleapiclient
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
CLIENT_SECRET_FILE = 'client_secret.json'

def parse_args():
    parser = argparse.ArgumentParser(description='Google apps Insert/Delete operation')
    subparsers = parser.add_subparsers(help='Help for insert and delete user')

    # create the parser for the "Insert" command
    parser_i = subparsers.add_parser('insert', help='Insert user help')
    parser_i.add_argument('fname', help='Firstname of the user')
    parser_i.add_argument('lname', help='Lastname of the user')
    parser_i.add_argument('email', help='Primary email of the user')
    parser_i.add_argument('passw', help='Password of the user')
    parser_i.add_argument('mobileno', help='Mobile number of the user')
    parser_i.set_defaults(which='insert')

    # create the parser for the "Delete" command
    parser_d = subparsers.add_parser('delete', help='Delete user help')
    parser_d.add_argument('email', help='Primary email of the user')
    parser_d.set_defaults(which='delete')

    args = parser.parse_args()
    return args

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    cwd = cwd = os.getcwd()
    credential_dir = os.path.join(cwd, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'cred.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def list_users(service):
    print '\nGetting the first 10 users in the domain'
    results = service.users().list(customer='my_customer', maxResults=10, orderBy='email').execute()
    users = results.get('users', [])
    if not users:
        print '\nNo users in the domain.\n'
    else:
        print '\nUsers:'
        for user in users:
            print '{0} ({1})'.format(user['primaryEmail'], user['name']['fullName'])

def delete_user(service, email):
    try:
        results = service.users().delete(userKey = email).execute()
        print '\nuser deleted successfully\n'
    except googleapiclient.errors.HttpError as e:
        print '\n %s \n' % e

def insert_user(service, email, fname, lname, passw, mobileno):
    userinfo = {
                'primaryEmail': email,
                'name': { 'givenName': fname, 'familyName': lname },
                'password': passw,
                'phones': [ { 'value' : mobileno, 'type': 'mobile', 'primary' : True} ]
            }
    try:
        results = service.users().insert(body = userinfo).execute()
        if results['id']:
            print '\nNew user %s created successfully\n' % fname
    except googleapiclient.errors.HttpError as e:
        print '\n %s \n' % e
def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)
    args = parse_args()
    if args.which == 'insert':
        insert_user(service, args.email, args.fname, args.lname, args.passw, args.mobileno)
    elif args.which == 'delete':
        delete_user(service, args.email)
    else:
        print '\nPlease provide valid argument\n'
    list_users(service)

if __name__ == '__main__':
    main()
