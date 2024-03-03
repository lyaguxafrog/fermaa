#!/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from dotenv import load_dotenv, find_dotenv

from farm import app, db, socketio

load_dotenv(find_dotenv())

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'create-user':
        import farm.services.create_user_by_command
    elif len(sys.argv) > 1 and sys.argv[1] == 'debug':
        with app.app_context():
            db.create_all()
            socketio.run(app, debug=False, host='0.0.0.0',
                         port=8080, allow_unsafe_werkzeug=True)
    elif len(sys.argv) > 1 and sys.argv[1] == 'run':
        with app.app_context():
            db.create_all()
            socketio.run(app, debug=False, host='0.0.0.0', port=8080,
                         allow_unsafe_werkzeug=True) # type: ignore
