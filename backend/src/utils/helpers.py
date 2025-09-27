import os
import logging
from datetime import datetime, timedelta
from functools import wraps
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
import requests

def setup_logging(app):
    """Set up logging configuration."""
    if not app.debug:
        # Production logging
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = logging.FileHandler('logs/smart_city.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Smart City Management Platform startup')

def send_email(to_email, subject, body, html_body=None):
    """Send email notification."""
    try:
        smtp_server = current_app.config.get('MAIL_SERVER')
        smtp_port = current_app.config.get('MAIL_PORT')
        smtp_username = current_app.config.get('MAIL_USERNAME')
        smtp_password = current_app.config.get('MAIL_PASSWORD')
        
        if not all([smtp_server, smtp_username, smtp_password]):
            current_app.logger.warning('Email configuration incomplete')
            return False
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = smtp_username
        msg['To'] = to_email
        
        # Add text part
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML part if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        return True
    
    except Exception as e:
        current_app.logger.error(f'Failed to send email: {e}')
        return False

def send_sms(phone_number, message):
    """Send SMS notification (placeholder implementation)."""
    try:
        # This is a placeholder implementation
        # In production, integrate with SMS service like Twilio, AWS SNS, etc.
        current_app.logger.info(f'SMS sent to {phone_number}: {message}')
        return True
    
    except Exception as e:
        current_app.logger.error(f'Failed to send SMS: {e}')
        return False

def send_push_notification(user_id, title, message, data=None):
    """Send push notification (placeholder implementation)."""
    try:
        # This is a placeholder implementation
        # In production, integrate with Firebase Cloud Messaging, Apple Push Notifications, etc.
        current_app.logger.info(f'Push notification sent to user {user_id}: {title} - {message}')
        return True
    
    except Exception as e:
        current_app.logger.error(f'Failed to send push notification: {e}')
        return False

def get_weather_data(lat, lon):
    """Get weather data from external API."""
    try:
        api_key = current_app.config.get('WEATHER_API_KEY')
        if not api_key:
            return None
        
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': api_key,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'weather': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'visibility': data.get('visibility', 0) / 1000  # Convert to km
        }
    
    except Exception as e:
        current_app.logger.error(f'Failed to get weather data: {e}')
        return None

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates using Haversine formula."""
    import math
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def format_datetime(dt, format_string='%Y-%m-%d %H:%M:%S'):
    """Format datetime object to string."""
    if isinstance(dt, datetime):
        return dt.strftime(format_string)
    return str(dt)

def parse_datetime(date_string, format_string='%Y-%m-%d %H:%M:%S'):
    """Parse datetime string to datetime object."""
    try:
        return datetime.strptime(date_string, format_string)
    except ValueError:
        # Try ISO format
        try:
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except ValueError:
            return None

def generate_report_filename(report_type, date=None):
    """Generate filename for reports."""
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime('%Y%m%d_%H%M%S')
    return f"smart_city_{report_type}_report_{date_str}.pdf"

def validate_coordinates(lat, lon):
    """Validate latitude and longitude coordinates."""
    try:
        lat = float(lat)
        lon = float(lon)
        
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return True, lat, lon
        else:
            return False, None, None
    except (ValueError, TypeError):
        return False, None, None

def cache_result(timeout=300):
    """Decorator to cache function results (simple in-memory cache)."""
    cache = {}
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            
            # Check if result is in cache and not expired
            if key in cache:
                result, timestamp = cache[key]
                if datetime.now() - timestamp < timedelta(seconds=timeout):
                    return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache[key] = (result, datetime.now())
            
            # Clean old cache entries (simple cleanup)
            current_time = datetime.now()
            expired_keys = [
                k for k, (_, timestamp) in cache.items()
                if current_time - timestamp >= timedelta(seconds=timeout * 2)
            ]
            for k in expired_keys:
                del cache[k]
            
            return result
        return wrapper
    return decorator

def retry_on_failure(max_retries=3, delay=1):
    """Decorator to retry function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(delay * (attempt + 1))  # Exponential backoff
                    else:
                        current_app.logger.error(f'Function {func.__name__} failed after {max_retries} attempts: {e}')
            
            raise last_exception
        return wrapper
    return decorator

def sanitize_filename(filename):
    """Sanitize filename for safe file operations."""
    import re
    
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing whitespace and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename

def generate_api_key():
    """Generate a random API key."""
    import secrets
    import string
    
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def hash_password(password):
    """Hash password using bcrypt."""
    import bcrypt
    
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed):
    """Verify password against hash."""
    import bcrypt
    
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def get_client_ip(request):
    """Get client IP address from request."""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

def is_valid_email(email):
    """Validate email address format."""
    import re
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    """Validate phone number format."""
    import re
    
    # Simple phone validation (adjust pattern as needed)
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone.replace(' ', '').replace('-', '')) is not None

def convert_timezone(dt, from_tz, to_tz):
    """Convert datetime from one timezone to another."""
    try:
        import pytz
        
        if dt.tzinfo is None:
            dt = from_tz.localize(dt)
        else:
            dt = dt.astimezone(from_tz)
        
        return dt.astimezone(to_tz)
    except Exception as e:
        current_app.logger.error(f'Timezone conversion failed: {e}')
        return dt

def create_thumbnail(image_path, thumbnail_path, size=(150, 150)):
    """Create thumbnail from image."""
    try:
        from PIL import Image
        
        with Image.open(image_path) as img:
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, optimize=True, quality=85)
        
        return True
    except Exception as e:
        current_app.logger.error(f'Thumbnail creation failed: {e}')
        return False
