import sys
sys.path.insert(0, '/home/admin/web/secretshop.cyberiasport.ru/private/secretshop.cyberiasport.ru/')

from manage import app as application

activate_this = '/home/admin/web/secretshop.cyberiasport.ru/private/secretshop.cyberiasport.ru/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))