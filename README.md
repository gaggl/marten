# Marten, Http Chaos Monkey Server

Marten provides a way to test your upstream application or proxy server by randomly returning HTTP codes with a predefined
probability.

Marten is an extension of toxiproxy proper with 1 additional toxic, namely the status toxic. This allows the user to modify
http response bodies.

## Update Dependencies

    go get -u github.com/Shopify/toxiproxy
    govendor update +local

## Buid
    go build

## Config

As marten is an extension of toxiproxy, so we like to point you to its [manual](https://github.com/Shopify/toxiproxy).

```
$ toxiproxy-cli toxic add marten -t response [-a code=500] [-a text="foobarbqq"] [-a body='{ "foo": "bar" }']
```

## Run

    ./marten [ --config example/marten.json ]


