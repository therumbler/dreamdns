build:
	docker build -t ${USER}/dreamdns .

run:
	docker run --env-file=.env ${USER}/dreamdns
	
runlocalweb:
	pipenv run gunicorn --reload -b 127.0.0.1:14001  web:app
