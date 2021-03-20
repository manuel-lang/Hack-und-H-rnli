api-docker:
	docker build -f Dockerfile.api -t api .
	docker run -it -p 5000:80 api
api-source:
	python3 api/api.py