#!/bin/bash

rootDir=$(dirname $0)
rootDir=$(cd ${rootDir}/.. && pwd)
imageName=$(cd ${rootDir} && basename $(pwd))

docker image build \
  -t ${imageName}:latest  \
  ${rootDir}
