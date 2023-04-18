FROM nginx:stable-alpine3.17-slim

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/nginx/nginx-default.conf /etc/nginx/nginx.conf
COPY ./docker/nginx/nginx.conf /etc/nginx/conf.d
