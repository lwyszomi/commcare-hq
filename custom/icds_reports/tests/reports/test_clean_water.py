from __future__ import absolute_import

from django.test.utils import override_settings

from custom.icds_reports.reports.clean_water import get_clean_water_data_map, get_clean_water_data_chart, \
    get_clean_water_sector_data
from django.test import TestCase


@override_settings(SERVER_ENVIRONMENT='icds')
class TestCleanWater(TestCase):

    def test_map_data(self):
        self.assertDictEqual(
            get_clean_water_data_map(
                'icds-cas',
                config={
                    'month': (2017, 5, 1),
                    'aggregation_level': 1
                },
                loc_level='state'
            )[0],
            {
                "rightLegend": {
                    "info": "Percentage of AWCs that reported having a source of clean drinking water",
                    "average": 96.66666666666667
                },
                "label": "Percentage of AWCs that reported having a source of clean drinking water",
                "data": {
                    "st1": {
                        "in_month": 17,
                        "original_name": [],
                        "all": 17,
                        "fillKey": "75%-100%"
                    },
                    "st2": {
                        "in_month": 12,
                        "original_name": [],
                        "all": 13,
                        "fillKey": "75%-100%"
                    }
                },
                "slug": "clean_water",
                "fills": {
                    "0%-25%": "#de2d26",
                    "25%-75%": "#fc9272",
                    "75%-100%": "#fee0d2",
                    "defaultFill": "#9D9D9D"
                }
            }
        )

    def test_map_name_is_different_data(self):
        self.assertDictEqual(
            get_clean_water_data_map(
                'icds-cas',
                config={
                    'month': (2017, 5, 1),
                    'state_id': 'st1',
                    'district_id': 'd1',
                    'aggregation_level': 3
                },
                loc_level='block',
            )[0],
            {
                "rightLegend": {
                    "info": "Percentage of AWCs that reported having a source of clean drinking water",
                    "average": 100.0
                },
                "label": "Percentage of AWCs that reported having a source of clean drinking water",
                "data": {
                    "block_map": {
                        "in_month": 17,
                        "original_name": [
                            "b1",
                            "b2"
                        ],
                        "all": 17,
                        "fillKey": "75%-100%"
                    }
                },
                "slug": "clean_water",
                "fills": {
                    "0%-25%": "#de2d26",
                    "25%-75%": "#fc9272",
                    "75%-100%": "#fee0d2",
                    "defaultFill": "#9D9D9D"
                }
            }
        )

    def test_chart_data(self):
        self.assertDictEqual(
            get_clean_water_data_chart(
                'icds-cas',
                config={
                    'month': (2017, 5, 1),
                    'aggregation_level': 1
                },
                loc_level='state'
            ),
            {
                "chart_data": [
                    {
                        "color": "#005ebd",
                        "values": [
                            {
                                "y": 0.0,
                                "x": 1485907200000,
                                "in_month": 0
                            },
                            {
                                "y": 0.0,
                                "x": 1488326400000,
                                "in_month": 0
                            },
                            {
                                "y": 1.0,
                                "x": 1491004800000,
                                "in_month": 14
                            },
                            {
                                "y": 0.9666666666666667,
                                "x": 1493596800000,
                                "in_month": 29
                            }
                        ],
                        "strokeWidth": 2,
                        "classed": "dashed",
                        "key": "Percentage of AWCs that reported having a source of clean drinking water"
                    }
                ],
                "top_five": [
                    {
                        "loc_name": "st1",
                        "percent": 100.0
                    },
                    {
                        "loc_name": "st2",
                        "percent": 92.3076923076923
                    }
                ],
                "location_type": "State",
                "all_locations": [
                    {
                        "loc_name": "st1",
                        "percent": 100.0
                    },
                    {
                        "loc_name": "st2",
                        "percent": 92.3076923076923
                    }
                ],
                "bottom_five": [
                    {
                        "loc_name": "st1",
                        "percent": 100.0
                    },
                    {
                        "loc_name": "st2",
                        "percent": 92.3076923076923
                    }
                ]
            }
        )

    def test_sector_data(self):
        self.assertDictEqual(
            get_clean_water_sector_data(
                'icds-cas',
                config={
                    'month': (2017, 5, 1),
                    'state_id': 'st1',
                    'district_id': 'd1',
                    'block_id': 'b1',
                    'aggregation_level': 4
                },
                location_id='b1',
                loc_level='supervisor'
            ),
            {
                "info": "Percentage of AWCs that reported having a source of clean drinking water",
                "tooltips_data": {
                    "s2": {
                        "in_month": 3,
                        "all": 3
                    },
                    "s1": {
                        "in_month": 5,
                        "all": 5
                    }
                },
                "chart_data": [
                    {
                        "color": "#006fdf",
                        "values": [
                            [
                                "s1",
                                1.0
                            ],
                            [
                                "s2",
                                1.0
                            ]
                        ],
                        "strokeWidth": 2,
                        "classed": "dashed",
                        "key": ""
                    }
                ]
            }
        )
