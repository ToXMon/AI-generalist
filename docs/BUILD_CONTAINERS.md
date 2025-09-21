# Manual Docker Build Commands

## Build Backend Container
```bash
cd backend
docker build --platform linux/amd64 -t generalist-backend:latest .
```

## Build Frontend Container
```bash
cd frontend
docker build --platform linux/amd64 -t generalist-frontend:latest .
```

## Tag for Registry (if using Docker Hub)
```bash
# Replace 'yourusername' with your Docker Hub username
docker tag generalist-backend:latest yourusername/generalist-backend:latest
docker tag generalist-frontend:latest yourusername/generalist-frontend:latest

# Push to registry
docker push yourusername/generalist-backend:latest
docker push yourusername/generalist-frontend:latest
```

## Update akash-deploy.yaml
After pushing images, update the image names in `akash-deploy.yaml`:
- Change `generalist-frontend:latest` to `yourusername/generalist-frontend:latest`
- Change `generalist-backend:latest` to `yourusername/generalist-backend:latest`