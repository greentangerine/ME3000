#!/usr/bin/env python3

from waitress import serve
import sofar
serve(sofar.app, host='0.0.0.0', port=4284)
