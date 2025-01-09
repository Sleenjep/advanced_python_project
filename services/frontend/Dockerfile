FROM node:16

RUN mkdir /app
WORKDIR /app

COPY package*.json /app/
RUN npm install

RUN mkdir -p node_modules/.cache && chmod -R 777 node_modules/.cache

COPY . /app/

EXPOSE 8080

CMD npm run serve
