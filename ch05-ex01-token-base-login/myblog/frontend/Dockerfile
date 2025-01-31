FROM node:23.1-alpine

WORKDIR /app/frontend

COPY package*.json ./

RUN npm install

COPY . /app/frontend
