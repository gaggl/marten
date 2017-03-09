VERSION=$(shell git describe --tags)
GODEP_PATH=$(shell pwd)/vendor
ORIGINAL_PATH=$(shell echo $(GOPATH))
COMBINED_GOPATH=$(GODEP_PATH):$(ORIGINAL_PATH)

.PHONY: build clean test package release 

build:
	GOPATH=$(COMBINED_GOPATH) go build -ldflags="-X github.com/Shopify/toxiproxy.Version=$(VERSION)" -o marten .

clean: 
	rm -rf release/
	rm -rf marten

test:
	echo "Testing with" `go version`
	GOPATH=$(COMBINED_GOPATH) go test -v -race .

package:
	mkdir -p release
	GOOS=linux GOARCH=amd64 GOPATH=$(COMBINED_GOPATH) go build -ldflags="-X github.com/Shopify/toxiproxy.Version=$(VERSION)" -o "release/marten_linux_amd64" .

release: clean package
