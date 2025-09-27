from flask_socketio import emit, join_room, leave_room, disconnect
from flask_jwt_extended import decode_token, get_jwt_identity
from src.models.user import User
from app import socketio
import logging

# Store connected users
connected_users = {}

@socketio.on('connect')
def handle_connect(auth):
    """Handle client connection."""
    try:
        # Verify JWT token
        if auth and 'token' in auth:
            token = auth['token']
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
            
            user = User.find_by_id(user_id)
            if user and user.is_active:
                connected_users[request.sid] = {
                    'user_id': user_id,
                    'user': user,
                    'connected_at': datetime.utcnow()
                }
                
                # Join user to appropriate rooms based on role
                join_user_rooms(user)
                
                emit('connected', {
                    'message': 'Connected successfully',
                    'user_id': user_id,
                    'timestamp': datetime.utcnow().isoformat()
                })
                
                logging.info(f'User {user_id} connected via WebSocket')
            else:
                emit('error', {'message': 'Invalid user or inactive account'})
                disconnect()
        else:
            emit('error', {'message': 'Authentication required'})
            disconnect()
    
    except Exception as e:
        logging.error(f'WebSocket connection error: {e}')
        emit('error', {'message': 'Connection failed'})
        disconnect()

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    try:
        if request.sid in connected_users:
            user_info = connected_users[request.sid]
            user_id = user_info['user_id']
            
            # Leave all rooms
            leave_user_rooms(user_info['user'])
            
            # Remove from connected users
            del connected_users[request.sid]
            
            logging.info(f'User {user_id} disconnected from WebSocket')
    
    except Exception as e:
        logging.error(f'WebSocket disconnection error: {e}')

@socketio.on('join_room')
def handle_join_room(data):
    """Handle joining a specific room."""
    try:
        if request.sid not in connected_users:
            emit('error', {'message': 'Not authenticated'})
            return
        
        room = data.get('room')
        user_info = connected_users[request.sid]
        user = user_info['user']
        
        # Check if user has permission to join the room
        if can_join_room(user, room):
            join_room(room)
            emit('joined_room', {
                'room': room,
                'message': f'Joined room {room}',
                'timestamp': datetime.utcnow().isoformat()
            })
            logging.info(f'User {user_info["user_id"]} joined room {room}')
        else:
            emit('error', {'message': f'Permission denied for room {room}'})
    
    except Exception as e:
        logging.error(f'Error joining room: {e}')
        emit('error', {'message': 'Failed to join room'})

@socketio.on('leave_room')
def handle_leave_room(data):
    """Handle leaving a specific room."""
    try:
        if request.sid not in connected_users:
            emit('error', {'message': 'Not authenticated'})
            return
        
        room = data.get('room')
        user_info = connected_users[request.sid]
        
        leave_room(room)
        emit('left_room', {
            'room': room,
            'message': f'Left room {room}',
            'timestamp': datetime.utcnow().isoformat()
        })
        logging.info(f'User {user_info["user_id"]} left room {room}')
    
    except Exception as e:
        logging.error(f'Error leaving room: {e}')
        emit('error', {'message': 'Failed to leave room'})

@socketio.on('subscribe_alerts')
def handle_subscribe_alerts(data):
    """Subscribe to specific alert types."""
    try:
        if request.sid not in connected_users:
            emit('error', {'message': 'Not authenticated'})
            return
        
        alert_types = data.get('alert_types', [])
        severity_levels = data.get('severity_levels', [])
        modules = data.get('modules', [])
        
        user_info = connected_users[request.sid]
        user = user_info['user']
        
        # Store subscription preferences
        subscription_key = f'alerts_{user_info["user_id"]}'
        connected_users[request.sid]['alert_subscriptions'] = {
            'alert_types': alert_types,
            'severity_levels': severity_levels,
            'modules': modules
        }
        
        emit('subscribed_alerts', {
            'message': 'Alert subscriptions updated',
            'subscriptions': connected_users[request.sid]['alert_subscriptions'],
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        logging.error(f'Error subscribing to alerts: {e}')
        emit('error', {'message': 'Failed to subscribe to alerts'})

@socketio.on('request_real_time_data')
def handle_real_time_data_request(data):
    """Handle request for real-time data."""
    try:
        if request.sid not in connected_users:
            emit('error', {'message': 'Not authenticated'})
            return
        
        data_type = data.get('data_type')
        user_info = connected_users[request.sid]
        user = user_info['user']
        
        # Check permissions
        if not has_data_permission(user, data_type):
            emit('error', {'message': f'Permission denied for {data_type} data'})
            return
        
        # Get and send real-time data
        real_time_data = get_real_time_data(data_type)
        emit('real_time_data', {
            'data_type': data_type,
            'data': real_time_data,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        logging.error(f'Error handling real-time data request: {e}')
        emit('error', {'message': 'Failed to get real-time data'})

@socketio.on('send_message')
def handle_send_message(data):
    """Handle sending messages between users."""
    try:
        if request.sid not in connected_users:
            emit('error', {'message': 'Not authenticated'})
            return
        
        recipient_id = data.get('recipient_id')
        message = data.get('message')
        message_type = data.get('type', 'text')
        
        user_info = connected_users[request.sid]
        sender_id = user_info['user_id']
        
        # Find recipient's session
        recipient_sid = None
        for sid, user_data in connected_users.items():
            if user_data['user_id'] == recipient_id:
                recipient_sid = sid
                break
        
        if recipient_sid:
            # Send message to recipient
            socketio.emit('new_message', {
                'sender_id': sender_id,
                'sender_name': f"{user_info['user'].first_name} {user_info['user'].last_name}",
                'message': message,
                'type': message_type,
                'timestamp': datetime.utcnow().isoformat()
            }, room=recipient_sid)
            
            # Confirm to sender
            emit('message_sent', {
                'recipient_id': recipient_id,
                'message': 'Message sent successfully',
                'timestamp': datetime.utcnow().isoformat()
            })
        else:
            emit('error', {'message': 'Recipient not online'})
    
    except Exception as e:
        logging.error(f'Error sending message: {e}')
        emit('error', {'message': 'Failed to send message'})

def join_user_rooms(user):
    """Join user to appropriate rooms based on their role."""
    # All authenticated users join general room
    join_room('authenticated_users')
    
    # Role-based rooms
    if user.role == 'admin':
        join_room('admin')
        join_room('all_modules')
    
    if user.has_permission('traffic.read'):
        join_room('traffic_monitoring')
    
    if user.has_permission('environment.read'):
        join_room('environment_monitoring')
    
    if user.has_permission('waste.read'):
        join_room('waste_monitoring')
    
    if user.has_permission('energy.read'):
        join_room('energy_monitoring')
    
    if user.has_permission('emergency.read'):
        join_room('emergency_response')
    
    if user.has_permission('alerts.read'):
        join_room('alerts')
    
    if user.has_permission('dashboard.read'):
        join_room('dashboard_updates')

def leave_user_rooms(user):
    """Leave all user rooms."""
    rooms_to_leave = [
        'authenticated_users',
        'admin',
        'all_modules',
        'traffic_monitoring',
        'environment_monitoring',
        'waste_monitoring',
        'energy_monitoring',
        'emergency_response',
        'alerts',
        'dashboard_updates'
    ]
    
    for room in rooms_to_leave:
        leave_room(room)

def can_join_room(user, room):
    """Check if user can join a specific room."""
    room_permissions = {
        'traffic_monitoring': 'traffic.read',
        'environment_monitoring': 'environment.read',
        'waste_monitoring': 'waste.read',
        'energy_monitoring': 'energy.read',
        'emergency_response': 'emergency.read',
        'alerts': 'alerts.read',
        'dashboard_updates': 'dashboard.read',
        'admin': 'all',
        'public_alerts': None  # Public room
    }
    
    required_permission = room_permissions.get(room)
    
    if required_permission is None:  # Public room
        return True
    
    return user.has_permission(required_permission)

def has_data_permission(user, data_type):
    """Check if user has permission to access specific data type."""
    data_permissions = {
        'traffic': 'traffic.read',
        'environment': 'environment.read',
        'waste': 'waste.read',
        'energy': 'energy.read',
        'emergency': 'emergency.read',
        'dashboard': 'dashboard.read'
    }
    
    required_permission = data_permissions.get(data_type)
    if not required_permission:
        return False
    
    return user.has_permission(required_permission)

def get_real_time_data(data_type):
    """Get real-time data for specific type."""
    # This would fetch actual real-time data from your models
    # Placeholder implementation
    from datetime import datetime
    
    if data_type == 'traffic':
        return {
            'active_incidents': 3,
            'average_congestion': 2.1,
            'traffic_flow': 1250
        }
    elif data_type == 'environment':
        return {
            'average_aqi': 85,
            'active_alerts': 1,
            'sensor_count': 15
        }
    elif data_type == 'waste':
        return {
            'full_bins': 12,
            'active_collections': 3,
            'efficiency': 89.5
        }
    elif data_type == 'energy':
        return {
            'grid_load': 78.5,
            'renewable_generation': 125.8,
            'efficiency': 94.2
        }
    else:
        return {}

def broadcast_alert(alert_data, room='alerts'):
    """Broadcast alert to specific room."""
    try:
        socketio.emit('new_alert', alert_data, room=room)
        logging.info(f'Alert broadcasted to room {room}')
    except Exception as e:
        logging.error(f'Error broadcasting alert: {e}')

def broadcast_update(update_data, room):
    """Broadcast update to specific room."""
    try:
        socketio.emit('system_update', update_data, room=room)
        logging.info(f'Update broadcasted to room {room}')
    except Exception as e:
        logging.error(f'Error broadcasting update: {e}')

def send_notification_to_user(user_id, notification_data):
    """Send notification to specific user."""
    try:
        # Find user's session
        for sid, user_data in connected_users.items():
            if user_data['user_id'] == user_id:
                socketio.emit('notification', notification_data, room=sid)
                logging.info(f'Notification sent to user {user_id}')
                return True
        
        logging.warning(f'User {user_id} not found in connected users')
        return False
    except Exception as e:
        logging.error(f'Error sending notification to user: {e}')
        return False

def get_connected_users_count():
    """Get count of connected users."""
    return len(connected_users)

def get_connected_users_by_role():
    """Get connected users grouped by role."""
    users_by_role = {}
    
    for user_data in connected_users.values():
        role = user_data['user'].role
        if role not in users_by_role:
            users_by_role[role] = 0
        users_by_role[role] += 1
    
    return users_by_role

# Import datetime at the top of the file
from datetime import datetime
from flask import request
