# Quick Start - AWS Deployment

## 🚀 Deploy in 5 Steps (15 minutes)

### Step 1: Install CDK CLI (2 min)

```bash
npm install -g aws-cdk
```

Verify:
```bash
cdk --version
```

### Step 2: Bootstrap CDK (2 min)

```bash
cdk bootstrap aws://891450252216/us-west-2
```

### Step 3: Install Dependencies (2 min)

```bash
cd infrastructure
pip install -r requirements.txt
```

### Step 4: Build Frontend (3 min)

```bash
cd ../frontend
npm install
npm run build
```

### Step 5: Deploy! (10 min)

```bash
cd ../infrastructure
cdk deploy --all
```

**Or use the script:**

```bash
cd infrastructure
deploy.bat  # Windows
```

---

## 📝 After Deployment

1. **Note the outputs:**
   - ApiUrl: `https://abc123.execute-api.us-west-2.amazonaws.com/prod/`
   - FrontendUrl: `https://d1234567890.cloudfront.net`

2. **Update frontend config:**
   ```bash
   # Edit frontend/.env.production
   REACT_APP_API_URL=YOUR_API_URL
   
   # Rebuild
   cd frontend
   npm run build
   
   # Redeploy
   cd ../infrastructure
   cdk deploy HealthLakeFrontendStack
   ```

3. **Test your app:**
   - Open FrontendUrl in browser
   - Test all features

---

## ✅ That's it!

Your app is now live on AWS! 🎉

**Full guide:** `AWS_DEPLOYMENT_COMPLETE.md`
