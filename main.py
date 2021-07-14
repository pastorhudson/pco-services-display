import os

import pypco
from dotenv import load_dotenv
from datetime import datetime, timedelta
import webbrowser

load_dotenv('.env')


"""Best practice is to store credentials in environment variables."""
pco = pypco.PCO(application_id=os.getenv('PCO_APPLICATION_ID'),
                secret=os.getenv('PCO_API_SECRET'))


def get_service_type_id(service_name):
    services = pco.iterate('/services/v2/service_types')
    for service in services:
        if service['data']['attributes']['name'] == service_name:
            # print(f"{service['data']['attributes']['name']} - {service['data']['id']}")
            return service['data']['id']


def get_latest_plan(service_type_id):
    plans = pco.iterate(f'/services/v2/service_types/{service_type_id}/plans?include=plan_times&order=sort_date&filter=future')
    for plan in plans:
        if plan['data']['attributes']['dates'] == (datetime.strftime(get_sunday(), '%B %d, %Y')):
            # print(plan['data']['attributes']['dates'])
            return plan['data']['id']


def get_url():
    service_type_id = get_service_type_id(os.getenv('SERVICE_TYPE'))
    plan_id = get_latest_plan(service_type_id)
    report_template_id = os.getenv('REPORT_TEMPLATE_ID')
    url = f"https://services.planningcenteronline.com/report_templates/{report_template_id}/report.html?plan_id={plan_id}"
    print(url)
    open_url(url)


def get_sunday():
    """Returns the next sunday or today if it is sunday"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if today.weekday() < 6:
        sunday = today + timedelta(days=6 - today.weekday())
        return sunday
    elif today.weekday() == 6:
        return today


def open_url(url):
    webbrowser.open(url)


if __name__ == "__main__":
    get_url()