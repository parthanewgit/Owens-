from pyngrok import ngrok
import time

# Kill any existing tunnels
ngrok.kill()

# Create tunnel for Streamlit (port 8501)
print("Creating secure tunnel for Streamlit...")
streamlit_tunnel = ngrok.connect(8501, "http")
streamlit_url = streamlit_tunnel.public_url

# Create tunnel for FastAPI (port 8000)
print("Creating secure tunnel for FastAPI...")
fastapi_tunnel = ngrok.connect(8000, "http")
fastapi_url = fastapi_tunnel.public_url

print("\n" + "="*60)
print("🎉 SECURE TUNNELS CREATED!")
print("="*60)
print(f"🌐 Frontend (Streamlit): {streamlit_url}")
print(f"⚙️  Backend API: {fastapi_url}")
print(f"📚 API Docs: {fastapi_url}/docs")
print("="*60)
print("✅ These URLs work from ANYWHERE (mobile data, other networks)")
print("✅ Secure HTTPS encryption included")
print("❌ URLs change each time you restart")
print("\nPress Ctrl+C to stop tunnels...")

try:
    # Keep the tunnels alive
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping tunnels...")
    ngrok.kill()