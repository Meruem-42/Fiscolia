FROM node:20-alpine

WORKDIR /app

RUN apk update
RUN npx create-vite@latest . --template react
RUN npm install

EXPOSE 5173
COPY ./srcs/App.js /app/src/App.jsx

CMD ["npm", "run", "dev", "--", "--host"]