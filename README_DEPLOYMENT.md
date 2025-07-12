# 🌟 PRATIBIMB - Windows VM Deployment Guide

**True Reflection of Digital World**

Complete one-click deployment solution for Windows Virtual Machines.

## 🚀 Quick Start

### **📋 Prerequisites**
- Windows 10/11 or Windows Server
- Python 3.8+ installed and in PATH
- Node.js 16+ installed and in PATH
- Administrator privileges (recommended)

### **⚡ One-Click Deployment**

1. **Copy the entire project folder to your VM**
2. **Right-click `deploy_vm.bat` → "Run as Administrator"**
3. **Follow the prompts**
4. **Access your application!**

```bash
# The script will automatically:
✅ Detect your VM IP address
✅ Configure Windows Firewall
✅ Setup Python virtual environment
✅ Install all dependencies
✅ Build the React UI
✅ Create service scripts
✅ Test the deployment
```

## 📁 Project Structure

```
pratibimb-main/
├── 📜 deploy_vm.bat          # Main deployment script
├── 📜 check_status.bat       # Check deployment status
├── 📜 troubleshoot.bat       # Fix common issues
├── 📜 start_all_services.bat # Start both API and UI
├── 📜 stop_all_services.bat  # Stop all services
├── 📁 API/                   # Python FastAPI backend
│   ├── main.py              # Main API server
│   ├── pratibimb.py         # Braille conversion engine
│   ├── requirements.txt     # Python dependencies
│   └── venv/                # Virtual environment (created)
└── 📁 UI/                    # React frontend
    ├── src/                 # Source code
    ├── build/               # Production build (created)
    ├── .env                 # Environment config (created)
    └── package.json         # Node.js dependencies
```

## 🎯 Available Scripts

### **🚀 Deployment & Management**
- `deploy_vm.bat` - Complete deployment setup
- `start_all_services.bat` - Start both API and UI servers
- `stop_all_services.bat` - Stop all running services
- `check_status.bat` - Check deployment status
- `troubleshoot.bat` - Fix common issues

### **🔧 Individual Services**
- `start_api.bat` - Start only the API server
- `start_ui.bat` - Start UI in development mode
- `start_ui_production.bat` - Start UI in production mode

## 🌐 Default URLs

After deployment, access your application at:

- **🎨 User Interface:** `http://YOUR_VM_IP:3000`
- **⚡ API Server:** `http://YOUR_VM_IP:8000`
- **📖 API Documentation:** `http://YOUR_VM_IP:8000/docs`

## 🔧 Configuration

### **Environment Variables**
The deployment script creates a `.env` file in the UI directory:

```bash
REACT_APP_ENVIRONMENT=vm
REACT_APP_API_URL=http://YOUR_VM_IP:8000
REACT_APP_VM_DEPLOYMENT=true
GENERATE_SOURCEMAP=false
```

### **Network Configuration**
- **API Port:** 8000
- **UI Port:** 3000
- **Firewall:** Automatically configured
- **IP Detection:** Automatic with manual override option

## 🛠️ Troubleshooting

### **Common Issues & Solutions**

#### **🔥 Firewall Issues**
```bash
# Run troubleshoot.bat and select option 1
# Or manually:
netsh advfirewall firewall add rule name="Pratibimb API Server" dir=in action=allow protocol=TCP localport=8000
```

#### **🐍 Python Environment Issues**
```bash
# Run troubleshoot.bat and select option 2
# Or manually rebuild:
cd API
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### **⚛️ UI Build Issues**
```bash
# Run troubleshoot.bat and select option 3
# Or manually rebuild:
cd UI
rmdir /s /q build node_modules
npm install
npm run build
```

#### **🌐 Network Connectivity**
```bash
# Check if services are running:
netstat -an | findstr ":8000"
netstat -an | findstr ":3000"

# Test API:
curl http://localhost:8000/docs
```

### **🔍 Quick Status Check**
Run `check_status.bat` to verify:
- ✅ All files are in place
- ✅ Services are running
- ✅ Firewall rules are active
- ✅ Network connectivity

## 📊 Features

### **🎯 Core Functionality**
- **YouTube Transcript Extraction**
- **AI-Enhanced Content for Accessibility**
- **Grade 1 Braille Conversion**
- **Embosser-Ready BRF Files**
- **Real-Time Progress Tracking**

### **📱 User Interface**
- **Modern React UI**
- **Real-Time Progress Display**
- **File Download Management**
- **Responsive Design**
- **Error Handling & Recovery**

### **⚡ API Features**
- **RESTful API with FastAPI**
- **Request-Specific Logging**
- **File Streaming & Downloads**
- **Comprehensive Error Handling**
- **Auto-Generated Documentation**

### **🔄 Real-Time Features**
- **Live Progress Updates**
- **Step-by-Step Processing**
- **Request Tracking**
- **Log Streaming**
- **Error Notifications**

## 🔐 Security Considerations

### **🛡️ Network Security**
- **Firewall Rules:** Automatically configured for required ports
- **Internal Access:** Recommend using private IP addresses
- **External Access:** Configure router/firewall for public access

### **📁 File Permissions**
- **Write Access:** Required for log files and outputs
- **Service Account:** Consider running services under dedicated account
- **Antivirus:** Exclude project directory if needed

## 🚀 Performance Optimization

### **💻 System Requirements**
- **RAM:** 4GB minimum, 8GB recommended
- **CPU:** 2+ cores recommended
- **Storage:** 2GB free space minimum
- **Network:** Stable internet for YouTube access

### **⚡ Performance Tips**
- **Use Production Build:** `start_ui_production.bat`
- **Monitor Resources:** Check Task Manager during processing
- **Log Rotation:** Clear old logs periodically
- **Cache Management:** Use troubleshoot.bat option 6

## 📞 Support & Maintenance

### **🔄 Regular Maintenance**
```bash
# Weekly tasks:
1. Run check_status.bat
2. Clear old log files
3. Update dependencies if needed
4. Test functionality with sample YouTube URL
```

### **🆙 Updates**
```bash
# To update the application:
1. Stop all services: stop_all_services.bat
2. Replace source files
3. Run: deploy_vm.bat
4. Test deployment: check_status.bat
```

### **📋 Monitoring**
- **Service Status:** Use check_status.bat
- **Error Logs:** Check API/logs/ directory
- **Performance:** Monitor CPU/RAM usage
- **Network:** Verify external accessibility

## 🎉 Success Indicators

After deployment, you should see:
- ✅ Both services running without errors
- ✅ UI accessible via browser
- ✅ API documentation loading
- ✅ Real-time progress working
- ✅ File downloads functioning
- ✅ Braille conversion completing

## 📝 Logging

### **📄 Log Files**
- **Main API Log:** `API/logs/pratibimb.log`
- **Request Logs:** `API/logs/requests/request_*.log`
- **Service Logs:** Individual service windows

### **🔍 Log Monitoring**
- **Real-Time:** View service windows
- **Historical:** Check log files
- **Debugging:** Use troubleshoot.bat option 8

---

## 🌟 **Ready to Deploy?**

1. **Copy this folder to your Windows VM**
2. **Right-click `deploy_vm.bat` → Run as Administrator**
3. **Follow the prompts**
4. **Start using Pratibimb!**

**Need help?** Run `troubleshoot.bat` for automated problem resolution.

---

**🔤 Pratibimb - Making Digital Content Accessible Through Braille**
