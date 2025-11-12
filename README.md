<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drone Mission Conflict Detection System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #1a3c6e 0%, #2c5282 100%);
            color: white;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        h1 {
            font-size: 3em;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .tagline {
            font-size: 1.4em;
            opacity: 0.9;
            font-weight: 300;
        }

        .overview {
            background: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        h2 {
            color: #1a3c6e;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #e53e3e;
            display: inline-block;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .feature-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #e53e3e;
            transition: transform 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }

        .feature-card h3 {
            color: #1a3c6e;
            margin-bottom: 10px;
        }

        .code-block {
            background: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
        }

        .steps {
            display: flex;
            flex-direction: column;
            gap: 20px;
            margin: 20px 0;
        }

        .step {
            display: flex;
            align-items: flex-start;
            gap: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }

        .step-number {
            background: #e53e3e;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            flex-shrink: 0;
        }

        .safety-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .safety-table th {
            background: #1a3c6e;
            color: white;
            padding: 15px;
            text-align: left;
        }

        .safety-table td {
            padding: 15px;
            border-bottom: 1px solid #e2e8f0;
        }

        .safety-table tr:nth-child(even) {
            background: #f8f9fa;
        }

        .severity-critical { background: #fed7d7 !important; }
        .severity-high { background: #feebc8 !important; }
        .severity-moderate { background: #fefcbf !important; }
        .severity-safe { background: #c6f6d5 !important; }

        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }

        .tech-tag {
            background: #2c5282;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }

        .footer {
            text-align: center;
            padding: 30px;
            background: #1a3c6e;
            color: white;
            border-radius: 15px;
            margin-top: 40px;
        }

        .btn {
            display: inline-block;
            background: #e53e3e;
            color: white;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            margin: 10px 5px;
        }

        .btn:hover {
            background: #c53030;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        @media (max-width: 768px) {
            h1 { font-size: 2em; }
            .tagline { font-size: 1.1em; }
            .features-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚁 Drone Mission Conflict Detection System</h1>
            <p class="tagline">Advanced airspace safety management with real-time conflict detection</p>
            <div style="margin-top: 20px;">
                <a href="#installation" class="btn">Get Started</a>
                <a href="#features" class="btn">View Features</a>
            </div>
        </header>

        <section class="overview">
            <h2>🚀 Overview</h2>
            <p>A comprehensive drone mission planning and conflict detection system designed to ensure <strong>safe airspace operations</strong>. The system checks for <strong>temporal and spatial conflicts</strong> between multiple drone missions, using deterministic algorithms with optional AI enhancements for predictive analysis.</p>
        </section>

        <section class="section" id="features">
            <h2>📋 Key Features</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <h3>🎯 Mission Generation</h3>
                    <p>Create realistic drone mission datasets with customizable parameters and waypoints.</p>
                </div>
                <div class="feature-card">
                    <h3>⚡ Conflict Detection</h3>
                    <p>Advanced temporal and spatial conflict detection with configurable safety buffers.</p>
                </div>
                <div class="feature-card">
                    <h3>📊 3D Visualization</h3>
                    <p>Interactive 3D mission visualization with real-time conflict highlighting.</p>
                </div>
                <div class="feature-card">
                    <h3>🕒 Temporal Analysis</h3>
                    <p>Efficient O(1) interval checks for overlapping mission windows.</p>
                </div>
                <div class="feature-card">
                    <h3>📍 Spatial Analysis</h3>
                    <p>3D line-segment distance checks with continuous trajectory evaluation.</p>
                </div>
                <div class="feature-card">
                    <h3>📈 Scalability Ready</h3>
                    <p>Architecture designed for migration to spatial-temporal databases and distributed processing.</p>
                </div>
            </div>
        </section>

        <section class="section" id="installation">
            <h2>🛠 Installation & Setup</h2>
            
            <h3 style="margin-top: 20px;">Prerequisites</h3>
            <div class="code-block">
# Required Python packages<br>
pip install pandas numpy matplotlib flask
            </div>

            <h3 style="margin-top: 25px;">Quick Start Guide</h3>
            <div class="steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <div>
                        <strong>Generate Mission Files</strong><br>
                        <div class="code-block" style="margin: 10px 0;">
python simulated_mission.py
                        </div>
                        <em>Generates mission_compact.csv and missions_expanded.csv</em>
                    </div>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <div>
                        <strong>Create Test Scenarios</strong><br>
                        <div class="code-block" style="margin: 10px 0;">
python create_test_missions.py
                        </div>
                        <em>Generates various conflict scenarios in test_missions/</em>
                    </div>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <div>
                        <strong>Run Detection System</strong><br>
                        <div class="code-block" style="margin: 10px 0;">
python io.py
                        </div>
                        <em>Choose manual input or CSV batch processing</em>
                    </div>
                </div>
                <div class="step">
                    <div class="step-number">4</div>
                    <div>
                        <strong>Launch Web Interface</strong><br>
                        <div class="code-block" style="margin: 10px 0;">
python app.py
                        </div>
                        <em>Access at http://localhost:5000</em>
                    </div>
                </div>
            </div>
        </section>

        <section class="section">
            <h2>🛡 Safety Buffer System</h2>
            
            <table class="safety-table">
                <thead>
                    <tr>
                        <th>Severity Level</th>
                        <th>Distance Range</th>
                        <th>Description</th>
                        <th>Visual Indicator</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="severity-critical">
                        <td>🚨 Critical</td>
                        <td>≤ 5m</td>
                        <td>Immediate danger - High collision risk</td>
                        <td>Solid red spheres</td>
                    </tr>
                    <tr class="severity-high">
                        <td>⚠️ High</td>
                        <td>5m - 8m</td>
                        <td>High risk - Requires immediate attention</td>
                        <td>Dark orange zones</td>
                    </tr>
                    <tr class="severity-moderate">
                        <td>📍 Moderate</td>
                        <td>8m - 10m</td>
                        <td>Moderate risk - Proceed with caution</td>
                        <td>Light orange zones</td>
                    </tr>
                    <tr class="severity-safe">
                        <td>✅ Safe</td>
                        <td>> 10m</td>
                        <td>No conflict - Clear for operation</td>
                        <td>No visual warning</td>
                    </tr>
                </tbody>
            </table>

            <h3 style="margin-top: 25px;">Configuration Example</h3>
            <div class="code-block">
# Adjust safety buffer in your code<br>
checker = MissionConflictChecker(safety_buffer_m=15.0)  # 15m buffer
            </div>
        </section>

        <section class="section">
            <h2>🏗 Project Structure</h2>
            <div class="code-block">
drone_mission-conflict_detection-system_gui/<br>
├── app.py                      # Flask web application<br>
├── simulated_mission.py        # Mission generation<br>
├── create_test_missions.py     # Test scenario creation<br>
├── io.py                       # Command-line interface<br>
├── requirements.txt            # Python dependencies<br>
├── static/<br>
│   ├── css/style.css          # Web interface styles<br>
│   └── js/main.js             # Frontend functionality<br>
├── templates/index.html        # Main web interface<br>
├── data/                       # Mission data storage<br>
└── test_missions/              # Test scenarios
            </div>
        </section>

        <section class="section">
            <h2>🔧 Technical Stack</h2>
            <div class="tech-stack">
                <span class="tech-tag">Python 3.8+</span>
                <span class="tech-tag">Pandas</span>
                <span class="tech-tag">NumPy</span>
                <span class="tech-tag">Matplotlib</span>
                <span class="tech-tag">Flask</span>
                <span class="tech-tag">HTML5</span>
                <span class="tech-tag">CSS3</span>
                <span class="tech-tag">JavaScript</span>
                <span class="tech-tag">3D Visualization</span>
            </div>
        </section>

        <section class="section">
            <h2>📈 Scaling Architecture</h2>
            <ul style="margin-left: 20px; margin-top: 15px;">
                <li><strong>Database Migration:</strong> CSV → PostGIS/Redis with spatial indexing</li>
                <li><strong>Temporal Interpolation:</strong> Continuous trajectory evaluation</li>
                <li><strong>Spatial Indexing:</strong> R-tree/Quadtree for O(n log n) filtering</li>
                <li><strong>Parallel Processing:</strong> Distributed mission batches</li>
                <li><strong>Infrastructure:</strong> Kubernetes + Redis + Kafka for real-time deployment</li>
            </ul>
        </section>

        <div class="footer">
            <h3>Developed by Kunal Chattaraj</h3>
            <p>For demonstration and simulation purposes only</p>
            <div style="margin-top: 20px;">
                <a href="https://github.com/KunalChattaraj/drone_mission-conflict_detection-system_gui" class="btn">View on GitHub</a>
            </div>
        </div>
    </div>

    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Add subtle animations
        document.addEventListener('DOMContentLoaded', function() {
            const features = document.querySelectorAll('.feature-card');
            features.forEach((feature, index) => {
                feature.style.animationDelay = `${index * 0.1}s`;
                feature.classList.add('fade-in');
            });
        });
    </script>
</body>
</html>
