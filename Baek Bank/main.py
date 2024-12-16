from os import system as sys
import shelve


def user_data_fill_out(user_data, existing=False):
    if not user_data.get('password', None) and existing:
        print('IMPOSSIBLE USER DATA')
        return False

    fixed_user_data = user_data

    if not user_data.get('name', None):
        fixed_user_data['name'] = 'UNKNOWN'
    if not user_data.get('bal', None):
        fixed_user_data['bal'] = 0

    return fixed_user_data


print('Are you an existing member?')
if input('(Y/N): ').lower() == 'y':
    while True:
        sys('clear')
        input_username = input('Username? ').lower()
        input_password = input('Password? ').lower()
        with shelve.open('user_accounts') as accounts:
            user_password = accounts.get(input_username, {}).get('password', None)
            if user_password and user_password == input_password:
                break
            else:
                print('\nIncorrect username or password')
                input('[Enter anything to move on]')

    with shelve.open('user_accounts').get(input_username) as user:
        user_data = user_data_fill_out(user, existing=True)
        if not user_data:
            exit()

    print('Name:', user_data['name'])
    print('Balance:', user_data['bal'])
else:
    input_name = input('Full name: ')
    sys('clear')
    while True:
        input_username = input('Username: ')
        with shelve.open('user_accounts')
