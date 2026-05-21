
from pyngrok import ngrok
import os

# Kill existing tunnels
ngrok.kill()

# Create Streamlit tunnel
public_url = ngrok.connect(8501)

print("Streamlit App URL:")
print(public_url)

# Run Streamlit
os.system("streamlit run app.py --server.port 8501")
