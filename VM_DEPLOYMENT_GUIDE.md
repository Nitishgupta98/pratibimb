# Windows VM Deployment Guide

## 🚀 **VM Deployment Configuration**

### **1. Environment Variables Setup**

Create a `.env` file in the UI directory (`/UI/.env`):

```bash
# For Windows VM deployment
REACT_APP_ENVIRONMENT=vm
REACT_APP_API_URL=http://YOUR_VM_IP:8000
REACT_APP_VM_DEPLOYMENT=true

# Example for internal network:
# REACT_APP_API_URL=http://192.168.1.100:8000

# Example for public VM:
# REACT_APP_API_URL=http://203.0.113.42:8000
```

### **2. API Server Configuration**

Update the FastAPI server in `main.py` to bind to all interfaces:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
```

### **3. Windows Firewall Configuration**

```powershell
# Allow FastAPI port through Windows Firewall
New-NetFirewallRule -DisplayName "FastAPI Server" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow

# Allow React dev server (if running in dev mode)
New-NetFirewallRule -DisplayName "React Dev Server" -Direction Inbound -Protocol TCP -LocalPort 3000 -Action Allow
```

### **4. Network Configuration Options**

#### **Option A: Internal Network (Recommended)**
- Use private IP address (e.g., 192.168.1.100:8000)
- Only accessible within the same network
- More secure for internal deployments

#### **Option B: Public Access**
- Use public IP address or domain
- Configure proper security measures
- Consider using HTTPS in production

### **5. Build Commands for Production**

```bash
# In the UI directory
npm run build

# Serve the built files using a web server
# Option 1: Using serve package
npx serve -s build -l 3000

# Option 2: Using IIS (Windows)
# Copy build folder contents to IIS wwwroot
```

### **6. Automatic Configuration Detection**

The app automatically detects the environment:

1. **Development**: `NODE_ENV=development` → Uses localhost:8000
2. **VM Mode**: `REACT_APP_VM_DEPLOYMENT=true` → Uses VM IP
3. **Production**: Uses environment variables or defaults

### **7. Testing VM Deployment**

```bash
# Test API connectivity from different machine
curl http://YOUR_VM_IP:8000/docs

# Test real-time logs
curl http://YOUR_VM_IP:8000/api/stream-logs/test-request-id
```

### **8. Troubleshooting**

#### **Common Issues:**

1. **CORS Errors**: Ensure CORS middleware allows your frontend domain
2. **Connection Refused**: Check Windows Firewall and port binding
3. **Network Timeout**: Verify VM network configuration
4. **Progress Not Loading**: Check streaming endpoint accessibility

#### **Debug Commands:**

```bash
# Check if ports are listening
netstat -an | findstr :8000
netstat -an | findstr :3000

# Test local API
curl http://localhost:8000/docs

# Check Windows Firewall rules
Get-NetFirewallRule -DisplayName "*FastAPI*"
```

### **9. Production Checklist**

- [ ] Environment variables configured
- [ ] Firewall rules added
- [ ] API server binds to 0.0.0.0
- [ ] Frontend built for production
- [ ] Network connectivity tested
- [ ] Real-time progress endpoints accessible
- [ ] File download endpoints working
- [ ] CORS properly configured

## 🔧 **Configuration Examples**

### **Local Development:**
```javascript
// Automatically uses: http://localhost:8000
```

### **VM Internal Network:**
```bash
# .env file
REACT_APP_API_URL=http://192.168.1.100:8000
```

### **VM Public Access:**
```bash
# .env file  
REACT_APP_API_URL=http://your-vm-domain.com:8000
```

## ✅ **Real-Time Features on VM**

All real-time features will work on VM deployment:

1. **Progress Tracking**: Polls every 1 second
2. **Log Streaming**: Real-time step updates
3. **File Downloads**: Direct file access
4. **Error Recovery**: Network retry logic included

The system is designed to be VM-ready with proper network configuration!
