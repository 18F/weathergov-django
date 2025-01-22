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
@register.inclusion_tag("weather/daily-summary-list-item.html")
def daily_summary_list_item(**kwargs):
    today = kwargs['today']
    day_label = kwargs.get("dayLabel", "")
    day_hours = today['hours']
    item_id = kwargs.get("itemId", None)

    # We need to ensure there is always an item id
    # for use by the element. If one is not provided,
    # this is the default that we use
    if not item_id:
        item_id = today["periods"][0]["monthAndDay"].lower().replace(" ", "-")

# Renders a wind speed and direction arrow
@register.inclusion_tag("weather/partials/wind.html")
def wind_speed_direction(**kwargs):
    speed = kwargs["speed"]
    direction = kwargs["direction"]

    # Get the name of the directional i18n message
    msg_name = f"wind.labels.speed-from-{direction['cardinalLong'].lower()}"
    sr_content = _(msg_name).format({'speed': speed})

    return {
        'speed': speed,
        'direction': direction,
        'sr_content': sr_content
    }
    

    
    
    
