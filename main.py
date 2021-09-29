import os

import pypco
from dotenv import load_dotenv
from datetime import datetime, timedelta
import webbrowser
import platform

load_dotenv('config.env')

"""Best practice is to store credentials in environment variables."""
pco = pypco.PCO(application_id=os.getenv('PCO_APPLICATION_ID'),
                secret=os.getenv('PCO_API_SECRET'))


def get_platform_date_format():
    """This is why we can't have nice things. Windows, and unix c libraries handle dates differently."""
    if platform.system() == 'Windows':
        return '%B %#d, %Y'
    elif platform.system() == 'Darwin' or platform.system() == "linux" or platform.system() == "linux2":
        return '%B %-d, %Y'


def get_service_type_id(service_name):
    """Takes a service type(string) and returns a service type id"""
    services = pco.iterate('/services/v2/service_types')
    for service in services:
        if service['data']['attributes']['name'] == service_name:
            return service['data']['id']


def get_latest_plan(service_type_id):
    """Takes a service type id and returns the next Sunday or today's plan if today is a Sunday"""
    plans = pco.iterate(
        f'/services/v2/service_types/{service_type_id}/plans?include=plan_times&order=sort_date&filter=future')
    for plan in plans:
        # print(f"API Date: {plan['data']['attributes']['dates']}\n"
        #       f"SUNDAY: {datetime.strftime(get_sunday(), get_platform_date_format())}\n"
        #       f"WEDNESDAY: {datetime.strftime(get_wednesday(), get_platform_date_format())}")

        if plan['data']['attributes']['dates'] == (datetime.strftime(get_sunday(), get_platform_date_format())):
            return plan['data']['id']

        if plan['data']['attributes']['dates'] == (datetime.strftime(get_wednesday(), get_platform_date_format())):
            return plan['data']['id']


def get_sunday():
    """Returns the next sunday or today if it is sunday"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if today.weekday() < 6:
        sunday = today + timedelta(days=6 - today.weekday())
        return sunday
    elif today.weekday() == 6:
        return today


def get_wednesday():
    """Returns the next wednesday or today if it is wednesday"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if today.weekday() < 2:
        wednesday = today + timedelta(days=2 - today.weekday())
        return wednesday
    elif today.weekday() > 2:
        wednesday = today + timedelta(days=9 - today.weekday())
        return wednesday
    elif today.weekday() == 2:
        return today


def get_url():
    """This brings everything together and returns the url."""
    service_type_id = get_service_type_id(os.getenv('SERVICE_TYPE'))
    plan_id = get_latest_plan(service_type_id)
    report_template_id = os.getenv('REPORT_TEMPLATE_ID')
    url = f"https://services.planningcenteronline.com/report_templates/{report_template_id}/report.html?plan_id={plan_id}"
    return url


def open_url(url):
    """Open's the default browser to the report url. This could be exteded to use solenium or a system command
    to make the browser go into fullscreen or kiosk mode."""
    webbrowser.open(url, new=0)


if __name__ == "__main__":
    url = get_url()
    print(url)
    open_url(url)
