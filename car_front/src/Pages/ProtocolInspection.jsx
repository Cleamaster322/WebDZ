import {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import api from "../shared/api.jsx";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";

import ProtocolInspectionHeader from "../Features/ProtocolInspection/ProtocolInspectionHeader.jsx";
import ProtocolInspectionConditions from "../Features/ProtocolInspection/ProtocolInspectionConditions.jsx";
import ProtocolInspectionPhotos from "../Features/ProtocolInspection/ProtocolInspectionPhotos.jsx";
import ProtocolInspectionVehicle from "../Features/ProtocolInspection/ProtocolInspectionVehicle.jsx";
import ProtocolInspectionEngine from "../Features/ProtocolInspection/ProtocolInspectionEngine.jsx";
import ProtocolInspectionSteeringTransmission
    from "../Features/ProtocolInspection/ProtocolInspectionSteeringTransmission.jsx";
import ProtocolInspectionBrakes from "../Features/ProtocolInspection/ProtocolInspectionBrakes.jsx";
import ProtocolInspectionLightsMain from "../Features/ProtocolInspection/ProtocolInspectionLightsMain.jsx";
import ProtocolInspectionLightsGeometry from "../Features/ProtocolInspection/ProtocolInspectionLightsGeometry.jsx";
import ProtocolInspectionMisc from "../Features/ProtocolInspection/ProtocolInspectionMisc.jsx";

import {
    pageSx,
    pageInnerSx,
    sectionPaperSx,
    sectionTitleSx,
    subsectionTitleSx,
    textFieldSx,
    selectFieldSx,
} from "../Features/ProtocolInspection/protocolInspectionStyles.jsx";

const initialForm = {
    appendix_number: "",
    appendix_date_day: "",
    appendix_date_month: "",
    appendix_date_year: "",

    ambient_temp_c: "",
    ambient_humidity_pct: "",
    atmospheric_pressure_kpa: "",
    road_ambient_temp_c: "",
    road_ambient_humidity_pct: "",
    electric_frequency_hz: "",
    voltage_phase_a_zero: "",
    voltage_phase_b_zero: "",
    voltage_phase_c_zero: "",
    voltage_phase_ab: "",
    voltage_phase_bc: "",
    voltage_phase_ac: "",

    photos_comment: "",

    brand_name: "",
    commercial_name: "",
    vin: "",
    category: "",
    body_type: "",
    mileage_km: "",
    tire_marking_front: "",
    tire_marking_rear: "",
    tire_season: "",
    tire_spikes_present: "",
    manufacture_year: "",
    color: "",
    wheel_formula: "",
    mufflers_count: "",
    seats_count: "",
    side_steps_present: "",

    engine_model: "",
    engine_power_kw: "",
    engine_layout: "",
    cylinder_layout: "",
    cylinders_count: "",
    fuel_type: "",
    turbo_present: "",

    steering_booster_type: "",
    transmission_type: "",

    service_brake_type: "",
    parking_brake_type: "",
    service_brake_control_force_axle1_n: "",
    service_brake_control_force_axle2_n: "",
    parking_brake_control_force_n: "",
    axle_1_brake_difference_pct: "",
    axle_2_brake_difference_pct: "",
    service_brake_front_left_kn: "",
    service_brake_front_right_kn: "",
    service_brake_rear_left_kn: "",
    service_brake_rear_right_kn: "",
    parking_brake_left_kn: "",
    parking_brake_right_kn: "",
    stand_axle1_load_kg: "",
    stand_axle2_load_kg: "",

    low_beam_count: "",
    low_beam_color: "",
    high_beam_count: "",
    high_beam_color: "",
    front_fog_count: "",
    front_fog_color: "",
    reverse_light_count: "",
    reverse_light_color: "",
    turn_signal_count: "",
    turn_signal_color: "",
    front_position_light_count: "",
    front_position_light_color: "",
    rear_position_light_count: "",
    rear_position_light_color: "",
    main_brake_signal_count: "",
    main_brake_signal_color: "",
    additional_brake_signal_count: "",
    additional_brake_signal_color: "",
    rear_fog_count: "",
    rear_fog_color: "",
    plate_light_count: "",
    plate_light_color: "",
    daytime_running_light_count: "",
    daytime_running_light_color: "",

    parking_light_count: "",
    parking_light_color: "",
    rear_parking_light_count: "",
    rear_parking_light_color: "",
    adaptive_front_lighting_count: "",
    adaptive_front_lighting_color: "",

    headlight_type: "",
    headlight_washer_present: "",
    left_34v_cd: "",
    left_52h_cd: "",
    left_high_beam_cd: "",
    right_34v_cd: "",
    right_52h_cd: "",
    right_high_beam_cd: "",
    turn_signal_frequency_per_min: "",
    turn_signal_frequency_hz: "",

    low_beam_upper_point_mm: "",
    low_beam_lower_point_mm: "",
    fog_light_upper_point_mm: "",
    fog_light_lower_point_mm: "",
    fog_light_left_distance_mm: "",
    fog_light_right_distance_mm: "",
    brake_signal_upper_point_mm: "",
    brake_signal_lower_point_mm: "",
    brake_signal_left_distance_mm: "",
    brake_signal_right_distance_mm: "",
    additional_brake_signal_from_glass_edge_mm: "",
    additional_brake_signal_from_support_surface_mm: "",
    additional_brake_signal_optical_center_shift_mm: "",
    rear_fog_upper_point_mm: "",
    rear_fog_lower_point_mm: "",

    spare_wheel_present: "",
    steering_lock_present: "",
    gas_equipment_present: "",

    tire_depth_fl_mm: "",
    tire_depth_rl_mm: "",
    tire_depth_fr_mm: "",
    tire_depth_rr_mm: "",
    bumper_ends_bent_to_body: "",
    bumper_to_body_distance_mm: "",
    opening_roof_present: "",
    fuel_leak_prevention_measure: "",
    protruding_elements_doors_mm: "",
    protruding_elements_other_mm: "",
    glass_transparency_right_pct: "",
    glass_transparency_left_pct: "",
    glass_transparency_windshield_pct: "",
    sun_strip_width_mm: "",
    steering_backlash_deg: "",
    speed_by_speedometer_kmh: "",
    actual_speed_kmh: "",
    exhaust_noise_constant_db: "",
    exhaust_noise_deceleration_db: "",
    co_min_pct: "",
    co_max_pct: "",
    light_absorption_1: "",
    light_absorption_2: "",
    light_absorption_3: "",
    light_absorption_4: "",
    light_absorption_5: "",
    light_absorption_6: "",
    vehicle_length_mm: "",
    vehicle_width_mm: "",
    vehicle_height_mm: "",
    vehicle_weight_kg: "",
    axle1_load_kg: "",
    axle2_load_kg: "",
};

function toFormValue(value) {
    return value === null || value === undefined ? "" : value;
}

function booleanToSelect(value) {
    if (value === true) return "true";
    if (value === false) return "false";
    return "";
}

function emptyToNull(value) {
    return value === "" ? null : value;
}

function stringToBooleanOrNull(value) {
    if (value === "true") return true;
    if (value === "false") return false;
    return null;
}

function mapProtocolToForm(data) {
    const protocol = data || {};
    const measurement = protocol.measurement || {};
    const brake = protocol.brake || {};
    const light = protocol.light || {};
    const testConditions = protocol.test_conditions || {};
    const roadConditions = protocol.road_conditions || {};
    const powerSupply = protocol.power_supply || {};

    return {
        ...initialForm,

        appendix_number: toFormValue(protocol.appendix_number),

        ambient_temp_c: toFormValue(testConditions.ambient_temperature_c),
        ambient_humidity_pct: toFormValue(testConditions.relative_humidity_pct),
        atmospheric_pressure_kpa: toFormValue(testConditions.atmospheric_pressure_kpa),

        road_ambient_temp_c: toFormValue(roadConditions.road_ambient_temperature_c),
        road_ambient_humidity_pct: toFormValue(roadConditions.road_relative_humidity_pct),

        electric_frequency_hz: toFormValue(powerSupply.frequency_hz),
        voltage_phase_a_zero: toFormValue(powerSupply.phase_a_n_voltage_v),
        voltage_phase_b_zero: toFormValue(powerSupply.phase_b_n_voltage_v),
        voltage_phase_c_zero: toFormValue(powerSupply.phase_c_n_voltage_v),
        voltage_phase_ab: toFormValue(powerSupply.phase_ab_voltage_v),
        voltage_phase_bc: toFormValue(powerSupply.phase_bc_voltage_v),
        voltage_phase_ac: toFormValue(powerSupply.phase_ac_voltage_v),

        brand_name: toFormValue(protocol.brand_name),
        commercial_name: toFormValue(protocol.commercial_name),
        vin: toFormValue(protocol.vin),
        category: toFormValue(protocol.vehicle_category),
        body_type: toFormValue(protocol.body_type),
        mileage_km: toFormValue(measurement.mileage_km),
        tire_marking_front: toFormValue(protocol.wheel_marking_front),
        tire_marking_rear: toFormValue(protocol.wheel_marking_rear),
        tire_season: toFormValue(protocol.tire_season),
        tire_spikes_present: booleanToSelect(protocol.has_spikes),
        manufacture_year: toFormValue(protocol.manufacture_year),
        color: toFormValue(protocol.color),

        wheel_formula: toFormValue(measurement.wheel_formula),
        mufflers_count: toFormValue(measurement.mufflers_count),
        seats_count: toFormValue(measurement.seats_count),
        side_steps_present: booleanToSelect(measurement.steps_present),

        engine_model: toFormValue(measurement.engine_model),
        engine_power_kw: toFormValue(measurement.engine_power_kw),
        engine_layout: toFormValue(measurement.engine_layout),
        cylinder_layout: toFormValue(measurement.cylinder_layout),
        cylinders_count: toFormValue(measurement.cylinders_count),
        fuel_type: toFormValue(measurement.fuel_type),
        turbo_present: booleanToSelect(measurement.turbo_present),

        steering_booster_type: toFormValue(measurement.steering_booster_type),
        transmission_type: toFormValue(measurement.transmission_type),

        service_brake_type: toFormValue(brake.service_brake_type),
        parking_brake_type: toFormValue(brake.parking_brake_type),
        service_brake_control_force_axle1_n: toFormValue(brake.service_brake_control_force_axle1_n),
        service_brake_control_force_axle2_n: toFormValue(brake.service_brake_control_force_axle2_n),
        parking_brake_control_force_n: toFormValue(brake.parking_brake_control_force_n),
        axle_1_brake_difference_pct: toFormValue(brake.axle_1_brake_difference_pct),
        axle_2_brake_difference_pct: toFormValue(brake.axle_2_brake_difference_pct),
        service_brake_front_left_kn: toFormValue(brake.service_brake_front_left_kn),
        service_brake_front_right_kn: toFormValue(brake.service_brake_front_right_kn),
        service_brake_rear_left_kn: toFormValue(brake.service_brake_rear_left_kn),
        service_brake_rear_right_kn: toFormValue(brake.service_brake_rear_right_kn),
        parking_brake_left_kn: toFormValue(brake.parking_brake_left_kn),
        parking_brake_right_kn: toFormValue(brake.parking_brake_right_kn),

        stand_axle1_load_kg: toFormValue(measurement.stand_axle1_load_kg),
        stand_axle2_load_kg: toFormValue(measurement.stand_axle2_load_kg),

        low_beam_count: toFormValue(light.low_beam_count),
        low_beam_color: toFormValue(light.low_beam_color),
        high_beam_count: toFormValue(light.high_beam_count),
        high_beam_color: toFormValue(light.high_beam_color),
        front_fog_count: toFormValue(light.front_fog_count),
        front_fog_color: toFormValue(light.front_fog_color),
        reverse_light_count: toFormValue(light.reverse_light_count),
        reverse_light_color: toFormValue(light.reverse_light_color),
        turn_signal_count: toFormValue(light.turn_signal_count),
        turn_signal_color: toFormValue(light.turn_signal_color),
        front_position_light_count: toFormValue(light.front_position_light_count),
        front_position_light_color: toFormValue(light.front_position_light_color),
        rear_position_light_count: toFormValue(light.rear_position_light_count),
        rear_position_light_color: toFormValue(light.rear_position_light_color),
        main_brake_signal_count: toFormValue(light.main_brake_signal_count),
        main_brake_signal_color: toFormValue(light.main_brake_signal_color),
        additional_brake_signal_count: toFormValue(light.additional_brake_signal_count),
        additional_brake_signal_color: toFormValue(light.additional_brake_signal_color),
        rear_fog_count: toFormValue(light.rear_fog_count),
        rear_fog_color: toFormValue(light.rear_fog_color),
        plate_light_count: toFormValue(light.plate_light_count),
        plate_light_color: toFormValue(light.plate_light_color),
        daytime_running_light_count: toFormValue(light.daytime_running_light_count),
        daytime_running_light_color: toFormValue(light.daytime_running_light_color),
        parking_light_count: toFormValue(light.parking_light_count),
        parking_light_color: toFormValue(light.parking_light_color),
        rear_parking_light_count: toFormValue(light.rear_parking_light_count),
        rear_parking_light_color: toFormValue(light.rear_parking_light_color),
        adaptive_front_lighting_count: toFormValue(light.adaptive_front_lighting_count),
        adaptive_front_lighting_color: toFormValue(light.adaptive_front_lighting_color),

        headlight_type: toFormValue(light.headlight_type),
        headlight_washer_present: booleanToSelect(light.headlight_washer_present),

        left_34v_cd: toFormValue(light.left_34v_cd),
        left_52h_cd: toFormValue(light.left_52h_cd),
        left_high_beam_cd: toFormValue(light.left_high_beam_cd),
        right_34v_cd: toFormValue(light.right_34v_cd),
        right_52h_cd: toFormValue(light.right_52h_cd),
        right_high_beam_cd: toFormValue(light.right_high_beam_cd),
        turn_signal_frequency_per_min: toFormValue(light.turn_signal_frequency_per_min),
        turn_signal_frequency_hz: toFormValue(light.turn_signal_frequency_hz),

        low_beam_upper_point_mm: toFormValue(light.low_beam_upper_point_mm),
        low_beam_lower_point_mm: toFormValue(light.low_beam_lower_point_mm),
        fog_light_upper_point_mm: toFormValue(light.fog_light_upper_point_mm),
        fog_light_lower_point_mm: toFormValue(light.fog_light_lower_point_mm),
        fog_light_left_distance_mm: toFormValue(light.fog_light_left_distance_mm),
        fog_light_right_distance_mm: toFormValue(light.fog_light_right_distance_mm),
        brake_signal_upper_point_mm: toFormValue(light.brake_signal_upper_point_mm),
        brake_signal_lower_point_mm: toFormValue(light.brake_signal_lower_point_mm),
        brake_signal_left_distance_mm: toFormValue(light.brake_signal_left_distance_mm),
        brake_signal_right_distance_mm: toFormValue(light.brake_signal_right_distance_mm),
        additional_brake_signal_from_glass_edge_mm: toFormValue(light.additional_brake_signal_from_glass_edge_mm),
        additional_brake_signal_from_support_surface_mm: toFormValue(light.additional_brake_signal_from_support_surface_mm),
        additional_brake_signal_optical_center_shift_mm: toFormValue(light.additional_brake_signal_optical_center_shift_mm),
        rear_fog_upper_point_mm: toFormValue(light.rear_fog_upper_point_mm),
        rear_fog_lower_point_mm: toFormValue(light.rear_fog_lower_point_mm),

        spare_wheel_present: booleanToSelect(measurement.spare_wheel_present),
        steering_lock_present: booleanToSelect(measurement.steering_lock_present),
        gas_equipment_present: booleanToSelect(measurement.gas_equipment_present),

        tire_depth_fl_mm: toFormValue(measurement.tire_depth_fl_mm),
        tire_depth_rl_mm: toFormValue(measurement.tire_depth_rl_mm),
        tire_depth_fr_mm: toFormValue(measurement.tire_depth_fr_mm),
        tire_depth_rr_mm: toFormValue(measurement.tire_depth_rr_mm),
        bumper_ends_bent_to_body: booleanToSelect(measurement.bumper_bends_to_body),
        bumper_to_body_distance_mm: toFormValue(measurement.bumper_to_body_distance_mm),
        opening_roof_present: booleanToSelect(measurement.opening_roof_present),
        fuel_leak_prevention_measure: toFormValue(measurement.fuel_tank_leak_protection_measure),
        protruding_elements_doors_mm: toFormValue(measurement.protruding_elements_doors_mm),
        protruding_elements_other_mm: toFormValue(measurement.protruding_elements_other_mm),
        glass_transparency_right_pct: toFormValue(measurement.glass_transparency_right_pct),
        glass_transparency_left_pct: toFormValue(measurement.glass_transparency_left_pct),
        glass_transparency_windshield_pct: toFormValue(measurement.glass_transparency_windshield_pct),
        sun_strip_width_mm: toFormValue(measurement.sun_strip_width_mm),
        steering_backlash_deg: toFormValue(measurement.steering_backlash_deg),
        speed_by_speedometer_kmh: toFormValue(measurement.speed_by_speedometer_kmh),
        actual_speed_kmh: toFormValue(measurement.actual_speed_kmh),
        exhaust_noise_constant_db: toFormValue(measurement.exhaust_noise_constant_db),
        exhaust_noise_deceleration_db: toFormValue(measurement.exhaust_noise_deceleration_db),
        co_min_pct: toFormValue(measurement.co_min_pct),
        co_max_pct: toFormValue(measurement.co_max_pct),
        light_absorption_1: toFormValue(measurement.light_absorption_1),
        light_absorption_2: toFormValue(measurement.light_absorption_2),
        light_absorption_3: toFormValue(measurement.light_absorption_3),
        light_absorption_4: toFormValue(measurement.light_absorption_4),
        light_absorption_5: toFormValue(measurement.light_absorption_5),
        light_absorption_6: toFormValue(measurement.light_absorption_6),
        vehicle_length_mm: toFormValue(measurement.vehicle_length_mm),
        vehicle_width_mm: toFormValue(measurement.vehicle_width_mm),
        vehicle_height_mm: toFormValue(measurement.vehicle_height_mm),
        vehicle_weight_kg: toFormValue(measurement.vehicle_weight_kg),
        axle1_load_kg: toFormValue(measurement.axle1_load_kg),
        axle2_load_kg: toFormValue(measurement.axle2_load_kg),
    };
}

function buildProtocolPayload(form) {
    return {
        appendix_number: emptyToNull(form.appendix_number),
        brand_name: emptyToNull(form.brand_name),
        commercial_name: emptyToNull(form.commercial_name),
        vin: emptyToNull(form.vin),
        vehicle_category: emptyToNull(form.category),
        body_type: emptyToNull(form.body_type),
        wheel_marking_front: emptyToNull(form.tire_marking_front),
        wheel_marking_rear: emptyToNull(form.tire_marking_rear),
        tire_season: emptyToNull(form.tire_season),
        has_spikes: stringToBooleanOrNull(form.tire_spikes_present),
        manufacture_year: emptyToNull(form.manufacture_year),
        color: emptyToNull(form.color),
    };
}

function buildTestConditionsPayload(form) {
    return {
        ambient_temperature_c: emptyToNull(form.ambient_temp_c),
        relative_humidity_pct: emptyToNull(form.ambient_humidity_pct),
        atmospheric_pressure_kpa: emptyToNull(form.atmospheric_pressure_kpa),
    };
}

function buildRoadConditionsPayload(form) {
    return {
        road_ambient_temperature_c: emptyToNull(form.road_ambient_temp_c),
        road_relative_humidity_pct: emptyToNull(form.road_ambient_humidity_pct),
    };
}

function buildPowerSupplyPayload(form) {
    return {
        frequency_hz: emptyToNull(form.electric_frequency_hz),
        phase_a_n_voltage_v: emptyToNull(form.voltage_phase_a_zero),
        phase_b_n_voltage_v: emptyToNull(form.voltage_phase_b_zero),
        phase_c_n_voltage_v: emptyToNull(form.voltage_phase_c_zero),
        phase_ab_voltage_v: emptyToNull(form.voltage_phase_ab),
        phase_bc_voltage_v: emptyToNull(form.voltage_phase_bc),
        phase_ac_voltage_v: emptyToNull(form.voltage_phase_ac),
    };
}

function buildMeasurementPayload(form) {
    return {
        mileage_km: emptyToNull(form.mileage_km),

        wheel_formula: emptyToNull(form.wheel_formula),
        mufflers_count: emptyToNull(form.mufflers_count),
        seats_count: emptyToNull(form.seats_count),
        steps_present: stringToBooleanOrNull(form.side_steps_present),

        engine_model: emptyToNull(form.engine_model),
        engine_power_kw: emptyToNull(form.engine_power_kw),
        engine_layout: emptyToNull(form.engine_layout),
        cylinder_layout: emptyToNull(form.cylinder_layout),
        cylinders_count: emptyToNull(form.cylinders_count),
        fuel_type: emptyToNull(form.fuel_type),
        turbo_present: stringToBooleanOrNull(form.turbo_present),

        steering_booster_type: emptyToNull(form.steering_booster_type),
        transmission_type: emptyToNull(form.transmission_type),

        tire_depth_fl_mm: emptyToNull(form.tire_depth_fl_mm),
        tire_depth_fr_mm: emptyToNull(form.tire_depth_fr_mm),
        tire_depth_rl_mm: emptyToNull(form.tire_depth_rl_mm),
        tire_depth_rr_mm: emptyToNull(form.tire_depth_rr_mm),

        bumper_bends_to_body: stringToBooleanOrNull(form.bumper_ends_bent_to_body),
        bumper_to_body_distance_mm: emptyToNull(form.bumper_to_body_distance_mm),
        opening_roof_present: stringToBooleanOrNull(form.opening_roof_present),
        fuel_tank_leak_protection_measure: emptyToNull(form.fuel_leak_prevention_measure),

        protruding_elements_doors_mm: emptyToNull(form.protruding_elements_doors_mm),
        protruding_elements_other_mm: emptyToNull(form.protruding_elements_other_mm),

        glass_transparency_right_pct: emptyToNull(form.glass_transparency_right_pct),
        glass_transparency_left_pct: emptyToNull(form.glass_transparency_left_pct),
        glass_transparency_windshield_pct: emptyToNull(form.glass_transparency_windshield_pct),
        sun_strip_width_mm: emptyToNull(form.sun_strip_width_mm),

        steering_backlash_deg: emptyToNull(form.steering_backlash_deg),

        speed_by_speedometer_kmh: emptyToNull(form.speed_by_speedometer_kmh),
        actual_speed_kmh: emptyToNull(form.actual_speed_kmh),

        exhaust_noise_constant_db: emptyToNull(form.exhaust_noise_constant_db),
        exhaust_noise_deceleration_db: emptyToNull(form.exhaust_noise_deceleration_db),
        co_min_pct: emptyToNull(form.co_min_pct),
        co_max_pct: emptyToNull(form.co_max_pct),

        light_absorption_1: emptyToNull(form.light_absorption_1),
        light_absorption_2: emptyToNull(form.light_absorption_2),
        light_absorption_3: emptyToNull(form.light_absorption_3),
        light_absorption_4: emptyToNull(form.light_absorption_4),
        light_absorption_5: emptyToNull(form.light_absorption_5),
        light_absorption_6: emptyToNull(form.light_absorption_6),

        vehicle_length_mm: emptyToNull(form.vehicle_length_mm),
        vehicle_width_mm: emptyToNull(form.vehicle_width_mm),
        vehicle_height_mm: emptyToNull(form.vehicle_height_mm),
        vehicle_weight_kg: emptyToNull(form.vehicle_weight_kg),

        axle1_load_kg: emptyToNull(form.axle1_load_kg),
        axle2_load_kg: emptyToNull(form.axle2_load_kg),
        stand_axle1_load_kg: emptyToNull(form.stand_axle1_load_kg),
        stand_axle2_load_kg: emptyToNull(form.stand_axle2_load_kg),

        spare_wheel_present: stringToBooleanOrNull(form.spare_wheel_present),
        steering_lock_present: stringToBooleanOrNull(form.steering_lock_present),
        gas_equipment_present: stringToBooleanOrNull(form.gas_equipment_present),
    };
}

function buildBrakePayload(form) {
    return {
        service_brake_type: emptyToNull(form.service_brake_type),
        parking_brake_type: emptyToNull(form.parking_brake_type),

        service_brake_control_force_axle1_n: emptyToNull(form.service_brake_control_force_axle1_n),
        service_brake_control_force_axle2_n: emptyToNull(form.service_brake_control_force_axle2_n),
        parking_brake_control_force_n: emptyToNull(form.parking_brake_control_force_n),

        axle_1_brake_difference_pct: emptyToNull(form.axle_1_brake_difference_pct),
        axle_2_brake_difference_pct: emptyToNull(form.axle_2_brake_difference_pct),

        service_brake_front_left_kn: emptyToNull(form.service_brake_front_left_kn),
        service_brake_front_right_kn: emptyToNull(form.service_brake_front_right_kn),
        service_brake_rear_left_kn: emptyToNull(form.service_brake_rear_left_kn),
        service_brake_rear_right_kn: emptyToNull(form.service_brake_rear_right_kn),

        parking_brake_left_kn: emptyToNull(form.parking_brake_left_kn),
        parking_brake_right_kn: emptyToNull(form.parking_brake_right_kn),
    };
}

function buildLightPayload(form) {
    return {
        low_beam_count: emptyToNull(form.low_beam_count),
        low_beam_color: emptyToNull(form.low_beam_color),

        high_beam_count: emptyToNull(form.high_beam_count),
        high_beam_color: emptyToNull(form.high_beam_color),

        front_fog_count: emptyToNull(form.front_fog_count),
        front_fog_color: emptyToNull(form.front_fog_color),

        reverse_light_count: emptyToNull(form.reverse_light_count),
        reverse_light_color: emptyToNull(form.reverse_light_color),

        turn_signal_count: emptyToNull(form.turn_signal_count),
        turn_signal_color: emptyToNull(form.turn_signal_color),

        front_position_light_count: emptyToNull(form.front_position_light_count),
        front_position_light_color: emptyToNull(form.front_position_light_color),

        rear_position_light_count: emptyToNull(form.rear_position_light_count),
        rear_position_light_color: emptyToNull(form.rear_position_light_color),

        main_brake_signal_count: emptyToNull(form.main_brake_signal_count),
        main_brake_signal_color: emptyToNull(form.main_brake_signal_color),

        additional_brake_signal_count: emptyToNull(form.additional_brake_signal_count),
        additional_brake_signal_color: emptyToNull(form.additional_brake_signal_color),

        rear_fog_count: emptyToNull(form.rear_fog_count),
        rear_fog_color: emptyToNull(form.rear_fog_color),

        plate_light_count: emptyToNull(form.plate_light_count),
        plate_light_color: emptyToNull(form.plate_light_color),

        daytime_running_light_count: emptyToNull(form.daytime_running_light_count),
        daytime_running_light_color: emptyToNull(form.daytime_running_light_color),

        parking_light_count: emptyToNull(form.parking_light_count),
        parking_light_color: emptyToNull(form.parking_light_color),

        rear_parking_light_count: emptyToNull(form.rear_parking_light_count),
        rear_parking_light_color: emptyToNull(form.rear_parking_light_color),

        adaptive_front_lighting_count: emptyToNull(form.adaptive_front_lighting_count),
        adaptive_front_lighting_color: emptyToNull(form.adaptive_front_lighting_color),

        headlight_type: emptyToNull(form.headlight_type),
        headlight_washer_present: stringToBooleanOrNull(form.headlight_washer_present),

        left_34v_cd: emptyToNull(form.left_34v_cd),
        left_52h_cd: emptyToNull(form.left_52h_cd),
        left_high_beam_cd: emptyToNull(form.left_high_beam_cd),

        right_34v_cd: emptyToNull(form.right_34v_cd),
        right_52h_cd: emptyToNull(form.right_52h_cd),
        right_high_beam_cd: emptyToNull(form.right_high_beam_cd),

        turn_signal_frequency_per_min: emptyToNull(form.turn_signal_frequency_per_min),
        turn_signal_frequency_hz: emptyToNull(form.turn_signal_frequency_hz),

        low_beam_upper_point_mm: emptyToNull(form.low_beam_upper_point_mm),
        low_beam_lower_point_mm: emptyToNull(form.low_beam_lower_point_mm),

        fog_light_upper_point_mm: emptyToNull(form.fog_light_upper_point_mm),
        fog_light_lower_point_mm: emptyToNull(form.fog_light_lower_point_mm),
        fog_light_left_distance_mm: emptyToNull(form.fog_light_left_distance_mm),
        fog_light_right_distance_mm: emptyToNull(form.fog_light_right_distance_mm),

        brake_signal_upper_point_mm: emptyToNull(form.brake_signal_upper_point_mm),
        brake_signal_lower_point_mm: emptyToNull(form.brake_signal_lower_point_mm),
        brake_signal_left_distance_mm: emptyToNull(form.brake_signal_left_distance_mm),
        brake_signal_right_distance_mm: emptyToNull(form.brake_signal_right_distance_mm),

        additional_brake_signal_from_glass_edge_mm: emptyToNull(form.additional_brake_signal_from_glass_edge_mm),
        additional_brake_signal_from_support_surface_mm: emptyToNull(form.additional_brake_signal_from_support_surface_mm),
        additional_brake_signal_optical_center_shift_mm: emptyToNull(form.additional_brake_signal_optical_center_shift_mm),

        rear_fog_upper_point_mm: emptyToNull(form.rear_fog_upper_point_mm),
        rear_fog_lower_point_mm: emptyToNull(form.rear_fog_lower_point_mm),
    };
}

function ProtocolInspection() {
    const {id} = useParams();
    const navigate = useNavigate();

    const currentProtocolId = id;

    const [form, setForm] = useState(initialForm);

    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [successMessage, setSuccessMessage] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const handleChange = (e) => {
        const {name, value} = e.target;

        setForm((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const loadProtocol = async (protocolId = currentProtocolId) => {
        if (!protocolId) return;

        try {
            setLoading(true);
            setErrorMessage("");

            const response = await api.get(`/cars/protocols/${protocolId}/full/`);
            const mappedForm = mapProtocolToForm(response.data);

            setForm(mappedForm);
        } catch (error) {
            console.error("Ошибка загрузки протокола:", error);
            setErrorMessage("Не удалось загрузить данные протокола");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (id) {
            loadProtocol(id);
        } else {
            setErrorMessage("Не передан ID протокола");
        }
    }, [id]);

    const handleSave = async () => {
        try {
            setSaving(true);
            setSuccessMessage("");
            setErrorMessage("");

            const protocolPayload = buildProtocolPayload(form);
            const testConditionsPayload = buildTestConditionsPayload(form);
            const roadConditionsPayload = buildRoadConditionsPayload(form);
            const powerSupplyPayload = buildPowerSupplyPayload(form);
            const measurementPayload = buildMeasurementPayload(form);
            const brakePayload = buildBrakePayload(form);
            const lightPayload = buildLightPayload(form);

            const protocolId = currentProtocolId;

            if (!protocolId) {
                setErrorMessage("Не передан ID протокола");
                return;
            }

            await api.patch(`/cars/protocols/${protocolId}/update/`, protocolPayload);

            await Promise.all([
                api.patch(`/cars/protocols/${protocolId}/test-conditions/update/`, testConditionsPayload),
                api.patch(`/cars/protocols/${protocolId}/road-conditions/update/`, roadConditionsPayload),
                api.patch(`/cars/protocols/${protocolId}/power-supply/update/`, powerSupplyPayload),
                api.patch(`/cars/protocols/${protocolId}/measurement/update/`, measurementPayload),
                api.patch(`/cars/protocols/${protocolId}/brake/update/`, brakePayload),
                api.patch(`/cars/protocols/${protocolId}/light/update/`, lightPayload),
            ]);

            await loadProtocol(protocolId);
            setSuccessMessage("Протокол успешно сохранён");
        } catch (error) {
            console.error("Ошибка сохранения:", error);
            setErrorMessage("Ошибка при сохранении данных");
        } finally {
            setSaving(false);
        }
    };

    const handleGenerateDocx = async () => {
        if (!currentProtocolId) {
            setErrorMessage("Сначала сохраните протокол");
            return;
        }

        try {
            setErrorMessage("");

            const response = await api.generateProtocolDocx(currentProtocolId);

            const blob = new Blob([response.data], {
                type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            });

            const url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = `protocol_${currentProtocolId}.docx`;
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error("Ошибка генерации DOCX:", error);
            setErrorMessage("Не удалось сформировать DOCX");
        }
    };

    const commonSectionProps = {
        form,
        handleChange,
        textFieldSx,
        selectFieldSx,
        sectionPaperSx,
        sectionTitleSx,
        subsectionTitleSx,
    };

    return (
        <Box sx={pageSx}>
            <Box sx={pageInnerSx}>
                <Typography variant="h4" sx={{color: "black", fontWeight: 700}}>
                    Осмотр автомобиля — Приложение 1-2 — протокол #{currentProtocolId || "новый"}
                </Typography>

                {loading && <Alert severity="info">Загрузка данных...</Alert>}
                {successMessage && <Alert severity="success">{successMessage}</Alert>}
                {errorMessage && <Alert severity="error">{errorMessage}</Alert>}

                <ProtocolInspectionHeader {...commonSectionProps} />
                <ProtocolInspectionConditions {...commonSectionProps} />
                <ProtocolInspectionPhotos {...commonSectionProps} />
                <ProtocolInspectionVehicle {...commonSectionProps} />
                <ProtocolInspectionEngine {...commonSectionProps} />
                <ProtocolInspectionSteeringTransmission {...commonSectionProps} />
                <ProtocolInspectionBrakes {...commonSectionProps} />
                <ProtocolInspectionLightsMain {...commonSectionProps} />
                <ProtocolInspectionLightsGeometry {...commonSectionProps} />
                <ProtocolInspectionMisc {...commonSectionProps} />

                <Box
                    sx={{
                        display: "flex",
                        justifyContent: "flex-end",
                        gap: 2,
                        pb: 2,
                    }}
                >
                    <Button
                        variant="outlined"
                        onClick={handleGenerateDocx}
                        disabled={!currentProtocolId}
                        sx={{
                            px: 4,
                            py: 1.2,
                            borderColor: "black",
                            color: "black",
                        }}
                    >
                        Сформировать DOCX
                    </Button>

                    <Button
                        variant="contained"
                        onClick={handleSave}
                        disabled={saving || loading}
                        sx={{
                            px: 4,
                            py: 1.2,
                            backgroundColor: "black",
                            color: "white",
                            "&:hover": {
                                backgroundColor: "#222",
                            },
                        }}
                    >
                        {saving ? "Сохранение..." : "Сохранить"}
                    </Button>
                </Box>
            </Box>
        </Box>
    );
}

export default ProtocolInspection;