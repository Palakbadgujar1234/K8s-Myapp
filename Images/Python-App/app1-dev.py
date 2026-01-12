from flask import Flask, render_template_string

app = Flask(__name__)

# HTML template with emojis and animations
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Name Display App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            /* Animated gradient background - colors change smoothly */
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            animation: gradientShift 5s ease infinite;
            background-size: 200% 200%;
        }
        
        /* Animation for background - makes colors move */
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container {
            text-align: center;
            background: white;
            padding: 50px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            /* Fade in animation when page loads */
            animation: fadeIn 1s ease-in;
        }
        
        /* Fade in effect */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        
        /* Emoji that waves - rotates back and forth */
        .wave-emoji {
            display: inline-block;
            animation: wave 1s ease-in-out infinite;
        }
        
        @keyframes wave {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(20deg); }
            75% { transform: rotate(-20deg); }
        }
        
        .name {
            font-size: 48px;
            color: #667eea;
            font-weight: bold;
            margin: 20px 0;
            /* Pulse animation - name grows and shrinks */
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .info {
            color: #666;
            margin-top: 20px;
            font-size: 18px;
        }
        
        /* Kubernetes emoji that floats up and down */
        .float-emoji {
            display: inline-block;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        /* Sparkle emojis that rotate */
        .sparkle {
            display: inline-block;
            animation: rotate 4s linear infinite;
            margin: 0 10px;
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        /* Footer with emojis */
        .footer {
            margin-top: 30px;
            font-size: 24px;
        }
        
        /* Bounce animation for rocket */
        .bounce {
            display: inline-block;
            animation: bounce 2s ease infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Wave emoji with animation -->
        <h1>
            <span class="wave-emoji">👋</span>
            Welcome to My k8s dev helm App!
            <span class="wave-emoji">👋</span>
        </h1>
        
        <!-- Sparkle emojis around the name -->
        <div>
            <span class="sparkle">✨</span>
            <span class="name">{{ name }}</span>
            <span class="sparkle">✨</span>
        </div>
        
        <!-- Kubernetes info with floating emoji -->
        <div class="info">
            Running in Kubernetes Pod
            <span class="float-emoji">☸️</span>
        </div>
        
        <!-- Footer with more emojis -->
        <div class="footer">
            <span class="bounce">🚀</span>
            💻 🎨 🌟 ⚡ 🎯
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # You can change this name to whatever you want
    name = "Yes palak Badgujar"
    return render_template_string(HTML_TEMPLATE, name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

#Running on Kubernetes!
