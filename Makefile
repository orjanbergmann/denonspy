
build:
	docker build -t denonspy .

run:
	docker run --rm --privileged -v /dev/i2c-1:/dev/i2c-1 -e DENON_IP=$(DENON_IP) denonspy
