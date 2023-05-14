build:
	docker build --build-arg BOT_TOKEN --build-arg OPENAI_API_KEY --build-arg OPENAI_ORG --tag speechpal-mvp:mac .

build-linux:
	docker build --platform linux/amd64 --build-arg BOT_TOKEN --build-arg OPENAI_API_KEY --build-arg OPENAI_ORG --tag speechpal-mvp .

run:
	docker run -p 8080:8080 speechpal-mvp:mac

build-cloud:
	gcloud builds submit --region=us-west2 --tag us-west2-docker.pkg.dev/horizontal-leaf-386604/speechpal-repo/speechpal-image

run-cloud:
	gcloud run deploy --image us-west2-docker.pkg.dev/horizontal-leaf-386604/speechpal-repo/speechpal-image
