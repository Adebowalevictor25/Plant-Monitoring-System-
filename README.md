
# 🌱 AI-Powered Plant Monitoring System

![Plant Monitoring](https://via.placeholder.com/800x400?text=AI+Powered+Plant+Monitoring+System)

# 📖 Overview
The **AI-Powered Plant Monitoring System** automates and optimizes plant care by integrating IoT sensors, AI-based health analysis, and a user-friendly web/Telegram interface. Designed for smart gardening enthusiasts, researchers, or anyone who wants healthier plants with minimal effort.

---

## 🚀 Features
- *Real-Time Monitoring*:
  - Tracks soil moisture, light levels, temperature, and humidity.
  - Automatically updates sensor data every minute.
  
- **AI-Based Plant Health Analysis**:
  - Detects diseases, water needs, and light deficiencies.
  - Provides actionable recommendations.

- **Automation**:
  - Scheduled watering and lighting controls.
  - Intelligent actions based on sensor data.

- **Interactive Interfaces**:
  - **Web Dashboard**: Visualize data and manage the system.
  - **Telegram Bot**: Get notifications and control the system remotely.

- **Notification System**:
  - Alerts for low moisture or unhealthy plants.
  - Daily summaries via Telegram or email.

---

## 🛠️ System Architecture

1. **IoT Sensors**: Measure environmental parameters.
2. **AI Analysis**: Uses TensorFlow to analyze plant health.
3. **Database**: SQLite stores historical data and logs.
4. **Web Interface**: Flask-powered dashboard.
5. **Telegram Bot**: Sends notifications and takes commands.

---

## 📋 Installation

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- Libraries: TensorFlow, Flask, schedule, SQLite3, Matplotlib, Telegram Bot API.

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/plant-monitoring.git
   cd plant-monitoring
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**:
   ```bash
   python database.py
   ```

4. **Start the web interface**:
   ```bash
   python web_interface.py
   ```

5. **Run the Telegram Bot**:
   ```bash
   python telegram_bot.py
   ```

6. **Train the AI Model** (optional):
   ```bash
   python ml_training.py
   ```

---

## 🌟 Usage

### Web Interface
- Access the dashboard at `http://localhost:5000`.
- View real-time sensor data, history, and AI analysis results.

### Telegram Bot Commands
- `/status`: View sensor data.
- `/analyze`: Perform AI analysis.
- `/set_schedule`: Schedule watering or lighting.
- `/reset`: Reset the system.

---

## 📊 Visualization

![Sensor Data Graph](https://via.placeholder.com/800x400?text=Sensor+Data+Graph)

---

# 📄 License
© 2023 Oleksii Hrachov. This project is licensed, Proprietary License. See the LICENSE file for details.
"""