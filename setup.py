import os

print('checking for required packages')
try:
    import flask
    import jwt
    print('required packages found')
    os.system('python3 app.py')
except ImportError:
    os.system('pip3 install -r requirements.txt')
    print('required packages installed')
    try:
        import flask
        import jwt
        os.system('python3 app.py')
    except ImportError:
        print("you need to install packages by running pip3 install -r requirements.txt before continuing")