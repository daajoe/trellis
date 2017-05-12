# trellis
TREewidth LocaL Improvement Solver

## System Requirements
- mono (for BZTreewidth install using: apt-get install mono-complete)
- openjdk-5 (for Jdrasil install using: apt-get install openjdk-8-jdk)
- python 2.7
- pip

## Installation
git clone --recursive git@github.com:daajoe/trellis.git

cmake .

make -j5

## Run
bin/trellis -f graph.gr
