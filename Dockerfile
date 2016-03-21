FROM python:2.7
RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/recipy/recipy.git
WORKDIR recipy
RUN pip install -r requirements.txt
RUN python setup.py install
RUN pip install numpy
RUN pip install pandas
RUN pip install matplotlib
ADD . /
