import os

def shutdown():
    if os.name == 'nt':
        os.system('shutdown /s /t 0')
    elif os.name == 'posix':
        os.system('shutdown now')
    else:
        print(' [ ! ] Unsupported operating system.')

def restart():
    if os.name == 'nt':
        os.system('shutdown /r /t 0')
    elif os.name == 'posix':
        os.system('reboot now')
    else:
        print(' [ ! ] Unsupported operating system.')
