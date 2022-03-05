import os

import pypco
from dotenv import load_dotenv
from datetime import datetime, timedelta
import webbrowser
import platform
from pypco import PCORequestException
import logging
logging.basicConfig(level=logging.DEBUG, force=True, format = "%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler("Log.txt"),
                              logging.StreamHandler()
                              ]
                    )

logger = logging.getLogger(__name__)


load_dotenv('config.env')

"""Best practice is to store credentials in environment variables."""
pco = pypco.PCO(application_id=os.getenv('PCO_APPLICATION_ID'),
                secret=os.getenv('PCO_API_SECRET'))


def get_platform_date_format():
    """This is why we can't have nice things. Windows, and unix c libraries handle dates differently."""
    if platform.system() == 'Windows':
        return '%B %#d, %Y'
    elif platform.system() == 'Darwin' or platform.system() == "Linux":
        return '%B %-d, %Y'


def get_service_type_id(service_name):
    """Takes a service type(string) and returns a service type id"""
    services = pco.iterate('/services/v2/service_types')
    for service in services:
        if service['data']['attributes']['name'] == service_name:
            return service['data']['id']
    logger.error(f'No Service ID for {service_name} found.')


def get_latest_plan(service_type_id):
    """Takes a service type id and returns the next Sunday or today's plan if today is a Sunday"""
    """
    https://api.planningcenteronline.com/services/v2/service_types/173868/plans?include=plan_times&order=sort_date&where[updated_at][gte]=2022-1-1
    """
    back_date = datetime.now() - timedelta(weeks=int(os.getenv('LOOK_BACK_WEEKS')))
    logger.info(f"Looking for Sunday: {datetime.strftime(get_sunday(), get_platform_date_format())} or "
                f"Wednesday: {datetime.strftime(get_wednesday(), get_platform_date_format())}")
    try:
        plans = pco.iterate(
            f'/services/v2/service_types/{service_type_id}/plans?include=plan_times&order=sort_date&where[created_at][gte]='
            f'{datetime.strftime(back_date, "%Y-%m-%d")}'
        )
    except PCORequestException:
        logger.error(f"Unable to find Service Type")

    for plan in plans:
        logger.debug(f"API Date: {plan['data']['attributes']['dates']} "
              f"SUNDAY: {datetime.strftime(get_sunday(), get_platform_date_format())} "
              f"WEDNESDAY: {datetime.strftime(get_wednesday(), get_platform_date_format())}")
        logger.debug(plan['data']['attributes']['dates'])
        if plan['data']['attributes']['dates'] == (datetime.strftime(get_sunday(), get_platform_date_format())):
            logger.info("Found Sunday plan id")
            return plan['data']['id']

        if plan['data']['attributes']['dates'] == (datetime.strftime(get_wednesday(), get_platform_date_format())):
            logger.info("Found wednesday id")
            return plan['data']['id']
    logger.info(f'No Plan ID Found for \n'
                f'Sunday: {datetime.strftime(get_sunday(), get_platform_date_format())}\n'
                f'Wednesday:{datetime.strftime(get_wednesday(), get_platform_date_format())}')


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
    try:
        logger.info(os.getenv('SERVICE_TYPE'))
        service_type_id = get_service_type_id(os.getenv('SERVICE_TYPE'))
        plan_id = get_latest_plan(service_type_id)
        report_template_id = os.getenv('REPORT_TEMPLATE_ID')
        url = f"https://services.planningcenteronline.com/report_templates/{report_template_id}/report.html?plan_id={plan_id}"
        return url
    except PCORequestException:
        # logger.error(PCORequestException)
        pass


def open_url(url):
    """Open's the default browser to the report url. This could be exteded to use solenium or a system command
    to make the browser go into fullscreen or kiosk mode."""
    webbrowser.open(url, new=0)


def check_config():
    logger.info("Checking Service Type: ")
    if os.getenv('SERVICE_TYPE'):
        logger.info(f'OK {os.getenv("SERVICE_TYPE")}\n')
    else:
        logger.error('SERVICE_TYPE NOT FOUND\n')
    logger.info("Report Template ID: ")
    if os.getenv('REPORT_TEMPLATE_ID'):
        logger.info(f'OK {os.getenv("REPORT_TEMPLATE_ID")}\n')
    else:
        logger.error('REPORT_TEMPLATE_ID NOT FOUND\n')
    logger.info("Checking API KEYS: ")
    if os.getenv("PCO_API_SECRET"):
        logger.info("API SECRET FOUND")
    else:
        logger.info("PCO_API_SECRET Not Found\n")
    if os.getenv("PCO_APPLICATION_ID"):
        logger.info("API APPLICATION ID Found\n")
    else:
        logger.error("API_APPLICATION_ID Not Found\n")
    logger.info("TESTING KEY PAIR:")
    try:
        services = pco.get('/services/v2/')
        logger.info("API KEYS ARE GOOD\n")

    except PCORequestException:
        logger.error("API KEYS BAD")


if __name__ == "__main__":
    check_config()
    url = get_url()
    if url:
        logger.info(url)
        open_url(url)

