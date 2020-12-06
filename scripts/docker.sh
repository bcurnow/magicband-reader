#!/bin/bash

rootDir=$(dirname $0)
rootDir=$(cd ${rootDir}/.. && pwd)
targetDir=$(cd ${rootDir} && basename $(pwd))

docker run -it --privileged --mount src=/dev,target=/dev,type=bind --mount src=${rootDir}/../sounds,target=/sounds,type=bind --mount src="${rootDir}",target=/${targetDir},type=bind ${targetDir}:latest /bin/bash
