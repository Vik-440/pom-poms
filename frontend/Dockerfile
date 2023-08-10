FROM node:16 AS build

RUN mkdir -p /app
WORKDIR /app
COPY package.json /app
RUN npm install
COPY . /app
RUN npm run build
FROM nginx:1.20.1
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build app/dist/pompons /usr/share/nginx/html
EXPOSE 4200:80