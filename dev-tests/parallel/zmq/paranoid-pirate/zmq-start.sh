python3 zmq-ppqueue.py &
for i in 1 2 3 4; do
    python3 zmq-ppworker.py &
    sleep 1
done
python3 zmq-lpclient.py &
