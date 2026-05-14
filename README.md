# Jenkins CI/CD Pipeline with Docker

A complete CI/CD pipeline project using **Jenkins**, **Docker**, and **GitHub** running on an AWS EC2 instance.

## 🏗️ Architecture

```
GitHub (Source Code) → Jenkins (CI/CD) → Docker (Containerization) → EC2 (Deployment)
```

## 📁 Project Structure

```
jenkins-pipeline/
├── app.py              # Flask web application
├── test_app.py         # Unit tests (pytest)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker container configuration
├── docker-compose.yml  # Docker Compose for local development
├── Jenkinsfile         # Jenkins pipeline definition
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🚀 Pipeline Stages

| Stage | Description |
|-------|-------------|
| **Checkout** | Pulls latest code from GitHub |
| **Build Docker Image** | Builds the Docker image from Dockerfile |
| **Run Tests** | Executes pytest unit tests inside container |
| **Deploy** | Stops old container, runs new one on port 5000 |
| **Health Check** | Verifies the app is running and healthy |

## 🛠️ Tech Stack

- **Application**: Python 3.11 + Flask
- **Testing**: Pytest
- **Containerization**: Docker
- **CI/CD**: Jenkins
- **Infrastructure**: AWS EC2 (t3.large)
- **Source Control**: GitHub

## 📋 Prerequisites

On your EC2 instance, ensure you have:
- Jenkins installed and running
- Docker installed (`sudo apt install docker.io` or `sudo yum install docker`)
- Jenkins user added to Docker group (`sudo usermod -aG docker jenkins`)
- Jenkins restarted after Docker group change (`sudo systemctl restart jenkins`)

## 🔧 Setup Instructions

### 1. EC2 Instance Setup (if not already done)

```bash
# Install Docker
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Add Jenkins user to Docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### 2. Jenkins Configuration

1. Go to Jenkins: `http://<your-ec2-ip>:8080`
2. Create a new **Pipeline** job
3. Under **Pipeline**, select "Pipeline script from SCM"
4. Set SCM to **Git**
5. Repository URL: `https://github.com/alandkhalil01/jenkins-pipeline.git`
6. Branch: `*/main`
7. Script Path: `Jenkinsfile`
8. Save and click **Build Now**

### 3. Access the Application

Once deployed, access your app at:
```
http://<your-ec2-public-ip>:5000
```

## 🧪 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home - returns welcome message |
| `/health` | GET | Health check endpoint |
| `/info` | GET | Application information |

## 🏃 Running Locally

```bash
# With Docker
docker build -t jenkins-pipeline-app .
docker run -p 5000:5000 jenkins-pipeline-app

# Or with Docker Compose
docker-compose up --build

# Or without Docker
pip install -r requirements.txt
python app.py
```

## 🧪 Running Tests Locally

```bash
pip install -r requirements.txt
pytest test_app.py -v
```

## 👤 Author

**Aland Khalil**

## 📄 EC2 Instance Details

- Instance: `jenkins-worker`
- Type: t3.large
- Public IP: Check AWS Console
- Jenkins: `http://<public-ip>:8080`
- App: `http://<public-ip>:5000`