FROM node:slim

WORKDIR /app

COPY package.json /app/package.json

RUN npm install 

#COPY . .
COPY public /app/public

EXPOSE 3000

CMD ["npm","start"]