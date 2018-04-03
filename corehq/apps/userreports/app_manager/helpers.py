from __future__ import absolute_import
from __future__ import unicode_literals
from corehq.apps.app_manager.app_schemas.case_properties import get_case_properties
from corehq.apps.app_manager.xform import XForm
from corehq.apps.export.models import FormExportDataSchema
from corehq.apps.export.system_properties import BOTTOM_MAIN_FORM_TABLE_PROPERTIES
from corehq.apps.userreports.app_manager.data_source_meta import make_form_data_source_filter, \
    make_case_data_source_filter
from corehq.apps.userreports.models import DataSourceConfiguration
from corehq.apps.userreports.reports.builder import (
    DEFAULT_CASE_PROPERTY_DATATYPES,
    make_case_property_indicator,
)
from corehq.apps.userreports.sql import get_column_name
import unidecode


def get_case_data_sources(app):
    """
    Returns a dict mapping case types to DataSourceConfiguration objects that have
    the default set of case properties built in.
    """
    return {case_type: get_case_data_source(app, case_type) for case_type in app.get_case_types() if case_type}


def get_case_data_source(app, case_type):
    prop_map = get_case_properties(app, [case_type], defaults=list(DEFAULT_CASE_PROPERTY_DATATYPES))
    return DataSourceConfiguration(
        domain=app.domain,
        referenced_doc_type='CommCareCase',
        table_id=clean_table_name(app.domain, case_type),
        display_name=case_type,
        configured_filter=make_case_data_source_filter(case_type),
        configured_indicators=[
            make_case_property_indicator(property) for property in prop_map[case_type]
        ]
    )


def get_form_data_sources(app):
    """
    Returns a dict mapping forms to DataSourceConfiguration objects

    This is never used, except for testing that each form in an app will source correctly
    """
    forms = {}

    for module in app.modules:
        for form in module.forms:
            forms = {form.xmlns: get_form_data_source(app, form)}

    return forms


def get_form_data_source(app, form):
    xform = XForm(form.source)
    schema = FormExportDataSchema.generate_schema_from_builds(
        app.domain,
        app._id,
        xform.data_node.tag_xmlns,
        only_process_current_builds=True,
    )
    main_schema = schema.group_schemas[0]
    meta_properties = [_export_column_to_ucr_indicator(c) for c in BOTTOM_MAIN_FORM_TABLE_PROPERTIES]
    dynamic_properties = [_export_item_to_ucr_indicator(i) for i in main_schema.items]
    form_name = form.default_name()
    return DataSourceConfiguration(
        domain=app.domain,
        referenced_doc_type='XFormInstance',
        table_id=clean_table_name(app.domain, form_name),
        display_name=form_name,
        configured_filter=make_form_data_source_filter(xform.data_node.tag_xmlns),
        configured_indicators=meta_properties + dynamic_properties,
    )


def _export_column_to_ucr_indicator(export_column):
    """
    Converts an ExportColumn (from exports module) to a UCR indicator definition.
    :param export_column:
    :return: a dict ready to be inserted into a UCR data source
    """
    return {
        "type": "expression",
        "column_id": get_column_name(export_column.label),
        "display_name": export_column.label,
        "datatype": export_column.item.datatype or 'string',
        "expression": {
            "type": "property_path",
            'property_path': [p.name for p in export_column.item.path],
        }
    }


def _export_item_to_ucr_indicator(export_item):
    """
    Converts an ExportItem (from exports module) to a UCR indicator definition.
    :param export_item:
    :return: a dict ready to be inserted into a UCR data source
    """
    return {
        "type": "expression",
        "column_id": get_column_name(export_item.readable_path),
        "display_name": export_item.path[-1].name,
        "datatype": export_item.datatype or 'string',
        "expression": {
            "type": "property_path",
            'property_path': [p.name for p in export_item.path],
        }
    }


def clean_table_name(domain, readable_name):
    """
    Slugifies and truncates readable name to make a valid configurable report table name.
    """
    name_slug = '_'.join(unidecode.unidecode(readable_name).lower().split(' '))
    # 63 = max postgres table name, 24 = table name prefix + hash overhead
    max_length = 63 - len(domain) - 24
    return name_slug[:max_length]