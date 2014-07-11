import logging
from django.contrib.auth.models import User
from corehq import Domain
from corehq.apps.users.models import WebUser, CommCareUser, CouchUser, UserRole
from custom.api.utils import apply_updates
from custom.ilsgateway.api import ILSGatewayEndpoint
from corehq.apps.commtrack.models import Product
from dimagi.utils.dates import force_to_datetime
from custom.ilsgateway.models import MigrationCheckpoint
from requests.exceptions import ConnectionError
from datetime import datetime



def sync_ilsgateway_product(domain, ilsgateway_product):
    product = Product.get_by_code(domain, ilsgateway_product.sms_code)
    product_dict = {
        'domain': domain,
        'name':  ilsgateway_product.name,
        'code':  ilsgateway_product.sms_code,
        'unit': str(ilsgateway_product.units),
        'description': ilsgateway_product.description,
    }
    if product is None:
        product = Product(**product_dict)
        product.save()
    else:
        if apply_updates(product, product_dict):
            product.save()
    return product


def sync_ilsgateway_webusers(domain, ilsgateway_webuser):
    user = WebUser.get_by_username(ilsgateway_webuser.email.lower())
    user_dict = {
        'first_name': ilsgateway_webuser.first_name,
        'last_name': ilsgateway_webuser.last_name,
        'is_staff': ilsgateway_webuser.is_staff,
        'is_active': ilsgateway_webuser.is_active,
        'is_superuser': ilsgateway_webuser.is_superuser,
        'last_login': force_to_datetime(ilsgateway_webuser.last_login),
        'date_joined': force_to_datetime(ilsgateway_webuser.date_joined),
        #TODO Location and supply point
        #'location': ilsgateway_webuser.location,
        #'supply_point': ilsgateway_webuser.supply_point,
        'is_ilsuser': True,
    }

    role_id = ilsgateway_webuser.role_id if hasattr(ilsgateway_webuser, 'role_id') else None

    if user is None:
        try:
            user = WebUser.create(domain=None, username=ilsgateway_webuser.email.lower(),
                                  password=ilsgateway_webuser.password, email=ilsgateway_webuser.email, **user_dict)
            user.add_domain_membership(domain, role_id=role_id)
            user.save()
        except Exception as e:
            logging.error(e)
    else:
        if domain not in user.get_domains():
            user.add_domain_membership(domain, role_id=role_id)
            user.save()

    return user


def sync_ilsgateway_smsusers(domain, ilsgateway_smsuser):
    username_part = "%s%d" % (ilsgateway_smsuser.name.strip().replace(' ', '.').lower(), ilsgateway_smsuser.id)
    username = "%s@%s.commcarehq.org" % (username_part, domain)
    user = CouchUser.get_by_username(username)
    splitted_value = ilsgateway_smsuser.name.split(' ', 1)
    first_name = last_name = ''
    if splitted_value:
        first_name = splitted_value[0][:30]
        last_name = splitted_value[1][:30] if len(splitted_value) > 1 else ''

    user_dict = {
        'first_name': first_name,
        'last_name': last_name,
        'is_active': bool(ilsgateway_smsuser.is_active),
        'email': ilsgateway_smsuser.email
        #TODO location
    }

    if ilsgateway_smsuser.phone_numbers:
        user_dict['phone_numbers'] = [ilsgateway_smsuser.phone_numbers[0].replace('+', '')]
        user.user_data = {
            'backend': ilsgateway_smsuser.backend
        }

    if user is None and username_part:
        try:
            password = User.objects.make_random_password()
            user = CommCareUser.create(domain=domain, username=username, password=password,
                                       email=ilsgateway_smsuser.email, commit=False)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = bool(ilsgateway_smsuser.is_active)
            user.save()
        except Exception as e:
            logging.error(e)
    else:
        if apply_updates(user, user_dict):
            user.save()
    return user


def products_sync(domain, endpoint):
    for product in endpoint.get_products():
            sync_ilsgateway_product(domain, product)


def webusers_sync(project, endpoint):
    for user in endpoint.get_webusers():
        if user.email:
            if not user.is_superuser:
                setattr(user, 'role_id', UserRole.get_read_only_role_by_domain(project.name).get_id)
            sync_ilsgateway_webusers(project, user)

def smsusers_sync(project, endpoint):
    has_next = True
    next_url = None
    while has_next:
        next_url_params = next_url.split('?')[1] if next_url else None
        meta, users = endpoint.get_smsusers(next_url_params)
        for user in users:
            sync_ilsgateway_smsusers(project, user)

        if not meta['next']:
            has_next = False
        else:
            next_url = meta['next']


def bootstrap_domain(domain):
    project = Domain.get_by_name(domain)
    start_date = datetime.today()
    endpoint = ILSGatewayEndpoint.from_config(project.commtrack_settings.ilsgateway_config, project.name)
    try:
        products_sync(project.name, endpoint)
        webusers_sync(project.name, endpoint)
        smsusers_sync(project.name, endpoint)
        try:
            checkpoint = MigrationCheckpoint.objects.get(domain=project.name)
            checkpoint.date = start_date
            checkpoint.save()
        except MigrationCheckpoint.DoesNotExist:
            checkpoint = MigrationCheckpoint()
            checkpoint.domain = project.name
            checkpoint.date = start_date
            checkpoint.save()
    except ConnectionError as e:
        logging.error(e)