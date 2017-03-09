package main

import (
	"bytes"
	"encoding/json"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/Shopify/toxiproxy"
	"github.com/Shopify/toxiproxy/toxics"
	"github.com/stretchr/testify/assert"
)

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

func DoResponseTest(t *testing.T, downResponse *HttpResponseToxic) (int, string, string) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		io.WriteString(w, `{"hello": "world"}`)
	}))
	defer ts.Close()

	proxy := toxiproxy.NewProxy()
	proxy.Name = "test"
	proxy.Listen = "localhost:0"
	proxy.Upstream = ts.Listener.Addr().String()
	proxy.Start()

	if downResponse == nil {
		downResponse = &HttpResponseToxic{}
	} else {
		_, err := proxy.Toxics.AddToxicJson(ToxicToJson(t, "response_down", "response", "downstream", downResponse))
		if err != nil {
			t.Error("AddToxicJson returned error:", err)
		}
	}

	response, err := http.Get("http://" + proxy.Listen)
	if err != nil {
		log.Fatal(err)
	}

	responseBody, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatal(err)
	}

	return response.StatusCode, response.Status, string(responseBody)
}

func TestDownstreamResponse(t *testing.T) {
	assert := assert.New(t)

	code, status, body := DoResponseTest(t, nil)
	assert.Equal(200, code, "This test should not have manipultated the status code")
	assert.Equal(`200 OK`, status, "This test should not have manipultated the status")
	assert.Equal(`{"hello": "world"}`, body, "This test should not have manipultated the body")
}

func TestHttpStatusCode(t *testing.T) {
	assert := assert.New(t)

	code, status, body := DoResponseTest(t, &HttpResponseToxic{HttpStatusCode: 418})
	assert.Equal(418, code, "This test should have manipultated the status code")
	assert.Equal(`418 200 OK`, status, "This test should not have manipultated the status")
	assert.Equal(`{"hello": "world"}`, body, "This test should not have manipultated the body")
}

func TestHttpStatusText(t *testing.T) {
	assert := assert.New(t)

	code, status, body := DoResponseTest(t, &HttpResponseToxic{HttpStatusText: "FOO"})
	assert.Equal(200, code, "This test should not have manipultated the status code")
	assert.Equal(`200 FOO`, status, "This test should have manipultated the status")
	assert.Equal(`{"hello": "world"}`, body, "This test should not have manipultated the body")
}

func TestHttpBody(t *testing.T) {
	assert := assert.New(t)

	code, status, body := DoResponseTest(t, &HttpResponseToxic{HttpBody: "{'foo': 'bar'}"})
	assert.Equal(200, code, "This test should not have manipultated the status code")
	assert.Equal(`200 OK`, status, "This test should not have manipultated the status")
	assert.Equal(`{'foo': 'bar'}`, body, "This test should have manipultated the body")
}
