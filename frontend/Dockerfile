FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx-headers.inc /etc/nginx/av-headers.inc
COPY . /usr/share/nginx/html
EXPOSE 80
