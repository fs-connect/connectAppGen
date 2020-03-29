FROM hkarhani/p3nb:latest

MAINTAINER Hassan El Karhani <hkarhani@gmail.com>

WORKDIR /notebooks

ADD templates /notebooks/templates
ADD generator.py /notebooks/
ADD *.yaml /notebooks/
ADD *.ipynb /notebooks/

RUN pip3 install -r requirements.txt
RUN rm /notebooks/requirements.txt

EXPOSE 8888

CMD /bin/sh -c "/usr/bin/jupyter notebook --allow-root"
