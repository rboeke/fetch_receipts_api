FROM python:3.13
RUN python -m pip install --upgrade pip
WORKDIR /
COPY requirements.txt requirements.txt
COPY ./api/ /
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]