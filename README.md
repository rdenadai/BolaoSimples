## Bolão de Futebol

Pequeno sistema de bolão para se divertir entre amigos.

### Requerimentos:

Para instalar o sistema você deve relizar os seguintes passos:

 - Python (originalmente o sistema foi criado em python 2 mas roda em python 3);
 - pip (package manager)

Comece pelo seguinte, em uma distrubuição linux, no diretório do projeto após *git clone*:

 >$ virtualenv venv
 
 >$ source venv/bin/activate
 
 >$ pip install -r requirements.txt
 
 >$ python manage.py collectstatic
 
 Antes de executar o comando abaixo, tenha certeza que criou o banco de dados, 
 veja o settings.py para ver configurações de DATABASE.
 
 >$ python manage.py migrate
 
 >$ python manage.py createsuperuser
 
 >$ gunicorn -b 0.0.0.0:8080 -w 3 wsgi:application --log-level debug --error-logfile bolao_gunicorn.log
 
 Pronto, ao acessa http://localhost:8080 você deve conseguir visualizar o sistema.
 
 Por fim, execute o arquivo data/data.sql, ele irá fornecer uma base pequena mas inicial de campeonatos e times.
 
 Bom divertimento! ;)