# Mixture-of-Communication-Pattern

######  b07901143 Chou, Zi-Ting

## Enviroment
- Ubuntu 20.04.3
- python 3.8.8

## How to run
- Install project dependencies
```bash
# install compliler & buildtools & required python module
sh installation.sh
```

- Compile protobuf schema to python wrapper
```bash
sh make.sh
```

- start the docker
```
docker run -d -it -p 1883:1883 --name iothw -v "$(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf" eclipse-mosquitto
```

- start fibonacci server
```python
# new terminal
cd service/fibo
python3 server.py --ip 0.0.0.0 --port 8080
```
- start logging server
```python
# new terminal
cd service/log
python3 server.py --ip localhost --port 8888
```
- start rest server
```python
# new terminal
cd rest
python3 manage.py migrate
python3 manage.py runserver
```
## Use curl to perform client request
- Post
```bash
# 10 is request order, change to whatever integer you want 
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/rest/fibonacci/ -d "{\"order\":\"10\"}"
```
- result:
```
{"order":10,"answer":55}
```
- Get
```bash
# get order history & answer history
curl http://localhost:8000/rest/logs
```
and you should get
```
{"history order":[10,20],"history answer":[55,6765]}
```
## Demo Video
{%youtube cyQAdSCKwuM %}
