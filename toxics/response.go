package toxics

import (
	"bufio"
	"bytes"
	"io"
	"io/ioutil"
	"net/http"

	"github.com/Shopify/toxiproxy/stream"
	"github.com/Shopify/toxiproxy/toxics"
)

type HttpResponseToxic struct {
	HttpBody       string `json:"body"`
	HttpStatusCode int    `json:"code"`
	HttpStatusText string `json:"text"`
}

func (t *HttpResponseToxic) ModifyResponse(resp *http.Response) {
	if t.HttpBody != "" {
		resp.Body = ioutil.NopCloser(bytes.NewBufferString(t.HttpBody))
		resp.ContentLength = int64(len(t.HttpBody))
	}
	if t.HttpStatusCode > 0 {
		resp.StatusCode = t.HttpStatusCode
	}
	if t.HttpStatusText != "" {
		resp.Status = t.HttpStatusText
	}
}

func (t *HttpResponseToxic) Pipe(stub *toxics.ToxicStub) {
	buffer := bytes.NewBuffer(make([]byte, 0, 32*1024))
	writer := stream.NewChanWriter(stub.Output)
	reader := stream.NewChanReader(stub.Input)
	reader.SetInterrupt(stub.Interrupt)
	for {
		tee := io.TeeReader(reader, buffer)
		resp, err := http.ReadResponse(bufio.NewReader(tee), nil)
		if err == stream.ErrInterrupted {
			buffer.WriteTo(writer)
			return
		} else if err == io.EOF {
			stub.Close()
			return
		}
		if err != nil {
			buffer.WriteTo(writer)
		} else {
			t.ModifyResponse(resp)
			resp.Write(writer)
		}
		buffer.Reset()
	}
}

func init() {
	toxics.Register("response", new(HttpResponseToxic))
}
