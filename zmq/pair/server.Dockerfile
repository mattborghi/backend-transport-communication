FROM julia:1.6-buster

# Solve term warnings
# https://github.com/phusion/baseimage-docker/issues/58
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /julia_server

COPY server.jl ./server.jl

# Download latest listing of available packages:
RUN apt-get -y -qq update
RUN apt-get install -y -qq apt-utils dialog git
# Upgrade already installed packages:
RUN apt-get -y -qq upgrade

ENV JULIA_DEPOT_PATH "/julia_server/.julia/packages/:$JULIA_DEPOT_PATH"

RUN julia -e 'import Pkg; Pkg.add("ZMQ"); Pkg.instantiate(); Pkg.precompile()'

# RUN useradd -ms /bin/bash borghi
# USER borghi
# EXPOSE 5556
# Run our file
CMD julia server.jl