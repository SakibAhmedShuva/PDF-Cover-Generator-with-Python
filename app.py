from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, white, black
from reportlab.lib.units import mm, inch
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw, ImageFilter
from typing import Dict, List, Optional, Tuple
import tempfile
import shutil

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs('templates', exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

class CoverPageGenerator:
    def __init__(self):
        self.page_width, self.page_height = A4
        self.margin = 20 * mm
        
    def hex_to_color(self, hex_color: str) -> Color:
        """Convert hex color to reportlab Color object"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return Color(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    
    def create_gradient_background(self, width: int, height: int, 
                                   start_color: str, end_color: str, 
                                   direction: str = "vertical") -> str:
        """Create a gradient background image"""
        img = Image.new('RGB', (int(width), int(height)))
        draw = ImageDraw.Draw(img)
        
        start_rgb = tuple(int(start_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        end_rgb = tuple(int(end_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        if direction == "vertical":
            for y in range(int(height)):
                ratio = y / height
                r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
                g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
                b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
                draw.line([(0, y), (int(width), y)], fill=(r, g, b))
        else:  # horizontal
            for x in range(int(width)):
                ratio = x / width
                r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
                g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
                b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
                draw.line([(x, 0), (x, int(height))], fill=(r, g, b))
        
        temp_path = f"temp_gradient_{uuid.uuid4().hex}.png"
        img.save(temp_path)
        return temp_path
    
    def add_curved_elements(self, c: canvas.Canvas, config: Dict):
        """Add curved decorative elements"""
        if config.get('curved_elements'):
            c.saveState()
            c.setFillAlpha(0.3)
            
            color = self.hex_to_color(config['curved_elements'].get('color', '#00BCD4'))
            c.setStrokeColor(color)
            c.setLineWidth(2)
            
            # Create flowing curves
            path = c.beginPath()
            path.moveTo(self.page_width * 0.6, self.page_height * 0.4)
            path.curveTo(self.page_width * 0.8, self.page_height * 0.5,
                          self.page_width * 0.9, self.page_height * 0.3,
                          self.page_width * 1.1, self.page_height * 0.6)
            c.drawPath(path, stroke=1, fill=0)
            
            for i in range(3):
                path = c.beginPath()
                start_x = self.page_width * (0.5 + i * 0.1)
                start_y = self.page_height * (0.3 + i * 0.1)
                path.moveTo(start_x, start_y)
                path.curveTo(start_x + 100, start_y + 50,
                              start_x + 150, start_y - 30,
                              start_x + 200, start_y + 80)
                c.drawPath(path, stroke=1, fill=0)
            
            c.restoreState()
    
    def generate_cover_page(self, config: Dict, output_path: str):
        """Generate the cover page based on configuration"""
        c = canvas.Canvas(output_path, pagesize=A4)
        temp_files = []
        
        try:
            # Background
            if config.get('background'):
                bg_config = config['background']
                if bg_config.get('type') == 'gradient':
                    gradient_path = self.create_gradient_background(
                        self.page_width, self.page_height,
                        bg_config.get('start_color', '#FFFFFF'),
                        bg_config.get('end_color', '#00BCD4'),
                        bg_config.get('direction', 'vertical')
                    )
                    temp_files.append(gradient_path)
                    c.drawImage(gradient_path, 0, 0, 
                                width=self.page_width, height=self.page_height)
                elif bg_config.get('type') == 'solid':
                    c.setFillColor(self.hex_to_color(bg_config.get('color', '#FFFFFF')))
                    c.rect(0, 0, self.page_width, self.page_height, fill=1)
                elif bg_config.get('type') == 'image' and bg_config.get('path'):
                    if os.path.exists(bg_config['path']):
                        c.drawImage(bg_config['path'], 0, 0, 
                                    width=self.page_width, height=self.page_height)
            
            # Add curved decorative elements
            self.add_curved_elements(c, config)
            
            # Header section
            if config.get('header'):
                header = config['header']
                y_pos = self.page_height - 80 * mm
                
                if header.get('exclusive_text'):
                    c.setFont("Helvetica-Bold", 24)
                    c.setFillColor(self.hex_to_color(header.get('exclusive_color', '#00BCD4')))
                    c.drawString(self.margin, y_pos, header['exclusive_text'])
                    y_pos -= 12 * mm
                
                if header.get('only_for_text'):
                    c.setFont("Helvetica-Bold", 16)
                    c.setFillColor(self.hex_to_color(header.get('only_for_color', '#9C27B0')))
                    c.drawString(self.margin + 150, y_pos + 8 * mm, header['only_for_text'])
                
                if header.get('company_name'):
                    c.setFont("Helvetica-Bold", 20)
                    c.setFillColor(black)
                    c.drawString(self.margin, y_pos, header['company_name'])
                    y_pos -= 15 * mm
                
                if header.get('company_logo') and os.path.exists(header['company_logo']):
                    c.drawImage(header['company_logo'], self.margin, y_pos - 30 * mm,
                                width=60 * mm, height=30 * mm, preserveAspectRatio=True)
            
            # Main content
            if config.get('main_content'):
                content = config['main_content']
                y_pos = self.page_height * 0.6
                
                if content.get('main_title'):
                    c.setFont("Helvetica-Bold", 48)
                    c.setFillColor(self.hex_to_color(content.get('main_title_color', '#00BCD4')))
                    title_width = c.stringWidth(content['main_title'], "Helvetica-Bold", 48)
                    c.drawString(self.page_width - title_width - self.margin, y_pos, 
                                 content['main_title'])
                    y_pos -= 20 * mm
                
                if content.get('subtitle'):
                    c.setFont("Helvetica-Bold", 16)
                    c.setFillColor(black)
                    
                    lines = content['subtitle'].split('\n')
                    for line in lines:
                        if line.strip():
                            line_width = c.stringWidth(line, "Helvetica-Bold", 16)
                            x_pos = (self.page_width - line_width) / 2
                            c.drawString(x_pos, y_pos, line)
                            y_pos -= 8 * mm
            
            # Footer section
            if config.get('footer'):
                footer = config['footer']
                y_pos = 80 * mm
                
                if footer.get('company_info'):
                    company = footer['company_info']
                    x_pos = self.page_width - 150 * mm
                    
                    if company.get('logo') and os.path.exists(company['logo']):
                        c.drawImage(company['logo'], x_pos, y_pos,
                                    width=40 * mm, height=20 * mm, preserveAspectRatio=True)
                        y_pos -= 25 * mm
                    
                    if company.get('tagline'):
                        c.setFont("Helvetica", 10)
                        c.setFillColor(black)
                        c.drawString(x_pos, y_pos, company['tagline'])
                        y_pos -= 15 * mm
                
                if footer.get('partner'):
                    partner = footer['partner']
                    x_pos = self.page_width - 150 * mm
                    
                    if partner.get('label'):
                        c.setFont("Helvetica-Bold", 12)
                        c.setFillColor(black)
                        c.drawString(x_pos, y_pos, partner['label'])
                        y_pos -= 8 * mm
                    
                    if partner.get('logo') and os.path.exists(partner['logo']):
                        c.drawImage(partner['logo'], x_pos, y_pos - 20 * mm,
                                    width=50 * mm, height=25 * mm, preserveAspectRatio=True)
                    
                    if partner.get('tagline'):
                        c.setFont("Helvetica", 10)
                        c.setFillColor(black)
                        c.drawString(x_pos, y_pos - 25 * mm, partner['tagline'])
            
            c.save()
            
        finally:
            # Clean up temporary files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_sample_config():
    """Get sample configuration"""
    return {
        "background": {
            "type": "gradient",
            "start_color": "#FFFFFF",
            "end_color": "#E0F7FA",
            "direction": "vertical"
        },
        "curved_elements": {
            "color": "#00BCD4"
        },
        "header": {
            "exclusive_text": "EXCLUSIVE",
            "exclusive_color": "#00BCD4",
            "only_for_text": "ONLY FOR",
            "only_for_color": "#9C27B0",
            "company_name": "UTHA FASHION LTD.",
            "company_logo": ""
        },
        "main_content": {
            "main_title": "QUOTATION",
            "main_title_color": "#00BCD4",
            "subtitle": "SUPPLY AND INSTALLATION OF\nADDITIONAL MATERIALS OF FIRE\nHYDRANT AND SPRINKLER SYSTEM"
        },
        "footer": {
            "company_info": {
                "logo": "",
                "tagline": "protect to progress Ltd."
            },
            "partner": {
                "label": "PARTNER OF",
                "logo": "",
                "tagline": "PASSION TO PROTECT"
            }
        }
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sample-config')
def sample_config():
    return jsonify(get_sample_config())

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'filename': filename, 'path': filepath})
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/generate', methods=['POST'])
def generate_cover():
    try:
        config = request.json
        if not config:
            return jsonify({'error': 'No configuration provided'}), 400
        
        # Generate unique filename
        filename = f"cover_page_{uuid.uuid4().hex}.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        # Generate the cover page
        generator = CoverPageGenerator()
        generator.generate_cover_page(config, output_path)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'download_url': f'/api/download/{filename}'
        })
        
    except Exception as e:
        app.logger.error(f"Error generating cover page: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file_route(filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        app.logger.error(f"Error downloading file: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)