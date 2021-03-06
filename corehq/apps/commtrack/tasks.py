from __future__ import absolute_import
from __future__ import unicode_literals
from celery.task import task
from corehq.apps.commtrack.consumption import recalculate_domain_consumption


@task(serializer='pickle', ignore_result=True)
def recalculate_domain_consumption_task(domain):
    recalculate_domain_consumption(domain)
