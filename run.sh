#!/bin/bash

export PYTHONPATH=$PWD/../::$PYTHONPATH
python -m flask run --host=0.0.0.0 --port=8088
