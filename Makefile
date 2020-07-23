build:
	docker build -t ${USER}/dreamdns .

run:
	docker run --env-file=.env ${USER}/dreamdns
	
