AWS_REGION=af-south-1
PROFILE_AWS=classifydepl
ACC_ID=760751342917

run:
	python -m app.app

build-local:
	docker build -t nexus-media-local .

run-local:
	docker run -p 5000:5000 nexus-media-local:latest

build-lam:
	docker build -t ${ACC_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/nexusmedia:latest . -f Dockerfile.aws.lambda

push:
	AWS_PROFILE=${PROFILE_AWS} aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ACC_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
	docker push ${ACC_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/nexusmedia:latest