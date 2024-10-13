echo "Version (2.0):"
read VERSION
test -z "${VERSION}" && VERSION=2.0 
echo "Version to generate : $VERSION"
docker build --tag pimpmysuperwatt:$VERSION .
docker login
docker tag pimpmysuperwatt:$VERSION docker.io/coxifred/pimpmysuperwatt:$VERSION
docker push coxifred/pimpmysuperwatt:$VERSION

docker tag docker.io/coxifred/pimpmysuperwatt:${VERSION} docker.io/coxifred/pimpmysuperwatt:latest
docker push  docker.io/coxifred/pimpmysuperwatt:latest
