# 🚀 ReLaunchAI - Career Reintegration Assistant

An AI-powered assistant designed to help women confidently return to the workforce after career breaks. Built with **SambaNova AI** for fast, efficient inference.

![ReLaunchAI](https://img.shields.io/badge/Powered%20by-SambaNova-6366f1)
![Python](https://img.shields.io/badge/Python-3.9+-3776ab)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30-ff4b4b)

## ✨ Features

- **📊 Skill Gap Analysis** - Identify transferable skills and development priorities
- **📝 Resume Summary Generator** - Create compelling professional summaries
- **🎯 Interview Coach** - Confident answers for explaining career breaks
- **📅 30-Day Roadmap** - Structured daily action plan for your comeback
- **🏢 Returnship Programs** - Discover relevant return-to-work programs

## 🎨 UI Features

- 🌟 **Premium animated hero section**
- ✨ **Glass morphism cards with hover effects**
- 🎊 **Confetti celebration on success**
- 📊 **Animated stepper progress tracker**
- 🌊 **Floating 3D background shapes**
- 💫 **Particle animation background**
- ✨ **Shimmer effects on result cards**
- 🎯 **Micro-interactions on buttons**

## 🛠️ Tech Stack

**Backend:**
- Python 3.9+
- FastAPI
- SambaNova AI API (OpenAI-compatible)
- Pydantic v2

**Frontend:**
- Streamlit
- Custom CSS animations
- Glass morphism design

## 📁 Project Structure

```
relaunch_ai/
│
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── agent.py             # AI Agent orchestrator
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration settings
│   └── services/
│       ├── __init__.py
│       ├── skill_gap.py     # Skill gap analysis
│       ├── resume_generator.py
│       ├── interview_coach.py
│       ├── roadmap_planner.py
│       └── returnship_finder.py
│
├── frontend/
│   └── app.py               # Streamlit UI with animations
│
├── .env                     # Environment variables
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```

## 🚀 Setup Instructions

### 1. Get SambaNova API Key

1. Sign up at [SambaNova Cloud](https://cloud.sambanova.ai/)
2. Generate an API key from your dashboard
3. Copy the API key for the next step

### 2. Configure Environment

```bash
cd relaunch_ai
```

Edit the `.env` file and add your SambaNova API key:

```bash
SAMBANOVA_API_KEY=your_sambanova_api_key_here
```

### 3. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🎮 Running the Application

### Start the Backend (Terminal 1)

```bash
python -m backend.main
```

The backend will start on `http://localhost:8000`

**API Documentation:** Visit `http://localhost:8000/docs` for interactive API docs.

### Start the Frontend (Terminal 2)

```bash
streamlit run frontend/app.py
```

The frontend will open in your browser at `http://localhost:8501`

## 📝 Usage

1. Open the Streamlit app in your browser
2. Fill in your profile details:
   - Name and education
   - Previous role and experience
   - Career break details
   - Current skills and target role
3. Click **"Generate My Comeback Plan"**
4. Watch the animated stepper progress
5. Enjoy the confetti celebration!
6. Review your personalized recommendations across all tabs

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | API health status |
| `/api/analyze` | POST | Complete analysis pipeline |
| `/api/skill-gap` | POST | Skill gap analysis only |
| `/api/resume` | POST | Resume summary only |
| `/api/interview` | POST | Interview prep only |
| `/api/roadmap` | POST | 30-day roadmap only |
| `/api/returnships` | POST | Returnship programs only |

### Example API Request

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "education": "Bachelor of Science in Computer Science",
    "previous_role": "Software Engineer",
    "years_experience": 5,
    "break_duration_months": 24,
    "break_reason": "childcare",
    "skills_known": ["Python", "Java", "SQL", "Agile"],
    "target_role": "Senior Software Engineer",
    "industry": "Technology",
    "location": "San Francisco, CA"
  }'
```

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SAMBANOVA_API_KEY` | Your SambaNova API key | Required |
| `SAMBANOVA_MODEL` | Model to use | Meta-Llama-3.1-8B-Instruct |
| `SAMBANOVA_BASE_URL` | API base URL | https://api.sambanova.ai/v1 |
| `APP_NAME` | Application name | ReLaunchAI |
| `DEBUG` | Debug mode | false |

## 🎨 UI Animation Features

| Feature | Description |
|---------|-------------|
| **Particle Background** | Floating animated particles |
| **3D Floating Shapes** | Gradient orbs with smooth animation |
| **Stepper Animation** | Progress tracker with pulse effects |
| **Glass Morphism** | Translucent cards with blur effects |
| **Shimmer Effect** | Light sweep animation on cards |
| **Confetti Burst** | Celebration animation on success |
| **Button Micro-interactions** | Ripple and scale effects |
| **Fade-in Animations** | Smooth content transitions |

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>
```

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check firewall settings
- Verify `API_BASE_URL` in `frontend/app.py`

### SambaNova API errors
- Verify your API key in `.env`
- Check your SambaNova account has available credits
- Ensure the model specified is available

### CSS not loading properly
- Clear browser cache (Ctrl+Shift+R)
- Check browser console for errors
- Ensure Streamlit version is 1.30+

## 🔄 Available SambaNova Models

- `Meta-Llama-3.1-8B-Instruct` (default)
- `Meta-Llama-3.1-70B-Instruct`
- `Meta-Llama-3.1-405B-Instruct`

Change in `.env`:
```bash
SAMBANOVA_MODEL=Meta-Llama-3.1-70B-Instruct
```

## 📄 License

MIT License - Feel free to use and modify for your needs.

## 💝 Support

For issues or questions, please open an issue in the project repository.

---

**Built with ❤️ for empowering career returns**

Powered by [SambaNova Systems](https://sambanova.ai/)
