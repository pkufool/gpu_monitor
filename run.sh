#!/bin/bash

export PYTHONPATH=$PWD/../::$PYTHONPATH
flask run --host=0.0.0.0 --port=8088
