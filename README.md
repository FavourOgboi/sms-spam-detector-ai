# SMS Guard - AI-Powered SMS Spam Detection System

<div align="center">
  <img src="public/pres.jpg" alt="SMS Guard Logo" width="120" height="120" style="border-radius: 50%;">
  
  <h3>🛡️ Advanced Machine Learning SMS Spam Detection</h3>
  
  [![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-5.5.3-blue.svg)](https://www.typescriptlang.org/)
  [![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4.1-38B2AC.svg)](https://tailwindcss.com/)
  [![Vite](https://img.shields.io/badge/Vite-5.4.2-646CFF.svg)](https://vitejs.dev/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [File Structure](#file-structure)
- [Getting Started](#getting-started)
- [VS Code Setup](#vs-code-setup)
- [Backend Integration Guide](#backend-integration-guide)
- [API Documentation](#api-documentation)
- [Technology Stack](#technology-stack)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🎯 Overview

SMS Guard is a production-ready, AI-powered SMS spam detection system built with modern web technologies. It provides real-time analysis of SMS messages using advanced machine learning algorithms, helping users identify and protect themselves from spam messages.

**Created by:** Ogboi Favour Ifeanyichukwu  
**Institution:** Federal University of Petroleum Resources Effurun  
**Field:** Computer Science Graduate & AI Developer  
**Location:** Lagos, Nigeria

## ✨ Features

### 🔐 **User Authentication & Security**
- Secure login/registration system
- JWT token-based authentication
- Protected routes and data isolation
- Password change functionality
- Account deletion with confirmation

### 🤖 **AI-Powered Spam Detection**
- Real-time SMS message analysis
- Confidence scoring (0-100%)
- Advanced machine learning algorithms
- Animated guard protection visualization
- Sample messages for testing

### 📊 **Personal Dashboard**
- Comprehensive statistics overview
- Interactive charts (pie and bar charts)
- Recent predictions history
- Personal insights and analytics
- Empty state handling for new users

### 📱 **Message History Management**
- Complete prediction history
- Search functionality across messages
- Filter by spam/ham categories
- Export data to CSV
- Detailed confidence visualization

### 🎨 **Modern UI/UX**
- Dark/Light theme toggle with system preference detection
- Responsive design for all devices
- Smooth animations with Framer Motion
- Professional design with micro-interactions
- Accessibility-first approach

### 👤 **Profile Management**
- Editable user information
- Profile image upload
- Theme preferences
- Member since tracking
- Bio and contact information

## 📸 Screenshots

### 🏠 Dashboard Overview
![Dashboard](docs/screenshots/dashboard.png)
*Comprehensive analytics dashboard with charts and recent activity*

### 🔍 Spam Detection Interface
![Prediction](docs/screenshots/prediction.png)
*Real-time spam detection with confidence scoring and animated guard*

### 📊 Message History
![History](docs/screenshots/history.png)
*Searchable and filterable message history with export functionality*

### 👤 User Profile
![Profile](docs/screenshots/profile.png)
*Complete profile management with theme toggle and settings*

### 🌙 Dark Mode
![Dark Mode](docs/screenshots/dark-mode.png)
*Beautiful dark mode with proper contrast and accessibility*

### 📱 Mobile Responsive
![Mobile](docs/screenshots/mobile.png)
*Fully responsive design optimized for mobile devices*

## 📁 File Structure

```
sms-guard-frontend/
├── 📁 public/
│   ├── 🖼️ pres.jpg                    # Profile image
│   └── 🌐 vite.svg                    # Vite logo
├── 📁 src/
│   ├── 📁 components/                 # Reusable UI components
│   │   ├── 📁 layout/                # Layout components
│   │   │   ├── 🧩 Layout.tsx         # Main layout wrapper
│   │   │   └── 🧭 Navigation.tsx     # Sidebar navigation
│   │   ├── 📁 ui/                    # Basic UI components
│   │   │   ├── 🛡️ GuardAnimation.tsx # Animated guard for predictions
│   │   │   ├── ⏳ LoadingSpinner.tsx # Loading spinner component
│   │   │   └── 🪟 Modal.tsx          # Modal dialog component
│   │   └── 🔒 ProtectedRoute.tsx     # Route protection wrapper
│   ├── 📁 contexts/                  # React contexts
│   │   ├── 🔐 AuthContext.tsx        # Authentication state management
│   │   └── 🎨 ThemeContext.tsx       # Theme management (light/dark)
│   ├── 📁 pages/                     # Page components
│   │   ├── 📊 Dashboard.tsx          # Main dashboard with analytics
│   │   ├── 🔍 Predict.tsx            # Message prediction interface
│   │   ├── 📜 History.tsx            # Message history with search
│   │   ├── 📚 Explanation.tsx        # How the AI model works
│   │   ├── 👤 Profile.tsx            # User profile management
│   │   ├── 📞 Contact.tsx            # Contact information
│   │   ├── 🔑 Login.tsx              # Login page
│   │   └── 📝 Register.tsx           # Registration page
│   ├── 📁 services/                  # API service layer
│   │   └── 🌐 api.ts                 # HTTP requests and mock data
│   ├── 📁 types/                     # TypeScript definitions
│   │   └── 📋 index.ts               # Shared interfaces and types
│   ├── 🎯 App.tsx                    # Main app component
│   ├── 🎨 index.css                  # Global styles (Tailwind)
│   ├── 🚀 main.tsx                   # Application entry point
│   └── 🔧 vite-env.d.ts             # Vite environment types
├── 📁 docs/                          # Documentation
│   └── 📁 screenshots/               # Application screenshots
├── ⚙️ eslint.config.js               # ESLint configuration
├── 🌐 index.html                     # HTML template
├── 📦 package.json                   # Dependencies and scripts
├── 🎨 postcss.config.js              # PostCSS configuration
├── 📖 README.md                      # This file
├── 🎨 tailwind.config.js             # Tailwind CSS configuration
├── 🔧 tsconfig.app.json              # TypeScript app configuration
├── 🔧 tsconfig.json                  # TypeScript root configuration
├── 🔧 tsconfig.node.json             # TypeScript Node configuration
└── ⚡ vite.config.ts                 # Vite configuration
```

### 📂 Key Directories Explained

- **`src/components/`** - Reusable UI components organized by category
- **`src/contexts/`** - React Context providers for global state
- **`src/pages/`** - Main application pages and routes
- **`src/services/`** - API integration and data fetching logic
- **`src/types/`** - TypeScript type definitions and interfaces

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16.0.0 or higher) - [Download here](https://nodejs.org/)
- **npm** (v7.0.0 or higher) - Comes with Node.js
- **Git** - [Download here](https://git-scm.com/)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/sms-guard-frontend.git
   cd sms-guard-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file:
   ```env
   VITE_API_BASE_URL=http://localhost:5000/api
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Navigate to `http://localhost:5173`

### 🎮 Demo Credentials

The application includes a demo system for testing:
- **Username:** `demo` or **Email:** `demo@example.com`
- **Password:** `demo123`

## 💻 VS Code Setup

### Recommended Extensions

Install these VS Code extensions for the best development experience:

```json
{
  "recommendations": [
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-vscode.vscode-typescript-next",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense",
    "ms-vscode.vscode-json"
  ]
}
```

### VS Code Settings

Create `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "emmet.includeLanguages": {
    "typescript": "html",
    "typescriptreact": "html"
  },
  "tailwindCSS.includeLanguages": {
    "typescript": "html",
    "typescriptreact": "html"
  }
}
```

### Launch Configuration

Create `.vscode/launch.json` for debugging:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch Chrome",
      "request": "launch",
      "type": "chrome",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/src"
    }
  ]
}
```

### Tasks Configuration

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "npm",
      "script": "dev",
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "label": "npm: dev",
      "detail": "vite"
    },
    {
      "type": "npm",
      "script": "build",
      "group": "build",
      "label": "npm: build",
      "detail": "vite build"
    }
  ]
}
```

## 🔧 Backend Integration Guide

### For Gemini AI Assistant

This frontend is designed to work with a Flask backend. Here's what you need to implement:

#### 🗄️ Database Schema

```sql
-- Users table
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile_image VARCHAR(500),
    bio TEXT,
    member_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    theme VARCHAR(10) DEFAULT 'light',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Predictions table
CREATE TABLE predictions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    prediction VARCHAR(10) NOT NULL, -- 'spam' or 'ham'
    confidence DECIMAL(5,4) NOT NULL, -- 0.0000 to 1.0000
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_time_ms INTEGER,
    model_version VARCHAR(50)
);
```

#### 🌐 Required API Endpoints

```python
# Authentication
POST /api/auth/login
POST /api/auth/register
POST /api/auth/logout
GET /api/auth/me

# Predictions
POST /api/predict

# User Data
GET /api/user/stats
GET /api/user/predictions
PUT /api/user/profile
PUT /api/user/change-password
DELETE /api/user/delete
```

#### 📊 Data Models (TypeScript → Python)

```python
# User model
class User:
    id: str
    username: str
    email: str
    profile_image: Optional[str]
    bio: Optional[str]
    member_since: str  # ISO date string
    theme: str = 'light'

# Prediction model
class PredictionResult:
    id: str
    message: str
    prediction: str  # 'spam' or 'ham'
    confidence: float  # 0.0 to 1.0
    timestamp: str  # ISO date string
    user_id: str

# User statistics
class UserStats:
    total_messages: int
    spam_count: int
    ham_count: int
    accuracy: float
    spam_rate: float
    avg_confidence: float
    recent_predictions: List[PredictionResult]
```

## 📚 API Documentation

### Authentication Flow

1. **Login/Register** → Receive JWT token
2. **Store token** in localStorage
3. **Include token** in Authorization header: `Bearer <token>`
4. **Validate token** on protected routes

### Response Format

All API responses follow this format:

```json
{
  "success": boolean,
  "data": any,
  "error": string
}
```

### Error Handling

The frontend expects specific error formats for proper user feedback.

## 🛠️ Technology Stack

### Frontend Technologies

- **⚛️ React 18.3.1** - Modern React with hooks and concurrent features
- **📘 TypeScript 5.5.3** - Type-safe JavaScript development
- **⚡ Vite 5.4.2** - Fast build tool and development server
- **🎨 Tailwind CSS 3.4.1** - Utility-first CSS framework
- **🎭 Framer Motion 11.3.0** - Smooth animations and transitions
- **📊 Recharts 2.12.7** - Beautiful charts and data visualization
- **🧭 React Router DOM 6.26.0** - Client-side routing
- **🌐 Axios 1.7.2** - HTTP client for API requests
- **🎯 Lucide React 0.344.0** - Beautiful icon library

### Development Tools

- **📏 ESLint** - Code linting and quality
- **🎨 Prettier** - Code formatting
- **🔧 PostCSS** - CSS processing
- **📦 npm** - Package management

### Recommended Backend Stack

- **🐍 Flask** - Python web framework
- **🗄️ PostgreSQL** - Database
- **🔐 JWT** - Authentication tokens
- **🤖 scikit-learn** - Machine learning
- **📁 Flask-WTF** - File uploads
- **🌐 Flask-CORS** - Cross-origin requests

## 📝 Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint

# VS Code Integration
code .               # Open project in VS Code
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow TypeScript best practices
- Use Tailwind CSS for styling
- Write meaningful commit messages
- Add proper error handling
- Test on multiple devices
- Maintain accessibility standards

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Ogboi Favour Ifeanyichukwu**  
Computer Science Graduate & AI Developer  
Federal University of Petroleum Resources Effurun

- 📧 **Email:** [ogboifavourifeanyichukwu@gmail.com](mailto:ogboifavourifeanyichukwu@gmail.com)
- 💼 **LinkedIn:** [Vincent Favour](https://linkedin.com/in/vincent-favour-297433205/)
- 🐦 **X (Twitter):** [@OgboiFavour](https://twitter.com/OgboiFavour)
- 📍 **Location:** Lagos, Nigeria

### Quick Contact

- 💼 **For Job Opportunities:** [Email Me](mailto:ogboifavourifeanyichukwu@gmail.com?subject=Job%20Opportunity%20-%20SMS%20Guard%20Developer)
- 🤝 **For Collaboration:** [Email Me](mailto:ogboifavourifeanyichukwu@gmail.com?subject=Collaboration%20Inquiry%20-%20SMS%20Guard)

---

<div align="center">
  <p>Built with ❤️ by Ogboi Favour Ifeanyichukwu</p>
  <p>🛡️ Protecting users from SMS spam with AI technology</p>
</div>