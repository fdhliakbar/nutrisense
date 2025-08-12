# Database Setup Instructions

## Setting up Users Table in Supabase

1. Open your Supabase project dashboard
2. Go to the SQL Editor
3. Copy and paste the contents of `setup_users_table.sql`
4. Run the SQL commands

This will:
- Create a `users` table linked to Supabase auth
- Set up Row Level Security (RLS) policies
- Create triggers to automatically manage user profiles
- Handle email confirmation status sync

## Environment Variables

Make sure your `.env` file in the backend directory contains:

```
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Email Confirmation

Supabase requires email confirmation by default. Users must:
1. Register an account
2. Check their email for confirmation link
3. Click the confirmation link
4. Return to the app and login

The app now includes a "Resend Confirmation Email" button if login fails due to unconfirmed email.

## Testing

1. Run the backend: `cd backend && python app.py`
2. Run the frontend: `cd frontend && npm run dev`
3. Test registration and login flow
