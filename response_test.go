package marten_test

import (
	"bytes"
	"encoding/json"
	"io"
	"net"
	"testing"

	"bufio"
	"github.com/Shopify/toxiproxy"
	"github.com/Shopify/toxiproxy/toxics"
	"github.com/gaggl/marten"
	tomb "gopkg.in/tomb.v1"
)

func NewTestProxy(name, upstream string) *toxiproxy.Proxy {
	proxy := toxiproxy.NewProxy()

	proxy.Name = name
	proxy.Listen = "localhost:0"
	proxy.Upstream = upstream

	return proxy
}

func WithEchoServer(t *testing.T, f func(string, chan []byte)) {
	ln, err := net.Listen("tcp", "localhost:0")
	if err != nil {
		t.Fatal("Failed to create TCP server", err)
	}

	defer ln.Close()

	response := make(chan []byte, 1)
	tomb := tomb.Tomb{}

	go func() {
		defer tomb.Done()
		src, err := ln.Accept()
		if err != nil {
			select {
			case <-tomb.Dying():
			default:
				t.Fatal("Failed to accept client")
			}
			return
		}

		ln.Close()

		scan := bufio.NewScanner(src)
		if scan.Scan() {
			received := append(scan.Bytes(), '\n')
			response <- received

			src.Write(received)
		}
	}()

	f(ln.Addr().String(), response)

	tomb.Killf("Function body finished")
	ln.Close()
	tomb.Wait()

	close(response)
}

func WithEchoProxy(t *testing.T, f func(proxy net.Conn, response chan []byte, proxyServer *toxiproxy.Proxy)) {
	WithEchoServer(t, func(upstream string, response chan []byte) {
		proxy := NewTestProxy("test", upstream)
		proxy.Start()

		conn, err := net.Dial("tcp", proxy.Listen)
		if err != nil {
			t.Error("Unable to dial TCP server", err)
		}

		f(conn, response, proxy)

		proxy.Stop()
	})
}

func ToxicToJson(t *testing.T, name, typeName, stream string, toxic toxics.Toxic) io.Reader {
	data := map[string]interface{}{
		"name":       name,
		"type":       typeName,
		"stream":     stream,
		"attributes": toxic,
	}
	request, err := json.Marshal(data)
	if err != nil {
		t.Errorf("Failed to marshal toxic for api (1): %v", toxic)
	}

	return bytes.NewReader(request)
}

func DoResponseTest(t *testing.T, downResponse *marten.HttpResponseToxic) {
	WithEchoProxy(t, func(conn net.Conn, response chan []byte, proxy *toxiproxy.Proxy) {
		if downResponse == nil {
			downResponse = &marten.HttpResponseToxic{}
		} else {
			_, err := proxy.Toxics.AddToxicJson(ToxicToJson(t, "response_down", "response", "downstream", downResponse))
			if err != nil {
				t.Error("AddToxicJson returned error:", err)
			}
		}

		msg := []byte("hello world " + "\n")

		_, err := conn.Write(msg)
		if err != nil {
			t.Error("Failed writing to TCP server", err)
		}

		resp := <-response
		if !bytes.Equal(resp, msg) {
			t.Error("Server didn't read correct bytes from client:", string(resp))
		}

		scan := bufio.NewScanner(conn)
		if scan.Scan() {
			resp = append(scan.Bytes(), '\n')
			if !bytes.Equal(resp, msg) {
				t.Error("Client didn't read correct bytes from server:", string(resp))
			}
		}

		proxy.Toxics.RemoveToxic("response_down")

		err = conn.Close()
		if err != nil {
			t.Error("Failed to close TCP connection", err)
		}
	})
}

func TestDownstreamResponse(t *testing.T) {
	DoResponseTest(t, nil)
}

func TestHttpBody(t *testing.T) {
	DoResponseTest(t, &marten.HttpResponseToxic{HttpBody: "{ 'foo': 'bar'}"})
}

func TestHttpStatusCode(t *testing.T) {
	DoResponseTest(t, &marten.HttpResponseToxic{HttpStatusCode: 418})
}

func TestHttpStatusText(t *testing.T) {
	DoResponseTest(t, &marten.HttpResponseToxic{HttpStatusText: "foo bar"})
}
