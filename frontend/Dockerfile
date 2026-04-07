FROM node:20-alpine

WORKDIR /app

RUN apk update
RUN npx create-vite@latest . --template react
RUN npm install
RUN npm install react-router-dom

EXPOSE 5173

COPY ./vite.config.js /app/vite.config.js

CMD ["npm", "run", "dev", "--", "--host"]