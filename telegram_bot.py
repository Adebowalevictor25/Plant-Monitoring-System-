# telegram_bot.py
# Telegram bot for plant monitoring and control system with extended features.

import logging
from datetime import datetime, timedelta
from threading import Timer
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)
from sensors import get_sensor_data
from ai_model import analyze_plant_image

# Constants
TOKEN = "your-telegram-bot-token"
LOG_FILE = "telegram_bot.log"
SCHEDULE_FILE = "watering_schedule.txt"
SYSTEM_STATUS = {
    "light": "off",
    "watering": "off",
    "plants": {"Plant1": {}, "Plant2": {}, "Plant3": {}},
}
WATERING_SCHEDULES = []

# Logging setup
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Helper functions
def log_action(user, action):
    """Logs user actions."""
    logger.info(f"User {user}: {action}")

def format_status():
    """Formats the system's current status for display."""
    return (
        f"Light: {SYSTEM_STATUS['light']}\n"
        f"Watering: {SYSTEM_STATUS['watering']}\n"
        f"Plants: {', '.join(SYSTEM_STATUS['plants'].keys())}"
    )

# Telegram commands
def start(update: Update, context: CallbackContext) -> None:
    """
    Sends a welcome message and displays available commands.
    """
    user = update.effective_user
    welcome_message = f"""
    Hi {user.first_name}, welcome to the Plant Monitoring System!
    Available commands:
    /status - Get current sensor data
    /analyze - Analyze plant health
    /set_schedule - Set watering or light schedule
    /view_schedule - View all schedules
    /cancel_schedule - Cancel a schedule
    /water_now - Water plants immediately
    /light_now - Turn on lights immediately
    /help - Show this help message
    """
    update.message.reply_text(welcome_message)
    log_action(user.first_name, "started the bot")

def status(update: Update, context: CallbackContext) -> None:
    """Sends current system and sensor status."""
    try:
        sensor_data = get_sensor_data()
        status_message = (
            f"Sensor Data:\n"
            f"- Soil Moisture: {sensor_data['soil_moisture']}%\n"
            f"- Light Level: {sensor_data['light_level']} lumens\n"
            f"- Temperature: {sensor_data['temperature']}°C\n"
            f"- Humidity: {sensor_data['humidity']}%\n\n"
            f"System Status:\n{format_status()}"
        )
        update.message.reply_text(status_message)
        log_action(update.effective_user.first_name, "checked status")
    except Exception as e:
        update.message.reply_text("Error retrieving sensor data.")
        logger.error(f"Error in status command: {e}")

def analyze(update: Update, context: CallbackContext) -> None:
    """Performs AI analysis on a plant's health."""
    try:
        plant_name = context.args[0] if context.args else "Plant1"
        if plant_name not in SYSTEM_STATUS["plants"]:
            update.message.reply_text("Invalid plant name.")
            return

        image_path = f"{plant_name}_image.jpg"
        analysis = analyze_plant_image(image_path)
        analysis_message = f"Health Analysis for {plant_name}:\n" + "\n".join(
            [f"- {k}: {v:.2f}" for k, v in analysis.items()]
        )
        update.message.reply_text(analysis_message)
        log_action(update.effective_user.first_name, f"analyzed {plant_name}")
    except Exception as e:
        update.message.reply_text("Error analyzing the plant image.")
        logger.error(f"Error in analyze command: {e}")

def set_schedule(update: Update, context: CallbackContext) -> None:
    """Adds a new watering or light schedule."""
    try:
        args = context.args
        if len(args) < 3:
            update.message.reply_text("Usage: /set_schedule <device> <time> <duration>")
            return
        device, schedule_time, duration = args
        WATERING_SCHEDULES.append((device, schedule_time, duration))
        with open(SCHEDULE_FILE, "a") as f:
            f.write(f"{device} {schedule_time} {duration}\n")
        update.message.reply_text(f"{device.capitalize()} scheduled at {schedule_time} for {duration} minutes.")
        log_action(update.effective_user.first_name, f"scheduled {device} at {schedule_time}")
    except Exception as e:
        update.message.reply_text("Error setting schedule.")
        logger.error(f"Error in set_schedule command: {e}")

def view_schedule(update: Update, context: CallbackContext) -> None:
    """Displays all active schedules."""
    if not WATERING_SCHEDULES:
        update.message.reply_text("No active schedules.")
        return
    schedule_message = "Active Schedules:\n" + "\n".join(
        [f"{device}: {time} for {duration} minutes" for device, time, duration in WATERING_SCHEDULES]
    )
    update.message.reply_text(schedule_message)
    log_action(update.effective_user.first_name, "viewed schedules")

def cancel_schedule(update: Update, context: CallbackContext) -> None:
    """Cancels all active schedules."""
    WATERING_SCHEDULES.clear()
    with open(SCHEDULE_FILE, "w"):
        pass
    update.message.reply_text("All schedules canceled.")
    log_action(update.effective_user.first_name, "canceled all schedules")

def start_bot():
    """Starts the Telegram bot."""
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("status", status))
    updater.dispatcher.add_handler(CommandHandler("analyze", analyze))
    updater.dispatcher.add_handler(CommandHandler("set_schedule", set_schedule))
    updater.dispatcher.add_handler(CommandHandler("view_schedule", view_schedule))
    updater.dispatcher.add_handler(CommandHandler("cancel_schedule", cancel_schedule))

    logger.info("Starting Telegram bot...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    start_bot()