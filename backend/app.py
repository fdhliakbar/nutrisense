from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Nutrisense API is running!',
        'status': 'success',
        'supabase_url': SUPABASE_URL[:30] + '...' if SUPABASE_URL else 'Not set',
        'supabase_key': 'Set' if SUPABASE_KEY else 'Not set'
    })

@app.route('/test', methods=['GET'])
def test():
    try:
        # Test Supabase connection
        response = supabase.table('test').select('*').limit(1).execute()
        return jsonify({
            'message': 'Supabase connection successful',
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'message': 'Supabase connection failed',
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        print(f"Attempting signup for email: {email}")
        
        # Sign up user with Supabase
        try:
            response = supabase.auth.sign_up({
                'email': email,
                'password': password,
                'options': {
                    'data': {
                        'name': name,
                        'display_name': name
                    }
                }
            })
        except Exception as signup_error:
            print(f"Supabase signup error: {signup_error}")
            error_msg = str(signup_error)
            if 'Email logins are disabled' in error_msg:
                return jsonify({
                    'error': 'Email registration is disabled. Please enable Email provider in Supabase Authentication settings.',
                    'details': 'Go to Supabase Dashboard → Authentication → Providers → Enable Email'
                }), 400
            raise signup_error
        
        print(f"Supabase signup response: {response}")
        
        # If signup successful and user exists, create user profile
        if response.user:
            try:
                # Insert into users table
                user_data = {
                    'id': response.user.id,
                    'name': name,
                    'email': email,
                    'created_at': response.user.created_at,
                    'email_confirmed': response.user.email_confirmed_at is not None
                }
                supabase.table('users').insert(user_data).execute()
                print(f"User profile created for user: {response.user.id}")
            except Exception as profile_error:
                print(f"User profile creation error (non-critical): {profile_error}")
                # Try alternative approach - update user metadata
                try:
                    supabase.auth.update_user({
                        'data': {
                            'name': name,
                            'display_name': name
                        }
                    })
                    print(f"User metadata updated for user: {response.user.id}")
                except Exception as metadata_error:
                    print(f"User metadata update error: {metadata_error}")
        
        return jsonify({
            'message': 'User created successfully! Please check your email for confirmation.' if response.user else 'User created successfully!',
            'user': response.user.model_dump() if response.user else None,
            'session': response.session.model_dump() if response.session else None
        }), 201
        
    except Exception as e:
        print(f"Signup error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        print(f"Attempting login for email: {email}")
        
        # Sign in user with Supabase
        try:
            response = supabase.auth.sign_in_with_password({
                'email': email,
                'password': password
            })
        except Exception as login_error:
            print(f"Supabase login error: {login_error}")
            error_msg = str(login_error)
            if 'Email logins are disabled' in error_msg:
                return jsonify({
                    'error': 'Email login is disabled. Please enable Email provider in Supabase Authentication settings.',
                    'details': 'Go to Supabase Dashboard → Authentication → Providers → Enable Email'
                }), 400
            raise login_error
        
        print(f"Login successful for user: {response.user.id if response.user else 'None'}")
        
        return jsonify({
            'message': 'Login successful',
            'user': response.user.model_dump() if response.user else None,
            'session': response.session.model_dump() if response.session else None
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        
        # Handle specific Supabase auth errors
        error_message = str(e)
        if 'Invalid login credentials' in error_message:
            return jsonify({'error': 'Invalid email or password. Please check your credentials.'}), 401
        elif 'Email not confirmed' in error_message or 'email_confirmed_at' in error_message:
            return jsonify({'error': 'Please confirm your email address before signing in.'}), 401
        elif 'signup_disabled' in error_message:
            return jsonify({'error': 'User registration is currently disabled.'}), 401
        else:
            return jsonify({'error': f'Login failed: {error_message}'}), 500

@app.route('/auth/logout', methods=['POST'])
def logout():
    try:
        # Sign out user
        supabase.auth.sign_out()
        
        return jsonify({
            'message': 'Logout successful'
        }), 200
        
    except Exception as e:
        print(f"Logout error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/auth/resend-confirmation', methods=['POST'])
def resend_confirmation():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Resend confirmation email
        response = supabase.auth.resend({
            'type': 'signup',
            'email': email
        })
        
        return jsonify({
            'message': 'Confirmation email sent successfully'
        }), 200
        
    except Exception as e:
        print(f"Resend confirmation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/auth/confirm-email-manual', methods=['POST'])
def confirm_email_manual():
    """
    Manual email confirmation for development/testing purposes
    In production, this should be handled by Supabase email confirmation flow
    """
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Update user email confirmation status manually (for development only)
        # This is a workaround - in production, use proper email confirmation
        try:
            # Update users table
            supabase.table('users').update({
                'email_confirmed': True,
                'updated_at': 'now()'
            }).eq('email', email).execute()
            
            return jsonify({
                'message': 'Email confirmation updated successfully (DEV MODE)',
                'warning': 'This is for development only. Use proper email confirmation in production.'
            }), 200
            
        except Exception as db_error:
            print(f"Database update error: {db_error}")
            return jsonify({'error': 'Failed to update confirmation status'}), 500
        
    except Exception as e:
        print(f"Manual confirmation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/debug/users', methods=['GET'])
def debug_users():
    """Debug endpoint to check users table"""
    try:
        # Get all users from custom users table
        users_response = supabase.table('users').select('*').execute()
        
        # Get auth users count (without sensitive data)
        auth_users_response = supabase.table('users').select('id, email, created_at, email_confirmed').execute()
        
        return jsonify({
            'message': 'Debug info retrieved successfully',
            'users_table': users_response.data,
            'users_count': len(users_response.data) if users_response.data else 0,
            'auth_users_count': len(auth_users_response.data) if auth_users_response.data else 0
        }), 200
        
    except Exception as e:
        print(f"Debug users error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/debug/auth-status', methods=['GET'])
def debug_auth_status():
    """Debug endpoint to check auth configuration"""
    try:
        # Try to get current session/user to test connection
        try:
            current_user = supabase.auth.get_user()
            connection_status = "Connected"
        except Exception as auth_error:
            connection_status = f"Connection error: {str(auth_error)}"
        
        return jsonify({
            'message': 'Auth debug info',
            'supabase_url': SUPABASE_URL[:30] + '...' if SUPABASE_URL else 'Not set',
            'supabase_key_status': 'Set' if SUPABASE_KEY else 'Not set',
            'connection_status': connection_status,
            'auth_instructions': {
                'step1': 'Go to Supabase Dashboard → Authentication → Providers',
                'step2': 'Enable "Email" provider',
                'step3': 'Enable "Allow new signups"',
                'step4': 'Save settings'
            }
        }), 200
        
    except Exception as e:
        print(f"Debug auth status error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/auth/user', methods=['GET'])
def get_user():
    try:
        # Get current user
        user = supabase.auth.get_user()
        
        if user and user.user:
            user_data = user.user.model_dump()
            
            # Try to get additional user data from users table
            try:
                profile_response = supabase.table('users').select('*').eq('id', user.user.id).execute()
                if profile_response.data:
                    user_data['profile'] = profile_response.data[0]
                    # Add display_name from profile if available
                    if 'name' in profile_response.data[0]:
                        user_data['display_name'] = profile_response.data[0]['name']
            except Exception as profile_error:
                print(f"Profile fetch error (non-critical): {profile_error}")
                # Fallback to user metadata
                if user.user.user_metadata and 'name' in user.user.user_metadata:
                    user_data['display_name'] = user.user.user_metadata['name']
            
            return jsonify({
                'user': user_data
            }), 200
        else:
            return jsonify({'error': 'User not authenticated'}), 401
            
    except Exception as e:
        print(f"Get user error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)