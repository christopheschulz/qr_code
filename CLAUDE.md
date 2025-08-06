# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django web application for QR code generation and reading. The application allows users to generate QR codes for various data types (URLs, text, vCard contacts, SMS, WiFi credentials, etc.) and decode existing QR codes from uploaded images.

## Development Commands

### Running the Application
```bash
cd src
python manage.py runserver
```

### Database Management
```bash
cd src
python manage.py makemigrations
python manage.py migrate
```

### Static Files
```bash
cd src
python manage.py collectstatic
```

### Django Admin
```bash
cd src
python manage.py createsuperuser
```

### Dependencies
Install dependencies using:
```bash
pip install -r requirements.txt
```

## Architecture

### Project Structure
- `src/QrCodeReader/` - Main Django application containing views, forms, templates, and static files
- `src/utils/qr_code.py` - Utility functions for QR code generation and reading
- `src/manage.py` - Django management script
- `src/db.sqlite3` - SQLite database file

### Core Components

**Views (`src/QrCodeReader/views.py`)**:
- `generate_qr_code_view()` - Handles QR code generation for multiple data types
- `qr_reader()` - Handles QR code reading from uploaded images  
- `about()`, `privacy_policy()` - Static page views

**Forms (`src/QrCodeReader/forms.py`)**:
- `QRBaseMixin` - Base mixin with common QR code configuration fields
- Multiple form classes for different QR code types: `QrGenerateUrl`, `QrGenerateVCard`, `QrGenerateSMS`, etc.
- `QrLoader` - Form for uploading QR code images to decode

**Utilities (`src/utils/qr_code.py`)**:
- QR code generation using the `qrcode` library
- QR code reading using OpenCV (`cv2`)
- Configuration management and parameter validation
- Command-line interface for QR operations

### Key Dependencies
- Django 5.2.5 - Web framework
- qrcode 8.2 - QR code generation
- opencv-python 4.12.0.88 - QR code reading and image processing
- Pillow 11.3.0 - Image handling
- numpy 2.2.6 - Array operations for image processing

### Configuration
- Settings in `src/QrCodeReader/settings.py`
- QR code configuration stored in `src/QrCodeReader/config/config.json`
- Static files served from `src/QrCodeReader/static/`
- Media files (generated QR codes) stored in `src/media/qr_codes/`

### Templates
HTML templates located in `src/QrCodeReader/templates/`:
- `base.html` - Base template
- `qr_generator.html` - QR code generation interface
- `qr_reader.html` - QR code reading interface
- Various static pages (about, privacy, etc.)

### URL Routing
Main URLs defined in `src/QrCodeReader/urls.py`:
- `/` - QR code generator (index)
- `/qrreader` - QR code reader
- `/qrgenerator` - QR code generator
- `/about` - About page
- `/privacy` - Privacy policy
- `/admin/` - Django admin interface

## Important Notes

- The application uses in-memory QR code generation (base64 encoded images) rather than saving files to disk
- QR code reading supports various image formats and includes error handling for corrupted/invalid images
- The codebase includes both web interface and command-line functionality for QR operations
- French language interface (`LANGUAGE_CODE = 'fr-fr'`)
- Production-ready settings with `DEBUG = False` and specific allowed hosts configured