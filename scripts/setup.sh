docker build . -t cider-eval:latest;
ID=$(docker run -dit cider-eval:latest);
docker attach $ID
