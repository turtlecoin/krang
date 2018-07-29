# Copyright (c) 2018, Nicholas Orr, The TurtleCoin Developers
# 
# Please see the included LICENSE file for more information.


# clone the turtlecoin/krang repo to home dir
# > git clone https://github.com/turtlecoin/krang.git ~/krang
#
# need to build debian stretch slim rootfs first
# > git clone https://github.com/debuerreotype/debuerreotype.git ~/debuerreotype
# > cd ~/debuerreotype
#
# see http://snapshot.debian.org/archive/debian/ for timestamp 
# > export DEBIAN_TIMESTAMP="2018-07-29T09:08:12Z"
# > sudo debuerreotype/build.sh --arch=amd64 output stretch $DEBIAN_TIMESTAMP
#
# copy the rootfs to same directory as this Dockerfile
# > cp output/$DEBIAN_TIMESTAMP/amd64/stretch/slim/rootfs.tar.xz ~/krang/docker/debian-stretch-slim-rootfs.tar.xz && touch ~/krang/docker/debian-stretch-slim-rootfs.${DEBIAN_TIMESTAMP//[-:]/}
#
# build mainnet first to sync blocks, need to stop at block 663,300
# > sudo docker build -t turtlecoind/mainnet:v0.6.3 --target turtlecoind .
#
# create the volume to store mainnet chain
# > sudo docker volume create mainnet-data
#
# start TurtleCoind to get mainnet chain - remember to stop before block 663,300
# > sudo docker run -d --restart=unless-stopped --name trtl-mainnet --mount source=mainnet-data,target=/home/node/data turtlecoind/mainnet:v0.6.3
#
# stop the container
# > sudo docker stop trtl-mainnet
#
# compress the blocks to reduce space as they get copied a lot going forward
# > sudo rm /var/lib/docker/volumes/mainnet-data/_data/p2pstate.bin /var/lib/docker/volumes/mainnet-data/_data/core
# > sudo tar -cJf ~/krang/docker/blocks.tar.xz /var/lib/docker/volumes/mainnet-data/_data/*
#
# uncomment the next lot of work in this Dockerfile and build again
# > sudo docker build -t turtlecoind/testnet-dev-zero --target testnet-dev-zero .
# > sudo docker build -t turtlecoind/testnet-dev-clone --target testnet-dev-clone .
# > sudo docker build -t turtlecoind/testnet-main-clone --target testnet-main-clone .


FROM scratch as debian
ADD debian-stretch-slim-rootfs.tar.xz /
CMD ["bash"]


FROM debian as builder
WORKDIR /build
RUN apt-get update && \
    apt-get install -y \
        git \
        build-essential \
        python-dev \
        gcc \
        g++ \
        cmake \
        libboost-all-dev \
        librocksdb-dev \
        libreadline-dev

CMD ["bash"]


FROM builder as built
WORKDIR /build
RUN git clone --depth 1 -b master https://github.com/turtlecoin/turtlecoin.git trtl-mainnet && \
  mkdir turtlecoin/build && \
  cd turtlecoin/build && \
  cmake -DCMAKE_BUILD_TYPE=Release -DSTATIC=true -DDO_TESTS=OFF ..&& \
  make -j$(nproc)

# These repos aren't ready to go yet.
#
# RUN git clone --depth 1 -b testnet-main-clone https://github.com/turtlecoin/testnet.git testnet-main-clone && \
#   mkdir turtlecoin/build && \
#   cd turtlecoin/build && \
#   cmake -DCMAKE_BUILD_TYPE=Release -DSTATIC=true -DDO_TESTS=OFF ..&& \
#   make -j$(nproc)
# 
# RUN git clone --depth 1 -b testnet-dev-clone https://github.com/turtlecoin/testnet.git testnet-dev-clone && \
#   mkdir turtlecoin/build && \
#   cd turtlecoin/build && \
#   cmake -DCMAKE_BUILD_TYPE=Release -DSTATIC=true -DDO_TESTS=OFF ..&& \
#   make -j$(nproc)
# 
# RUN git clone --depth 1 -b testnet-dev-zero https://github.com/turtlecoin/testnet.git testnet-dev-zero && \
#   mkdir turtlecoin/build && \
#   cd turtlecoin/build && \
#   cmake -DCMAKE_BUILD_TYPE=Release -DSTATIC=true -DDO_TESTS=OFF ..&& \
#   make -j$(nproc)

CMD ["/bin/bash"]


FROM debian as nodebloat

RUN set -ex; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
    gnupg2 \
    dirmngr \
    curl \
    ca-certificates \
  ; \
  rm -rf /var/lib/apt/lists/*

# gpg keys listed at https://github.com/nodejs/node#release-team
RUN set -ex \
  && for key in \
    94AE36675C464D64BAFA68DD7434390BDBE9B9C5 \
    FD3A5288F042B6850C66B31F09FE44734EB7990E \
    71DCFD284A79C3B38668286BC97EC7A07EDE3FC1 \
    DD8F2338BAE7501E3DD5AC78C273792F7D83545D \
    C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 \
    B9AE9905FFD7803F25714661B63B535A4C206CA9 \
    56730D5401028683275BD23C23EFEFE93C4CFFFE \
    77984A986EBC2AA786BC0F66B01FBB92821C587A \
    8FCCA13FEF1D0C2E91008E09770F7A9A5AE15600 \
  ; do \
    gpg --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys "$key" || \
    gpg --keyserver hkp://ipv4.pool.sks-keyservers.net --recv-keys "$key" || \
    gpg --keyserver hkp://pgp.mit.edu:80 --recv-keys "$key" ; \
  done

ENV NODE_VERSION 10.7.0
ENV ARCH x64

RUN  curl -fsSLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$ARCH.tar.gz" \
  && curl -fsSLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
  && gpg --batch --decrypt --output SHASUMS256.txt SHASUMS256.txt.asc \
  && grep " node-v$NODE_VERSION-linux-$ARCH.tar.gz\$" SHASUMS256.txt | sha256sum -c -

ENV YARN_VERSION 1.7.0

RUN set -ex \
  && for key in \
    6A010C5166006599AA17F08146C2130DFD2497F5 \
  ; do \
    gpg --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys "$key" || \
    gpg --keyserver hkp://ipv4.pool.sks-keyservers.net --recv-keys "$key" || \
    gpg --keyserver hkp://pgp.mit.edu:80 --recv-keys "$key" ; \
  done \
  && curl -fsSLO --compressed "https://yarnpkg.com/downloads/$YARN_VERSION/yarn-v$YARN_VERSION.tar.gz" \
  && curl -fsSLO --compressed "https://yarnpkg.com/downloads/$YARN_VERSION/yarn-v$YARN_VERSION.tar.gz.asc" \
  && gpg --batch --verify yarn-v$YARN_VERSION.tar.gz.asc yarn-v$YARN_VERSION.tar.gz


CMD [ "bash" ]


FROM debian as node

RUN groupadd --gid 1000 node \
  && useradd --uid 1000 --gid node --shell /bin/bash --create-home node

# Install node
COPY --from=nodebuilder /node-v10.7.0-linux-x64.tar.gz /node-v10.7.0-linux-x64.tar.gz
RUN set -ex \
  && tar -xzf "node-v10.7.0-linux-x64.tar.gz" -C /usr/local --strip-components=1 --no-same-owner \
  && rm "node-v10.7.0-linux-x64.tar.gz" \
  && ln -s /usr/local/bin/node /usr/local/bin/nodejs

# Install yarn
COPY --from=nodebuilder /yarn-v1.7.0.tar.gz /yarn-v1.7.0.tar.gz
RUN set -ex \
  && mkdir -p /opt \
  && tar -xzf yarn-v1.7.0.tar.gz -C /opt/ \
  && ln -s /opt/yarn-v1.7.0/bin/yarn /usr/local/bin/yarn \
  && ln -s /opt/yarn-v1.7.0/bin/yarnpkg /usr/local/bin/yarnpkg \
  && rm yarn-v1.7.0.tar.gz

# Install pm2
RUN yarn install pm2 -g && \
    pm2 install pm2-logrotate && \
    pm2 set pm2-logrotate:retain 7 && \
    pm2 set pm2-logrotate:compress true

# Expose ports needed to use Keymetrics.io
EXPOSE 80 443 43554

# Start pm2.json process file
CMD ["pm2-runtime", "start", "pm2.json"]


FROM node as turtlecoind

USER node
WORKDIR /home/node

# trtl-mainnet
COPY --from=built /build/trtl-mainnet/build/src/TurtleCoind /home/node/TurtleCoind
ADD trtl-mainnet.tar.xz .

# TODO this yarn install needs to be fixed later, need a static list of deps from a git repo
# need to minimise random injections of code and verify what is being installed is legit
RUN yarn install --production

# p2p-bind-port
EXPOSE 11897
# rpc-bind-port
EXPOSE 11898

# Show current folder structure in logs
RUN ls -al -R

CMD [ "pm2-runtime", "start", "trtl-mainnet.js" ]



# FROM node as testnet-dev-zero
# 
# USER node
# WORKDIR /home/node
# 
# COPY --from=built /build/testnet-dev-zero/build/src/TurtleCoind /home/node/testnet-dev-zero
# ADD testnet-dev-zero.tar.xz .
# 
# # TODO this yarn install needs to be fixed later, need a static list of deps from a git repo
# # need to minimise random injections of code and verify what is being installed is legit
# RUN yarn install --production
# 
# # p2p-bind-port
# EXPOSE 11897
# # rpc-bind-port
# EXPOSE 11898
# 
# # Show current folder structure in logs
# RUN ls -al -R
# 
# CMD [ "pm2-runtime", "start", "testnet-dev-zero.js" ]


# FROM node as addblocks
# 
# USER node
# WORKDIR /home/node
# 
# ADD blocks.tar.xz data/
# 
# CMD ["bash"]


# FROM addblocks as testnet-dev-clone
# 
# USER node
# WORKDIR /home/node
# 
# COPY --from=built /build/testnet-dev-clone/build/src/TurtleCoind /home/node/testnet-dev-clone
# ADD testnet-dev-clone.tar.xz .
# 
# # TODO this yarn install needs to be fixed later, need a static list of deps from a git repo
# # need to minimise random injections of code and verify what is being installed is legit
# RUN yarn install --production
# 
# # p2p-bind-port
# EXPOSE 11897
# # rpc-bind-port
# EXPOSE 11898
# 
# # Show current folder structure in logs
# RUN ls -al -R
# 
# CMD [ "pm2-runtime", "start", "testnet-dev-clone.js" ]


# FROM addblocks as testnet-main-clone
# 
# USER node
# WORKDIR /home/node
# 
# # trtl-mainnet
# COPY --from=built /build/trtl-mainnet/build/src/TurtleCoind /home/node/TurtleCoind
# ADD trtl-mainnet.tar.xz .
# 
# COPY --from=built /build/testnet-dev-clone/build/src/TurtleCoind /home/node/testnet-dev-clone
# ADD testnet-dev-clone.tar.xz .
# 
# # TODO this yarn install needs to be fixed later, need a static list of deps from a git repo
# # need to minimise random injections of code and verify what is being installed is legit
# RUN yarn install --production
# 
# # p2p-bind-port
# EXPOSE 11897
# # rpc-bind-port
# EXPOSE 11898
# 
# # Show current folder structure in logs
# RUN ls -al -R
# 
# CMD [ "pm2-runtime", "start", "testnet-main-clone.js" ]


# TODO got to figure best way to do this, get daemons sorted first, taking forever to compress the blocks
#
# FROM debian as service
# WORKDIR /data
# 
# COPY --from=trtlmainnet /build/turtlecoin/build/src/walletd /walletd
# 
# # rpc-bind-port
# EXPOSE 8070
# 
# ENTRYPOINT ["/walletd"]
# CMD ["--rpc-password", "password", "--container-file", "/data/container", "--container-password", "password", "--local", "--data-dir", "/data", "--hide-my-port", "--log-file", "/dev/null" ]
# 
# 
# FROM debian as miner
# WORKDIR /
# 
# COPY --from=trtlmainnet /build/turtlecoin/build/src/miner .
# 
# ENTRYPOINT ["/miner"]
# CMD ["--daemon-host", "turtlecoind", "--threads", "1", "--log-level", "4", "--address", "over-ride-cmd-and-specify-address"]
