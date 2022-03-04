# pco-services-display

This project will open a Planning Center Services Report for the current Sunda in a web browser to display on screen.
It is used to show on a display who is scheduled, and what position they are scheduled.


## Getting Started

### Binaries (Command Line)

The following binaries with their corresponding checksums are included in this repository for your convenience. It is strongly RECOMMENDED that you verify their checksums before use.

| Platform | Command Line Program       | Checksum (SHA256) |
|----------|----------------------------|-----------|
| Windows  | get_report.exe             | f365f156eafc9754f1b82062735cae7801fe4218         |
| Mac OS   | get_report                 | bdd87d7c10aebba095703ba0420d98efb18495adbd745c868a730039eb047639 |


To verify the above checksums on your platform, use the corresponding command below to verify their match:
- On Windows, run: `CertUtil -hashfile 'path\to\bin\windows\get_report.exe' sha256`
- On Mac OS, run: `shasum -a 256 path/to/get_report` or `sha256sum path/to/get_report`

Alternatively, you can also build these binaries from source using the scripts found in the *release/* folder.

See also [Developer Instructions](#developer-instructions) below for running the main script directly.

### Editing config.env
Template:
```
PCO_APPLICATION_ID=
PCO_API_SECRET=
SERVICE_TYPE="Sunday Morning"
REPORT_TEMPLATE_ID=
```

Edit settings in this file (**config.env**) as follows:
- `PCO_APPLICATION_ID`, `PCO_API_SECRET` - Get your API credentials from https://api.planningcenteronline.com
- `SERVICE_TYPE` - The regular name of the Service Type (i.e. "Sunday Morning")
- `REPORT_TEMPLATE_ID` - The ID number in the URL when you run the report as HTML

### Run
**Important.** Before running the program:
- Please ensure both **config.env** and the command line program for your platform are in the *same* directory
- (Mac OS users only) Please ensure `get_report` is executable by running `chmod +x ./get_report`

Once configured, simply run the command line program: `get_report.exe` (Windows) or `./get_report` (Mac OS)

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
Get your API keys from https://api.planningcenteronline.com
```
PCO_APPLICATION_ID=
PCO_API_SECRET=
SERVICE_TYPE="Sunday Morning"
REPORT_TEMPLATE_ID=
```

### Run The Script
`python main.py`

## Executable Build Instructions
From within your dev virtual environment

###Install pyinstaller
On Windows or Latest Mac: `pip install pyinstaller`
On Older Mac: `pip install pyinstaller==4.3`

###Run build script:
- `cd release`
- On Windows, run: 'package_executable_windows.bat'
- On Mac OS, run: 'package_executable_mac.sh'
- The respective binary will be added to the project directory.