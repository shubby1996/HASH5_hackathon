# Deployment Guide

## 🐳 Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose installed
- AWS credentials configured in `.env` file

### Quick Start

1. **Ensure `.env` file exists in project root:**
```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_SESSION_TOKEN=your_token
AWS_REGION=us-west-2
```

2. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

3. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Individual Container Commands

**Backend only:**
```bash
cd backend
docker build -t healthlake-backend .
docker run -p 8000:8000 --env-file ../.env healthlake-backend
```

**Frontend only:**
```bash
cd frontend
docker build -t healthlake-frontend .
docker run -p 3000:3000 healthlake-frontend
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

## 🚀 Production Deployment

### Environment Variables
Create `.env.production` with:
```bash
AWS_ACCESS_KEY_ID=prod_key
AWS_SECRET_ACCESS_KEY=prod_secret
AWS_SESSION_TOKEN=prod_token
AWS_REGION=us-west-2
REACT_APP_API_URL=https://your-api-domain.com
```

### Build for Production

**Backend:**
```bash
cd backend
docker build -t healthlake-backend:prod .
```

**Frontend:**
```bash
cd frontend
npm run build
docker build -t healthlake-frontend:prod -f Dockerfile.prod .
```

### Deploy to AWS

**Option 1: AWS ECS**
1. Push images to ECR
2. Create ECS task definitions
3. Deploy to ECS cluster

**Option 2: AWS EC2**
1. Launch EC2 instance
2. Install Docker
3. Pull and run containers

**Option 3: AWS Elastic Beanstalk**
1. Create application
2. Upload docker-compose.yml
3. Deploy

## 🔧 Troubleshooting

**Port conflicts:**
```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Backend
  - "3001:3000"  # Frontend
```

**AWS credentials not working:**
- Verify `.env` file is in project root
- Check credentials are not expired
- Ensure proper IAM permissions

**Container won't start:**
```bash
docker-compose logs backend
docker-compose logs frontend
```

## 📊 Health Checks

**Backend health:**
```bash
curl http://localhost:8000/health
```

**Frontend:**
Open http://localhost:3000 in browser

## 🔐 Security Notes

- Never commit `.env` files
- Use AWS Secrets Manager for production
- Enable HTTPS in production
- Set up proper CORS policies
- Use IAM roles instead of access keys when possible
