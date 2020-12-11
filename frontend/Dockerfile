FROM node:15.3-alpine as builder
USER root
RUN mkdir /frontend
WORKDIR /frontend
ARG API_URL
ENV REACT_APP_HOST_IP_ADDRESS $API_URL
COPY ./package*.json ./
RUN yarn
COPY . /frontend
RUN chmod +x /frontend/*.sh

#RUN yarn build
#RUN yarn build