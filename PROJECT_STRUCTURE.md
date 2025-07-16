# 📁 SMS Guard - Project Structure

## 🗂️ Organized Directory Layout

```
sms-spam-detector-ai/
├── 📂 src/                     # Frontend React Application
│   ├── components/             # Reusable UI components
│   ├── contexts/              # React contexts (Auth, etc.)
│   ├── pages/                 # Page components
│   ├── services/              # API services
│   └── types/                 # TypeScript type definitions
│
├── 📂 backend/                 # Flask Backend Application
│   ├── routes/                # API route handlers
│   ├── ml_model/              # Machine learning model
│   ├── uploads/               # User uploaded files
│   ├── app.py                 # Main Flask application
│   ├── models.py              # Database models
│   └── requirements.txt       # Python dependencies
│
├── 📂 documentation/           # Project Documentation
│   ├── COMPLETE_FEATURES_GUIDE.md
│   ├── LOGIN_FIX_GUIDE.md
│   ├── NEW_USER_SETUP.md
│   ├── STARTUP_GUIDE.md
│   └── USER_MANAGEMENT_COMPLETE.md
│
├── 📂 docs/                    # Additional Documentation
│   ├── BACKEND_GUIDE.md
│   └── screenshots/
│
├── 📂 scripts/                 # Utility Scripts
│   ├── setup/                 # Setup and installation scripts
│   └── tests/                 # Test scripts
│
├── 📂 temp_files/              # Temporary Files
│   ├── smsguard.db            # Development database
│   └── smsguard_working.db    # Backup database
│
├── 📂 ml_notebooks/            # Jupyter Notebooks
│   ├── SMS_Spam_Detection_Model_Training.ipynb
│   ├── SMS_Spam_Model_Demo.ipynb
│   └── create_spam_model.py
│
├── 📂 models/                  # Pre-trained ML Models
│   ├── model_metadata.json
│   ├── spam_model_logistic_regression.joblib
│   └── tfidf_vectorizer.joblib
│
├── 📂 public/                  # Static Assets
│   └── pres.jpg
│
├── 📂 uploads/                 # User Uploads
│   └── profile_images/
│
├── 📂 instance/                # Flask Instance Folder
│   └── smsguard.db            # Production database
│
├── 📂 node_modules/            # Node.js Dependencies
│
├── 📄 README.md                # Main project documentation
├── 📄 package.json             # Node.js dependencies
├── 📄 vite.config.ts           # Vite configuration
├── 📄 tailwind.config.js       # Tailwind CSS configuration
├── 📄 tsconfig.json            # TypeScript configuration
└── 📄 index.html               # Main HTML file
```

## 🚀 Key Benefits of This Structure

### ✅ **Clean Root Directory**
- Only essential configuration files in root
- No clutter from test files or temporary scripts

### ✅ **Logical Organization**
- **Frontend code** in `/src/`
- **Backend code** in `/backend/`
- **Documentation** in `/documentation/` and `/docs/`
- **Scripts** in `/scripts/`
- **Temporary files** in `/temp_files/`

### ✅ **Preserved Functionality**
- All import paths remain unchanged
- App continues to work without modifications
- Development and production builds unaffected

## 🔧 Development Workflow

### **Frontend Development**
```bash
npm run dev          # Start development server
npm run build        # Build for production
```

### **Backend Development**
```bash
cd backend
python run.py        # Start Flask server
```

### **Full Stack Development**
```bash
npm run dev          # Terminal 1: Frontend
cd backend && python run.py  # Terminal 2: Backend
```

## 📝 File Locations

| File Type | Location | Purpose |
|-----------|----------|---------|
| React Components | `/src/components/` | Reusable UI components |
| API Routes | `/backend/routes/` | Flask API endpoints |
| Documentation | `/documentation/` | Project guides and docs |
| Test Scripts | `/scripts/tests/` | Testing utilities |
| Setup Scripts | `/scripts/setup/` | Installation helpers |
| ML Models | `/models/` | Trained models |
| User Uploads | `/uploads/` | Profile images, etc. |
| Databases | `/temp_files/`, `/instance/` | SQLite databases |

## 🎯 Next Steps

1. **Continue development** - All functionality preserved
2. **Add new features** - Follow the organized structure
3. **Documentation** - Update guides in `/documentation/`
4. **Testing** - Use scripts in `/scripts/tests/`
5. **Deployment** - Use scripts in `/scripts/setup/`

---

*This structure maintains full app functionality while providing a clean, professional organization.*
