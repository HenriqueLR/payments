clean:
	@find . -name "*.pyc" | xargs rm -f

start: clean
	./app/manage.py runserver 0.0.0.0:8000 --settings=conf.settings_production

config: clean migrate create_superuser start

migrate:
	./app/manage.py makemigrations --settings=conf.settings_production
	./app/manage.py migrate --settings=conf.settings_production

install:
	pip install -r requirements.txt

create_superuser:
	python ./app/conf/config_start.py

clean_migrations:
	rm -rf ./app/wallet/migrations/*.pyc
	find ./app/wallet/migrations/ |grep '0'|xargs rm -f
	rm -rf ./app/accounts/migrations/*.pyc
	find ./app/accounts/migrations/ |grep '0'|xargs rm -f