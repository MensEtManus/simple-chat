#!/usr/bin/env python
# Albert Yang
# ECE695 Warm-up 5

import sys, os
import tornado.ioloop
import tornado.web
import logging
import sockjs.tornado

# Settings
PORT = 8888
DEBUG = True

class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render('index.html')


class ChatConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    # Class level variable
    clients = set()

    def on_open(self, info):
        # Send that someone joined
        self.broadcast(self.clients, "Someone joined.")

        # Add client to the clients list
        self.clients.add(self)

    def on_message(self, message):
        # Broadcast message
        self.broadcast(self.clients, message)

    def on_close(self):
        # Remove client from the clients list and broadcast leave message
        self.clients.remove(self)

        self.broadcast(self.clients, "Someone left.")

if __name__ == "__main__":
    def main():
      logging.getLogger().setLevel(logging.DEBUG)

      # Create chat router
      ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/chat')

      # Create Tornado application
      app = tornado.web.Application(
              [(r"/", IndexHandler)] + ChatRouter.urls
      )

      # Make Tornado app listen on port 8080
      app.listen(port=PORT) 
      sys.stderr.write("Starting server at http://localhost:%d\n" % PORT)
      # Start IOLoop
      tornado.ioloop.IOLoop.instance().start()

    main()
