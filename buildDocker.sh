echo -e "Version (2.0): \c"
read VERSION
test -z "${VERSION}" && VERSION=2.0 
echo -e "Arch ($(uname -m | cut -c1-3)): \c"
read ARCH
test -z "${ARCH}" && ARCH="-$(uname -m | cut -c1-3)"
test "${ARCH}" = "-x86" && ARCH=""

VERSION=$VERSION${ARCH}
echo "Version to generate : $VERSION press enter to continue " ; read SUITE
DOCKER_FILE=""
if [ "$(uname -m | cut -c1-3)" = "arm" ]
 then
  echo "Overriding Dockerfile to Arm one"
  DOCKER_FILE="-f DockerfileArm"
fi
echo "docker build --tag pimpmysuperwatt:$VERSION . ${DOCKER_FILE}" ; sleep 0.5
docker build --tag pimpmysuperwatt:$VERSION . ${DOCKER_FILE}
docker login
docker tag pimpmysuperwatt:$VERSION docker.io/coxifred/pimpmysuperwatt:$VERSION
docker push coxifred/pimpmysuperwatt:$VERSION

docker tag docker.io/coxifred/pimpmysuperwatt:${VERSION} docker.io/coxifred/pimpmysuperwatt:$VERSION
docker push  docker.io/coxifred/pimpmysuperwatt:$VERSION
