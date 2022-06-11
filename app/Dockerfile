FROM ubuntu:latest

RUN apt-get update -y 
RUN apt install python3 -y
RUN apt-get install python3-pip -y

COPY  requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /usr/app/
COPY  . .

CMD streamlit run main.py --server.port=5000





