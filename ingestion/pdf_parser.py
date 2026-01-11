import pdfplumber
from typing import Dict, List, Any
import re
import os

class PDFParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.data = {
            "endpoints": [],
            "models": {},
            "authentication": {},
            "base_url": "",
            "error_codes": {}
        }
    
    def extract_structured_data(self):
        """Extract structured data from PDF"""
        with pdfplumber.open(self.pdf_path) as pdf:
            full_text = ""
            
            # Extract all text
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n\n"
            
            # Parse using regex patterns
            self._parse_content(full_text)
        
        return self.data
    
    def _parse_content(self, text: str):
        """Parse the extracted text into structured data"""
        lines = text.split('\n')
        
        # Extract base URL
        base_match = re.search(r'Base URL:\s*(https?://[^\s]+)', text)
        if base_match:
            self.data["base_url"] = base_match.group(1)
        
        # Extract authentication
        auth_section = re.search(r'Authentication(.*?)(?=Endpoint:|Model:|Error Codes:|$)', text, re.DOTALL)
        if auth_section:
            auth_text = auth_section.group(1)
            self.data["authentication"] = {
                "header": "Authorization",
                "format": "Bearer <YOUR_API_KEY>",
                "rate_limit": self._extract_rate_limit(auth_text)
            }
        
        # Extract endpoints
        endpoint_pattern = r'Endpoint:\s*(.*?)\n.*?Method:\s*(.*?)\n.*?Path:\s*(.*?)\n.*?Description:\s*(.*?)\n(.*?)(?=Endpoint:|Model:|Error Codes:|$)'
        endpoints = re.findall(endpoint_pattern, text, re.DOTALL)
        
        for endpoint in endpoints:
            endpoint_data = {
                "name": endpoint[0].strip(),
                "method": endpoint[1].strip(),
                "path": endpoint[2].strip(),
                "description": endpoint[3].strip(),
                "parameters": self._extract_parameters(endpoint[4])
            }
            self.data["endpoints"].append(endpoint_data)
        
        # Extract models
        model_pattern = r'Model:\s*(.*?)\n(.*?)(?=Model:|Error Codes:|$)'
        models = re.findall(model_pattern, text, re.DOTALL)
        
        for model in models:
            model_name = model[0].strip()
            self.data["models"][model_name] = {
                "name": model_name,
                "fields": self._extract_model_fields(model[1])
            }
        
        # Extract error codes
        error_pattern = r'(\d{3}):\s*(.*?)(?=\n|$)'
        errors = re.findall(error_pattern, text)
        for code, desc in errors:
            self.data["error_codes"][code] = desc.strip()
    
    def _extract_parameters(self, param_text: str) -> List[Dict]:
        """Extract parameters from text"""
        parameters = []
        lines = param_text.split('\n')
        
        for line in lines:
            if '- ' in line and '(' in line:
                # Clean the line
                line = line.strip()
                if line.startswith('- '):
                    line = line[2:]
                
                # Extract parameter info
                param_match = re.match(r'([a-z_]+)\s*\((.*?)\):\s*(.*)', line)
                if param_match:
                    name = param_match.group(1)
                    type_info = param_match.group(2)
                    description = param_match.group(3)
                    
                    # Check if required
                    is_required = 'required' in type_info.lower()
                    
                    # Check if references a model
                    model_ref = None
                    if 'Address Object' in description or 'Address Object' in type_info:
                        model_ref = 'Address Object'
                    
                    param_data = {
                        "name": name,
                        "type": type_info.split(',')[0].strip(),
                        "required": is_required,
                        "description": description,
                    }
                    
                    if model_ref:
                        param_data["model_reference"] = model_ref
                    
                    parameters.append(param_data)
        
        return parameters
    
    def _extract_model_fields(self, fields_text: str) -> List[Dict]:
        """Extract model fields from text"""
        fields = []
        lines = fields_text.split('\n')
        
        for line in lines:
            if '- ' in line and '(' in line:
                line = line.strip()
                if line.startswith('- '):
                    line = line[2:]
                
                field_match = re.match(r'([a-z_]+)\s*\((.*?)\):\s*(.*)', line)
                if field_match:
                    fields.append({
                        "name": field_match.group(1),
                        "type": field_match.group(2),
                        "description": field_match.group(3)
                    })
        
        return fields
    
    def _extract_rate_limit(self, text: str) -> str:
        """Extract rate limit from authentication text"""
        rate_match = re.search(r'Rate Limit:\s*(.*?)(?=\n|$)', text)
        return rate_match.group(1).strip() if rate_match else "Not specified"

# Parse PDF
# Get the path relative to the script's parent directory (project root)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
pdf_path = os.path.join(project_root, "data", "nexus_logistics_api_v2.pdf")

