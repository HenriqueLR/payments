clean:
	@find . -name "*.pyc" | xargs rm -f

start: clean
	./app/manage.py runserver 0.0.0.0:8000 --settings=conf.settings

init_config:
	./app/manage.py syncdb --settings=conf.settings

migrate:
	./app/manage.py makemigrations --settings=conf.settings
	./app/manage.py migrate --settings=conf.settings

install:
	pip install -r requirements.txt