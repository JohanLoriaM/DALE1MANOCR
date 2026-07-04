FROM node:20-slim

WORKDIR /app

# Instalar dependencias de Nuxt
COPY package*.json ./
RUN npm install

# Copiar el resto del código del frontend
COPY . .

EXPOSE 3000

# Iniciar el servidor de desarrollo de Nuxt enlazando a todas las interfaces de red (--host)
CMD ["npm", "run", "dev", "--", "--host"]
