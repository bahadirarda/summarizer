"""
Documentation Routes
Comprehensive API documentation with interactive examples
"""

from flask import Blueprint, render_template_string

# Create Blueprint
bp = Blueprint("docs", __name__, url_prefix="/")


@bp.route("/", methods=["GET"])
def api_documentation():
    """API Documentation Homepage"""

    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Summarizer Framework API Documentation</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            color: #333; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .header p {
            color: #666;
            font-size: 1.2em;
        }
        .endpoint-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .endpoint-section h2 {
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        .endpoint-section h2::before {
            content: '🔗';
            margin-right: 10px;
        }
        .endpoint {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        .method {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
            margin-right: 10px;
        }
        .get { background: #28a745; }
        .post { background: #007bff; }
        .put { background: #ffc107; color: #333; }
        .delete { background: #dc3545; }
        .endpoint-path {
            font-family: 'Courier New', monospace;
            background: #e9ecef;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        .description {
            margin-top: 10px;
            color: #666;
        }
        .example {
            background: #f1f3f4;
            border-radius: 8px;
            padding: 15px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
        }
        .example-title {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 8px;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .feature {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        }
        .feature-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .feature h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .params {
            background: #e8f4f8;
            border-radius: 8px;
            padding: 15px;
            margin-top: 10px;
        }
        .params h4 {
            color: #667eea;
            margin-bottom: 8px;
        }
        .param {
            margin-bottom: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            color: rgba(255, 255, 255, 0.8);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Summarizer Framework API</h1>
            <p>AI-Powered Changelog Management & Code Analysis REST API</p>
        </div>

        <div class="features">
            <div class="feature">
                <div class="feature-icon">🤖</div>
                <h3>AI-Powered Analysis</h3>
                <p>Gemini AI integration for intelligent code analysis and changelog generation</p>
            </div>
            <div class="feature">
                <div class="feature-icon">📊</div>
                <h3>Rich Analytics</h3>
                <p>Comprehensive statistics, timelines, and filtering capabilities</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🔍</div>
                <h3>Advanced Search</h3>
                <p>Powerful search and pagination features for efficient data retrieval</p>
            </div>
            <div class="feature">
                <div class="feature-icon">📝</div>
                <h3>Multiple Formats</h3>
                <p>JSON and Markdown export capabilities for seamless integration</p>
            </div>
        </div>

        <div class="endpoint-section">
            <h2>📋 Changelog Endpoints</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/changelog/</span>
                <div class="description">Get paginated changelog entries with optional filtering</div>
                <div class="params">
                    <h4>Query Parameters:</h4>
                    <div class="param">• limit: Number of results (default: 20)</div>
                    <div class="param">• page: Page number (default: 1)</div>
                    <div class="param">• change_type: Filter by type (feature, bugfix, test, etc.)</div>
                    <div class="param">• impact_level: Filter by impact (low, medium, high)</div>
                </div>
                <div class="example">
                    <div class="example-title">Example:</div>
                    curl "http://localhost:5002/api/changelog/?limit=5&change_type=feature"
                </div>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/changelog/stats</span>
                <div class="description">Get comprehensive changelog statistics and metrics</div>
                <div class="example">
                    <div class="example-title">Example:</div>
                    curl "http://localhost:5002/api/changelog/stats"
                </div>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/changelog/entry/&lt;id&gt;</span>
                <div class="description">Get specific changelog entry by ID</div>
                <div class="example">
                    <div class="example-title">Example:</div>
                    curl "http://localhost:5002/api/changelog/entry/entry_20250611_150853"
                </div>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/changelog/search</span>
                <div class="description">Search changelog entries by content</div>
                <div class="params">
                    <h4>Query Parameters:</h4>
                    <div class="param">• q: Search query (required)</div>
                    <div class="param">• fields: Fields to search (summary, files, tags)</div>
                </div>
                <div class="example">
                    <div class="example-title">Example:</div>
                    curl "http://localhost:5002/api/changelog/search?q=gemini&fields=summary,tags"
                </div>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/changelog/timeline</span>
                <div class="description">Get timeline view of changelog entries</div>
                <div class="params">
                    <h4>Query Parameters:</h4>
                    <div class="param">• granularity: Time grouping (daily, weekly, monthly)</div>
                </div>
                <div class="example">
                    <div class="example-title">Example:</div>
                    curl "http://localhost:5002/api/changelog/timeline?granularity=weekly"
                </div>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/changelog/export</span>
                <div class="description">Export changelog in different formats</div>
                <div class="params">
                    <h4>Query Parameters:</h4>
                    <div class="param">• format: Export format (json, markdown)</div>
                </div>
                <div class="example">
                    <div class="example-title">Example:</div>
                    curl "http://localhost:5002/api/changelog/export?format=markdown" -o CHANGELOG.md
                </div>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/changelog/tags</span>
                <div class="description">Get all available tags with usage counts</div>
                <div class="example">
                    <div class="example-title">Example:</div>
                    curl "http://localhost:5002/api/changelog/tags"
                </div>
            </div>
        </div>

        <div class="endpoint-section">
            <h2>🏥 System Endpoints</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/health</span>
                <div class="description">Health check and system status</div>
                <div class="example">
                    <div class="example-title">Example:</div>
                    curl "http://localhost:5002/api/health"
                </div>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/info</span>
                <div class="description">API information and available endpoints overview</div>
                <div class="example">
                    <div class="example-title">Example:</div>
                    curl "http://localhost:5002/api/info"
                </div>
            </div>
        </div>

        <div class="endpoint-section">
            <h2>🧪 Test Endpoints</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/test</span>
                <div class="description">Simple test endpoint for API connectivity verification</div>
                <div class="example">
                    <div class="example-title">Example:</div>
                    curl "http://localhost:5002/api/test"
                </div>
            </div>
        </div>

        <div class="footer">
            <p>🔧 Powered by Flask & Gemini AI | 📊 Built with ❤️ for Developer Productivity</p>
        </div>
    </div>
</body>
</html>
    """

    return render_template_string(html_template)
