FROM python:3

RUN apt-get -y update
RUN pip install --upgrade pip
RUN apt-get install zip -y
RUN apt-get install unzip -y

# Install chromedriver
RUN wget -N https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.92/linux64/chromedriver-linux64.zip -P ~/
RUN unzip ~/chromedriver-linux64.zip -d ~/
RUN rm ~/chromedriver-linux64.zip
RUN mv -f ~/chromedriver-linux64/chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

# Install chrome broswer
# ????
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable

WORKDIR /usr/src/app

COPY . .

RUN apt update
RUN apt install libsystemd-dev
RUN pip install --no-cache-dir -r requirements.txt


CMD [ "python", "./main.py" ]