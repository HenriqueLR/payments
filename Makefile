#makefile

config: clean migrate create_superuser start

install:
	pip install -r requirements.txt

clean:
	@find . -name "*.pyc" | xargs rm -f

create_superuser:
	@if [ $(settings) ]; then \
		python ./app/conf/config_start.py "conf.settings_production" ;\
	else \
		python ./app/conf/config_start.py "conf.settings" ;\
	fi

start: clean
	@if [ $(settings) ]; then \
		./app/manage.py runserver 0.0.0.0:8000 --settings=conf.settings_production ;\
	else \
		./app/manage.py runserver 0.0.0.0:8000 ;\
	fi

migrate:
	@if [ $(settings) ]; then \
		./app/manage.py makemigrations --settings=conf.settings_production ;\
		./app/manage.py migrate --settings=conf.settings_production ;\
	else \
		./app/manage.py makemigrations ;\
		./app/manage.py migrate ;\
	fi

clean_migrations:
	rm -rf ./app/wallet/migrations/*.pyc
	find ./app/wallet/migrations/ |grep '0'|xargs rm -f
	rm -rf ./app/accounts/migrations/*.pyc
	find ./app/accounts/migrations/ |grep '0'|xargs rm -f

clean_sqlitedb:
	rm -rf ./app/db.sqlite3
	rm -rf ./db.sqlite3

capture_words:
	./app/manage.py makemessages -l en

compile_words:
	./app/manage.py compilemessages