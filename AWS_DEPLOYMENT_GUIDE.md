# AWS Deployment Guide - Quick Setup

## 🚀 Deployment Strategy

**Frontend**: AWS Amplify (easiest, auto-deploy from Git)
**Backend**: AWS EC2 (simple, reliable)

---

## Part 1: Deploy Backend to EC2

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. **Name**: `healthlake-backend`
3. **AMI**: Ubuntu Server 22.04 LTS
4. **Instance Type**: t3.medium (2 vCPU, 4GB RAM)
5. **Key Pair**: Create new or use existing
6. **Security Group**: Create new with rules:
   - SSH (22) - Your IP
   - HTTP (80) - Anywhere
   - Custom TCP (8000) - Anywhere
7. **Storage**: 20 GB
8. Click "Launch Instance"

### Step 2: Connect to EC2

```bash
# Windows (use Git Bash or WSL)
ssh -i "your-key.pem" ubuntu@your-ec2-public-ip

# Example:
ssh -i "healthlake-key.pem" ubuntu@54.123.45.67
```

### Step 3: Install Dependencies on EC2

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.12
sudo apt install python3.12 python3.12-venv python3-pip -y

# Install Git
sudo apt install git -y

# Install Docker (optional, for easier deployment)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
```

### Step 4: Clone Repository

```bash
# Clone your repo (or upload files)
git clone https://github.com/harshavadlamudi/HASH5_hackathon.git
cd HASH5_hackathon/backend

# OR upload via SCP
# scp -i "your-key.pem" -r backend ubuntu@your-ec2-ip:~/
```

### Step 5: Setup Backend

```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
```

**Add to .env:**
```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_SESSION_TOKEN=your_token
AWS_REGION=us-west-2
```

### Step 6: Run Backend with PM2 (keeps it running)

```bash
# Install PM2
sudo npm install -g pm2

# Start backend
pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name healthlake-backend

# Save PM2 config
pm2 save
pm2 startup

# Check status
pm2 status
pm2 logs healthlake-backend
```

### Step 7: Test Backend

```bash
# From EC2
curl http://localhost:8000/health

# From your computer
curl http://your-ec2-public-ip:8000/health
```

**Backend URL**: `http://your-ec2-public-ip:8000`

---

## Part 2: Deploy Frontend to AWS Amplify

### Step 1: Push Code to GitHub

```bash
# In your project root
git add .
git commit -m "Ready for AWS deployment"
git push origin main
```

### Step 2: Deploy with AWS Amplify

1. Go to AWS Console → AWS Amplify
2. Click "New app" → "Host web app"
3. Select "GitHub" (or your Git provider)
4. Authorize AWS Amplify to access your repo
5. Select repository: `HASH5_hackathon`
6. Select branch: `main`
7. **Build settings**:
   - App root directory: `frontend`
   - Build command: `npm run build`
   - Output directory: `build`
8. **Environment variables**:
   - Key: `REACT_APP_API_URL`
   - Value: `http://your-ec2-public-ip:8000`
9. Click "Save and deploy"

### Step 3: Wait for Deployment

- Amplify will build and deploy (5-10 minutes)
- You'll get a URL like: `https://main.d1234abcd.amplifyapp.com`

### Step 4: Update Backend CORS

```bash
# SSH to EC2
ssh -i "your-key.pem" ubuntu@your-ec2-ip

# Edit main.py
cd HASH5_hackathon/backend
nano app/main.py
```

**Update CORS origins:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://main.d1234abcd.amplifyapp.com"  # Add your Amplify URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Restart backend:**
```bash
pm2 restart healthlake-backend
```

---

## Part 3: Test Production Deployment

1. Open your Amplify URL: `https://main.d1234abcd.amplifyapp.com`
2. Test all 5 critical tests again
3. Verify backend API calls work

---

## 🔧 Troubleshooting

### Backend not accessible
```bash
# Check if running
pm2 status

# Check logs
pm2 logs healthlake-backend

# Restart
pm2 restart healthlake-backend
```

### Frontend can't reach backend
- Check EC2 security group allows port 8000
- Check CORS settings in backend
- Check REACT_APP_API_URL in Amplify environment variables

### AWS credentials expired
```bash
# SSH to EC2
cd HASH5_hackathon/backend
nano .env
# Update credentials
pm2 restart healthlake-backend
```

---

## 💰 Cost Estimate

- **EC2 t3.medium**: ~$30/month
- **AWS Amplify**: ~$0 (free tier covers it)
- **Data transfer**: ~$5/month
- **Total**: ~$35/month

---

## 🎯 Quick Commands Reference

**EC2 Backend:**
```bash
# SSH
ssh -i "key.pem" ubuntu@ec2-ip

# Check status
pm2 status

# View logs
pm2 logs healthlake-backend

# Restart
pm2 restart healthlake-backend

# Stop
pm2 stop healthlake-backend
```

**Amplify Frontend:**
- Auto-deploys on Git push
- View logs in Amplify Console
- Redeploy: Amplify Console → Redeploy this version

---

## ✅ Deployment Checklist

- [ ] EC2 instance launched
- [ ] Backend running on EC2
- [ ] Backend accessible at http://ec2-ip:8000/health
- [ ] Code pushed to GitHub
- [ ] Amplify app created
- [ ] Frontend deployed to Amplify
- [ ] CORS updated with Amplify URL
- [ ] Production app tested

---

## 🚀 You're Live!

**Frontend**: https://your-app.amplifyapp.com
**Backend**: http://your-ec2-ip:8000
**API Docs**: http://your-ec2-ip:8000/docs
