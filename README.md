# pco-services-display

This project will open a Planning Center Services Report for the current Sunda in a web browser to display on screen.
It is used to show on a display who is scheduled, and what position they are scheduled.


## Simple Usage
Download `get_report.exe` (Windows) OR `get_report`(Mac)
Download config.env

### Edit config.env
Get Your api keys from https://api.planningcenteronline.com
The Service type is the regular name of the Service Type.
The Report template id is the id number in the url when you run the report as html.
```
PCO_APPLICATION_ID=
PCO_API_SECRET=
SERVICE_TYPE="Sunday Morning"
REPORT_TEMPLATE_ID=
```

### Run
#### Windows
Ensure `config.env` and `get_report.exe` are in the same directory.
Run `get_report.exe`

#### Mac
Ensure `config.env` and `get_report` are in the same directory.
Run `get_report`
If it opens in txtedit then Downlod from the release or set the file to executable:
`chmod +x get_report`

## Developer Instructions
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

### Edit config.env
Get Your api keys from https://api.planningcenteronline.com
```
PCO_APPLICATION_ID=
PCO_API_SECRET=
SERVICE_TYPE="Sunday Morning"
REPORT_TEMPLATE_ID=
```

### Run The Script
`python main.py`
