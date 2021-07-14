# pco-services-display

### Clone the Repo
`git clone https://github.com/pastorhudson/pco-services-display.git`

### Change to Directory
`cd pco-services-display`

### Make Virtual Environment
`python3 -m venv ./venv`

### Activate Virtual Envionment
`source ./venv/bin/activate`

### Install Requirements
`pip install -r requirements.txt`

### Edit .env
Get Your api keys from https://api.planningcenteronline.com
```
PCO_APPLICATION_ID=
PCO_API_SECRET=
SERVICE_TYPE="Sunday Morning"
REPORT_TEMPLATE_ID=
```

### Run The Script
`python main.py`

### Windows Executable
Make sure the .env file is in the same directory as the exe
`get_report.exe`
