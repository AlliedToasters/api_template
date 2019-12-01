FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6

ENV redisurl="http://download.redis.io/redis-stable.tar.gz"
RUN curl -s -o redis-stable.tar.gz $redisurl
RUN mkdir -p /usr/local/lib/
RUN chmod a+w /usr/local/lib/
RUN tar -C /usr/local/lib/ -xzf redis-stable.tar.gz
RUN cd /usr/local/lib/redis-stable/ && make && make install
RUN mkdir -p /etc/redis/
RUN touch /etc/redis/6379.conf
COPY ./redis.conf /etc/redis/6379.conf

COPY ./requirements* /app/
COPY ./results.json /app/results.json
COPY ./start.sh /start.sh
RUN chmod 755 /start.sh
RUN pip install -r /app/requirements-dev.txt

RUN mkdir /app/app
WORKDIR /app

COPY ./app /app/app
COPY ./unit_tests /app/unit_tests

ENTRYPOINT /start.sh
