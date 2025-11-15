from flask import Flask


class RunServer:
    def __init__(self, server: None)-> None:
        self.app = Flask(__name__)
        self.server = server
        self.action()
    def action(self):
        print("action")

