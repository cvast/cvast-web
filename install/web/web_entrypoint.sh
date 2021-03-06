#!/bin/bash
run_django_server() {
	if [[ ${DJANGO_DEBUG} == "True" ]]; then
		exec python ${WEB_ROOT}/${WEB_APP_NAME}/manage.py runserver --noreload --nothreading 0.0.0.0:8000
	else
		exec python ${WEB_ROOT}/${WEB_APP_NAME}/manage.py runserver 0.0.0.0:8000
	fi
}

collect_static(){
	python manage.py collectstatic --noinput
}

### Starting point ### 

echo "*** Collecting Django static files ***"
collect_static

echo "*** Running Django server ***"
run_django_server