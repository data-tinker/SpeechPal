build:
	docker build --build-arg BOT_TOKEN --build-arg OPENAI_API_KEY --build-arg OPENAI_ORG --tag speechpal-mvp .

run:
	docker run -p 8080:8080 speechpal-mvp

build-remote:
	gcloud builds submit --region=us-west2 --tag us-west2-docker.pkg.dev/horizontal-leaf-386604/speechpal-repo/speechpal-image

run-remote:
	gcloud run deploy --image us-west2-docker.pkg.dev/horizontal-leaf-386604/speechpal-repo/speechpal-image
