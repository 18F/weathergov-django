from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()

# Renders the partial for the daily high/low information
@register.inclusion_tag("weather/partials/daily-high-low.html")
def daily_high_low(**kwargs):
    periods = kwargs['periods']
    temps = [period['data']['temperature']['degF'] for period in periods]
    low = min(temps)
    high = max(temps)

    # We show the high and/or low
    # based on the periods and
    # whether there are several or only
    # a daytime period
    show_high = False
    show_low = False
    if len(periods) > 1 or periods[0]['isDaytime']:
        show_high = True
    if len(periods) > 1 or not periods[0]['isDaytime']:
        show_low = True

    return {
        'high': high,
        'low': low,
        'show_high': show_high,
        'show_low': show_low
    }

# Renders the alert link in the daily summary
@register.inclusion_tag("weather/partials/alert-link.html")
def alert_link(**kwargs):
    alerts = kwargs['alerts']
    num_alerts = alerts['metadata']['count']
    alert_id = None
    alert_type = None
    alert_level = None
    if num_alerts == 0:
        return {}
    elif num_alerts > 1:
        alert_id = alerts['items'][0]['id']
        alert_type = alerts['items'][0]['event']
        alert_level = alerts['items'][0]['level']
    else:
        alert_type = _("daily-forecast.labels.multiple-alerts.01")
        alert_level = alerts['metadata']['highest']

    return {
        'alertID': alert_id,
        'alertType': alert_type,
        'alertLevel': alert_level,
        'alertCount': num_alerts
    }

# Renders a daily summary list item
# for a given day
@register.inclusion_tag("weather/partials/daily-summary-list-item.html")
def daily_summary_list_item(**kwargs):
    day = kwargs['day']
    day_label = kwargs.get("dayLabel", day["periods"][0]["dayName"])
    day_hours = day['hours']
    item_id = kwargs.get("itemId", None)
    alerts = day["alerts"]

    # We need to ensure there is always an item id
    # for use by the element. If one is not provided,
    # this is the default that we use
    if not item_id:
        item_id = day["periods"][0]["monthAndDay"].lower().replace(" ", "-")

    # Map data for the chart
    times = [hour['hour'] for hour in day_hours]
    temps = [hour['temperature']['degF'] for hour in day_hours]
    feels_like = [hour['apparentTemperature']['degF'] for hour in day_hours]

    return {
        'day': day,
        'dayLabel': day_label,
        'dayHours': day_hours,
        'itemId': item_id,
        'alerts': alerts,
        'times': times,
        'temps': temps,
        'feelsLike': feels_like
    }

# Renders a wind speed and direction arrow
@register.inclusion_tag("weather/partials/wind.html")
def wind_speed_direction(**kwargs):
    speed = kwargs["speed"]
    direction = kwargs["direction"]
    has_direction = direction["cardinalLong"] != None
    direction_name =  ""
    if has_direction:
        direction_name = direction["cardinalLong"].lower()

    # Get the name of the directional i18n message
    msg_name = f"wind.labels.speed-from-{direction_name}"
    sr_content = _(msg_name).format({'speed': speed})

    return {
        'speed': speed,
        'direction': direction,
        'sr_content': sr_content,
        'has_direction': has_direction
    }

# Renders the radar
@register.inclusion_tag("weather/partials/radar.html")
def radar(**kwargs):
    INTENSITIES = [{
        "dbz": "−35–0",
        "description": "Extremely light (drizzle/snow)",
        "gradient": "180deg, #8E827E 0%, #969155 17.64%, #A5A36D 27.53%, #D0D2B2 54.47%, #7E8BAF 100%"
        },{
        "dbz": "0–20",
        "description": "Very light precipitation or general clutter",
        "gradient": "180deg, #7B88AE 0%, #5C71A6 17.64%, #445FA0 36.39%, #5DA9CC 61.25%, #59C0BA 73.2%, #52D6A2 87.85%, #3FD657 100%"
        },{
        "dbz": "20–40",
        "description": "Light precipitation",
        "gradient": "180deg, #3FD657 0%, #3ED624 9.47%, #24890E 36.39%, #176108 61.25%, #819F06 73.2%, #FBE000 85.5%, #F4CB17 100%"
        },{
        "dbz": "40–50",
        "description": "Moderate precipitation",
        "gradient": "180deg, #F4CB17 0%, #EBB32D 25.38%, #F9B103 72.13%, #F52D04 73.91%, #D10808 99.72%"
        },{
        "dbz": "50–65",
        "description": "Heavy precipitation or some hail",
        "gradient": "180deg, #D10808 0%, #A20F10 16.84%, #B00301 48.32%, #FEFBFF 49.94%, #EDA7FD 71.83%, #E474FC 83.75%, #F174FD 100%);"
        },{
        "dbz": ">65",
        "description": "Extremely heavy precipitation including water-coated hail",
        "gradient": "180deg, #F174FD 0%, #F875FF 30.26%, #AA0BFA 34%, #5B06D3 98.5%"
        }]
    place = kwargs["place"]
    point = kwargs["point"]

    return {
        'place': place,
        'point': point,
        'intensities': INTENSITIES
    }
    
