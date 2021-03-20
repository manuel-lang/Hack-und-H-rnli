api-docker:
	docker build -f Dockerfile.api -t api .
	docker run -it -p 5000:80 api
api-source:
	python3 api/api.py
frontend-docker:
	docker build -f Dockerfile.frontend -t frontend .
	docker run -it -p 3000:80 frontend
frontend-source:
	cd frontend
	npm start