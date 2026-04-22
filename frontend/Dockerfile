FROM node:20-alpine AS build
WORKDIR /app

COPY frontend/ ./

RUN npm i -g pnpm@10.28.0

ENV CI=true

RUN pnpm install --frozen-lockfile --prod=false --force

ARG VITE_AUTH_URL
ARG VITE_BUSLINES_URL
ENV VITE_AUTH_URL=$VITE_AUTH_URL
ENV VITE_BUSLINES_URL=$VITE_BUSLINES_URL

RUN pnpm build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
