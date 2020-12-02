#!/bin/bash

rootDir=$(dirname $0)
rootDir=$(cd ${rootDir}/.. && pwd)
targetDir=$(cd ${rootDir} && basename $(pwd))

docker run -it --mount src="${rootDir}",target=/${targetDir},type=bind --device=/dev/input/rfid:/dev/input/rfid:r --device=/dev/snd ${targetDir}:latest /bin/bash
