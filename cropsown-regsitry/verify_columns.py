import re

db_columns = [
    'history_record_id', 'internal_record_id', 'tab_id', 'section_id', 'change_request_id', 'submission_id', 'change_request_source', 'is_primary_section', 'functional_record_id', 'link_internal_record_id', 'link_foundational_id', 'record_name', 'record_image_document_id', 'record_status', 'record_status_reason', 'created_by', 'created_at', 'approved_by', 'approved_at', 'latitude', 'longitude', 'altitude', 'plus_code', 'address_line_1', 'address_line_2', 'postal_code', 'country_code', 'geo_lowest_level_value_id', 'geo_code_hierarchy_json', 'land_id', 'is_land_registered', 'land_area', 'cluster_name', 'agro_ecological_zone', 'season', 'cluster_area_hectare', 'number_of_smallholders', 'collected_land', 'collected_quintal', 'water_source', 'is_plot_not_registered', 'temporary_land_id', 'sync_id', 'start_gc', 'start_month', 'start_day', 'end_gc', 'end_month', 'end_day', 'cluster_id', 'cluster_area_timad', 'gps_location', 'cluster_plan', 'cluster_collected_land', 'collected_by_combiner', 'actual_cluster_plan', 'actual_cluster_collected_land', 'actual_cluster_collected_quintal', 'actual_cluster_participant_farmers', 'actual_collected_land', 'actual_collected_land_quintal', 'actual_collected_by_combiner', 'is_actual', 'da_name', 'da_mobile_number', 'supervisor_name', 'supervisor_mobile_number', 'water_source_method', 'water_source_frequency'
]

cluster_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/register_domain/models/cluster.py"
with open(cluster_file, 'r') as f:
    cluster_py = f.read()

model_fields = re.findall(r"    ([a-zA-Z0-9_]+): Mapped\[", cluster_py)

missing_in_db = set(model_fields) - set(db_columns)
print("Fields in model but missing in DB:", missing_in_db)
