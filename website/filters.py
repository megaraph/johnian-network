import cloudinary
import json
import datetime
from flask import current_app
from cloudinary import utils


def humanize_time(date_posted, time_now):
    date_comp = date_posted.strftime("%b %d, %Y")
    date_no_year = date_posted.strftime("%b %d")
    diff = (time_now - date_posted).total_seconds()

    if diff < 1 or diff == 1:
        return '1s'
    elif diff < 60:
        return f'{int(round(diff))}s'
    elif int(round(diff//60)) == 1:
        return '1m'
    elif diff > 60 and diff < 3600:
        return f'{int(round(diff // 60)) }m'
    elif int(round(diff//3600)) == 1:
        return '1h'
    elif diff > 3600 and diff < 86400:
        return f'{ int(round(diff // 3600)) }h'
    elif int(round(diff/86400)) == 1:
        return '1d'
    elif int(round(diff/86400)) >= 2 and int(round(diff/86400)) < 30:
        return f'{int(round(diff // 86400))}d'
    elif int(round((diff/86400))) == 30 or int(round(((diff/86400))) >= 30 and int(round((diff/86400))) < 365):
        return date_no_year
    elif int(round(diff/86400)) == 365 or int(round(diff/86400)) >= 365:
        return date_comp
    else:
        return 'Posted ... ago'


def get_cloud_file(image_str):
    image_dict = json.loads(image_str)
    id = image_dict.get('id')
    extension = image_dict.get('ext')
    resource_type = image_dict.get('resource_type')
    return utils.cloudinary_url(f'{id}.{extension}', resource_type=resource_type)[0]
