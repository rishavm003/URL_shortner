import uvicorn
import webbrowser
import threading

def open_browser():
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    # Open browser after a short delay to let the server start
    threading.Timer(1.5, open_browser).start()
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        reload_excludes=["*.db", "*.db-journal", "*.db-wal"]
    )
