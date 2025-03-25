# windmill
SAT solver for windmill with Flask server.

# Install
python3 est requis.
<pre>pip install flask python-sat</pre> 

# Development
<pre>python3 app.py</pre>

# Staging
<pre>gunicorn app:app --timeout 0
ngrok http --url=⟪⟪your-entry-point⟫⟫ http://localhost:8000</pre>

# Production
At your discretion, 
