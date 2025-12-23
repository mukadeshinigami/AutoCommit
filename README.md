# AutoCommit

Automated Git commit message generation using AI (Google Gemini).

## Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your Google Gemini API key:
```bash
export GOOGLE_API_KEY="your-api-key"
# or
export GEMINI_API_KEY="your-api-key"
```

## Usage

Basic usage:
```bash
python -m autocommit.cli
```

With options:
```bash
# Generate commit in English
python -m autocommit.cli --lang en

# Stage all files before analysis
python -m autocommit.cli --stage

# Show message only, don't commit
python -m autocommit.cli --no-commit

# Specify AI model
python -m autocommit.cli --model gemini-3-flash-preview
```

## Environment Variables

- `GOOGLE_API_KEY` or `GEMINI_API_KEY` - Google Gemini API key
- `AUTOCOMMIT_MODEL` - AI model (default: gemini-3-flash-preview)
- `AUTOCOMMIT_LANGUAGE` - Commit language (ru/en, default: ru)
- `AUTOCOMMIT_AUTO_STAGE` - Auto stage files (true/false)
- `AUTOCOMMIT_AUTO_COMMIT` - Auto commit without confirmation (true/false)
