 # Use official Node image
FROM node:20

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

# Serve with simple http server
RUN npm install -g serve

CMD ["serve", "-s", "dist", "-l", "3000"]
