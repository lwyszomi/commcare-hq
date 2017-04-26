from sqlagg.base import AggregateColumn, AliasColumn
from sqlagg.columns import SimpleColumn, SumColumn
from sqlagg.filters import EQ

from corehq.apps.reports.datatables import DataTablesColumn
from corehq.apps.reports.datatables import DataTablesHeader
from corehq.apps.reports.sqlreport import SqlData, DatabaseColumn
from corehq.util.quickcache import quickcache
from custom.icds_reports.utils import ICDSMixin


class BaseIdentification(object):

    title = 'a. Identification'
    slug = 'identification'
    has_sections = False
    subtitle = []
    posttitle = None

    def __init__(self, config):
        self.config = config

    @property
    def headers(self):
        return DataTablesHeader(
            DataTablesColumn('', sortable=False),
            DataTablesColumn('Name', sortable=False),
            DataTablesColumn('Code', sortable=False)
        )


class BaseOperationalization(ICDSMixin):

    title = 'c. Status of operationalization of AWCs'
    slug = 'operationalization'

    @property
    def headers(self):
        return DataTablesHeader(
            DataTablesColumn('', sortable=False),
            DataTablesColumn('Sanctioned', sortable=False),
            DataTablesColumn('Functioning', sortable=False),
            DataTablesColumn('Reporting', sortable=False)
        )

    @property
    def rows(self):
        if self.config['location_id']:
            data = self.custom_data(selected_location=self.selected_location, domain=self.config['domain'])
            return [
                [
                    'No. of AWCs',
                    self.awc_number,
                    0,
                    data['owner_id']
                ],
                [
                    'No. of Mini AWCs',
                    0,
                    0,
                    0
                ]
            ]


class BasePopulation(ICDSMixin):

    slug = 'population'

    def __init__(self, config):
        super(BasePopulation, self).__init__(config)
        self.config.update(dict(
            location_id=config['location_id']
        ))

    @property
    def headers(self):
        return []

    @property
    def rows(self):
        if self.config['location_id']:
            data = self.custom_data(selected_location=self.selected_location, domain=self.config['domain'])
            return [
                [
                    "Total Population of the project:",
                    data['open_count']
                ]
            ]


class StateData(SqlData):
    table_name = "agg_child_health_monthly"
    filters = [
        EQ('aggregation_level', 'aggregation_level')
    ]
    group_by = ['state_name', 'state_id']

    @property
    def columns(self):
        return [
            DatabaseColumn('State Id', SimpleColumn('state_id')),
            DatabaseColumn('State Name', SimpleColumn('state_name'))
        ]

    @property
    @quickcache([])
    def data(self):
        return super(StateData, self).data
