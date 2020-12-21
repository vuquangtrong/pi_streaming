#!/usr/bin/env python3
# vuquangtrong.github.io

import io
import picamera
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from wsgiref.simple_server import make_server
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIHandler, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication
from threading import Thread, Condition


class FrameBuffer(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
    
    def write(self, buf):
        if buf.startswith(b'\x00\x00\x00\x01'):
            with self.condition:
                self.buffer.seek(0)    
                self.buffer.write(buf)
                self.buffer.truncate()
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()


def stream():
    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        broadcasting = True
        frame_buffer = FrameBuffer()
        camera.start_recording(frame_buffer, format='h264', profile="baseline")
        try:
            WebSocketWSGIHandler.http_version = '1.1'
            websocketd = make_server('', 9000, server_class=WSGIServer,
                     handler_class=WebSocketWSGIRequestHandler,
                     app=WebSocketWSGIApplication(handler_cls=WebSocket))
            websocketd.initialize_websockets_manager()
            websocketd_thread = Thread(target=websocketd.serve_forever)

            httpd = ThreadingHTTPServer(('', 8000), SimpleHTTPRequestHandler)
            httpd_thread = Thread(target=httpd.serve_forever)

            try:
                websocketd_thread.start()
                httpd_thread.start()
                while broadcasting:
                    with frame_buffer.condition:
                        frame_buffer.condition.wait()
                        websocketd.manager.broadcast(frame_buffer.frame, binary=True)
            except KeyboardInterrupt:
                pass
            finally:
                websocketd.shutdown()
                httpd.shutdown()
                broadcasting = False
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            pass
        finally:
            camera.stop_recording()

if __name__ == "__main__":
    stream()
