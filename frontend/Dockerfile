FROM node:slim

WORKDIR /app

COPY package.json /app/package.json

COPY tsconfig.json /app/tsconfig.json

RUN npm install npm

RUN npm install 

#COPY . .
COPY public /app/public

EXPOSE 3000

CMD ["npm","start"]