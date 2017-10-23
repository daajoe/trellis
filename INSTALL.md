# Installation of trellis
## Installation on Linux Ubuntu (tested on trusty)
```bash
sudo apt-get install git make cmake build-essential mono-complete openjdk-8-jdk gradle automake stx-btree-dev libboost-graph-dev libboost-thread-dev libboost-system-dev zlib1g-dev libtool python-pip gcc xz-utils liblzma-dev
pip install --user --upgrade pip
```

```bash
git clone https://github.com/daajoe/trellis.git
cd trellis
cmake .
make
pip install --user -r requirements.txt
```
Notes:
- Upgrade cmake if cmake <3.5 (see Upgrade cmake below)
- If you have multiple cores then you might want to run make in parallel using ``make -j5`` to get things done a little faster.

## Installation on Debian (jessie)
```bash
sudo apt-get install git make cmake build-essential mono-complete automake stx-btree-dev libboost-graph-dev libboost-thread-dev libboost-system-dev zlib1g-dev libtool python-pip gcc python-dev libyaml-dev libpython2.7-dev xz-utils liblzma-dev
pip install --user --upgrade pip
```

#### Install backports manually
```bash
apt install -t jessie-backports cmake
```
Edit the */etc/apt/sources.list*:
```bash
sudo vi /etc/apt/sources.list
```
Add the following lines:
```bash
# Backports repository
deb http://deb.debian.org/debian jessie-backports main contrib non-free
deb http://deb.debian.org/debian jessie-backports-sloppy main contrib non-free
```

#### Upgrade cmake (from backports)
Requred if only cmake <3.5 is present on your system. For details see <https://wiki.debian.org/Backports>

Run
```bash
sudo apt-get update
apt-cache show cmake  | grep Version | head -n1 
```
Take version number (>=3.5) and run
```bash
sudo apt-get install cmake=VERSION cmake-data=VERSION
```

#### Install jdk8 (from backports)
```bash
apt install -t jessie-backports  openjdk-8-jre-headless openjdk-8-jdk ca-certificates-java
```
Requires backports (see above for cmake)

#### Install gradle
See <https://gradle.org/install/#with-the-gradle-wrapper> Section "Install manually"

#### Install trellis 
```bash
git clone https://github.com/daajoe/trellis.git
cd trellis
cmake .
make
pip install --user -r requirements.txt
```

## Installation on Centos
TODO
vagrant init centos/7
vagrant up


## Installation on OSX/Windows
Not supported, because the subsolvers might not compile on OSX/Windows. 

Please install [virtual box](https://www.virtualbox.org/wiki/Downloads) and [vagrant](https://www.vagrantup.com/downloads.html).
```bash
vagrant init ubuntu/xenial64
vagrant up
```
Then, proceed with Linux installation. Note that we require more than *2GB memory* to compile (due to mono builds for bztreewidth).


## System Requirements 
0) System
    1) Memory: 2GB
    2) Disk: 1GB (due to gradle/jdk8/mono dependencies for external solvers)
1) Linux (Debian)
2) Trellis
    - cmake > 3.5
    - python 2.7
    - pip
    - requirements.txt (python dependencies)
    - xz-utils (for compressed files)
3) Sub-Solvers
    - automake (tdlib)
    - boost graph, thread, system (tdlib)
    - libtool (tdlib)
    - mono-complete
    - gradle (jdrasil)
    - jdk7 (jdrasil, tamaki)
    - mono (bztreewidth)
    - stx-btree-dev (tdlib)
    - zlib (jdrasil/glucose)
