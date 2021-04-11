build:
	docker build -t ${USER}/dreamdns .

run:
	docker run --env-file=.env -p 9083:8080 ${USER}/dreamdns
	
runlocalweb:
	pipenv run gunicorn --reload -b 127.0.0.1:14001  web:app

deploy-k8s:
	./k8s/deploy.sh
	kubectl apply -f k8s/service.yaml

delete-k8s:
	kubectl delete -f k8s/deploy.yaml.template
	kubectl delete -f k8s/service.yaml