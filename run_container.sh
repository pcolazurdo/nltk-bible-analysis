#!/bin/bash
docker run -it --rm -v `pwd`:/tf/bible -v $HOME/.ssh:/root/.ssh -p 8888:8888 tensorflow/tensorflow:latest-py3-jupyter
