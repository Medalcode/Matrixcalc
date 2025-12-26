# Quick CORS Fix for MatrixCalc Backend

# Add this to your Django settings.py

CORS_ALLOWED_ORIGINS = [
"http://localhost:5173",
"http://127.0.0.1:5173",
"https://matrixcalc-frontend-772384307164.us-central1.run.app",
"https://matrixcalc-frontend-541716295092.us-central1.run.app", # NEW URL
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
'accept',
'accept-encoding',
'authorization',
'content-type',
'dnt',
'origin',
'user-agent',
'x-csrftoken',
'x-requested-with',
]
