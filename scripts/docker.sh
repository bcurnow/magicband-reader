#!/bin/bash

rootDir=$(dirname $0)
rootDir=$(cd ${rootDir}/.. && pwd)
targetDir=$(cd ${rootDir} && basename $(pwd))

docker run -it --group-add $(getent group gpio | cut -d: -f3) --group-add kmem --privileged --device=/dev/input/rfid --device=/dev/snd --device=/dev/gpiomem --mount src="${rootDir}",target=/${targetDir},type=bind ${targetDir}:latest /bin/bash
