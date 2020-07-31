build:
	docker build -t ${USER}/dreamdns .

run:
	docker run --env-file=.env ${USER}/dreamdns
	
runlocalweb:
	pipenv run gunicorn --reload -b 0.0.0.0:8000  web:app
