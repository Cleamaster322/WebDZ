import api from "../shared/api.jsx";
import { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";

import ProtocolInspectionHeader from "../Features/ProtocolInspection/ProtocolInspectionHeader";
import ProtocolInspectionConditions from "../Features/ProtocolInspection/ProtocolInspectionConditions";
import ProtocolInspectionPhotos from "../Features/ProtocolInspection/ProtocolInspectionPhotos";
import ProtocolInspectionVehicle from "../Features/ProtocolInspection/ProtocolInspectionVehicle";
import ProtocolInspectionPowertrain from "../Features/ProtocolInspection/ProtocolInspectionPowertrain";
import ProtocolInspectionBrakes from "../Features/ProtocolInspection/ProtocolInspectionBrakes";
import ProtocolInspectionLights from "../Features/ProtocolInspection/ProtocolInspectionLights";
import ProtocolInspectionMisc from "../Features/ProtocolInspection/ProtocolInspectionMisc";

import {
  pageSx,
  pageInnerSx,
  sectionPaperSx,
  sectionTitleSx,
  subsectionTitleSx,
  textFieldSx,
  selectFieldSx,
  smallLabelSx,
} from "../Features/ProtocolInspection/protocolInspectionStyles.jsx";

function ProtocolInspection() {
  const id = window.location.pathname.split("/").filter(Boolean).pop();

  const [form, setForm] = useState({
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

    headlight_type: "",
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
    headlight_washer_present: "",
    left_34v_cd: "",
    left_52h_cd: "",
    left_high_beam_cd: "",
    right_34v_cd: "",
    right_52h_cd: "",
    right_high_beam_cd: "",
    turn_signal_frequency_per_min: "",
    turn_signal_frequency_hz: "",

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
    exhaust_noise_db: "",
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
  });

  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {}, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      setSuccessMessage("");
      setErrorMessage("");

      console.log("FORM DATA:", form);
      setSuccessMessage("Форма заполнена. Сохранение в БД подключим следующим шагом.");
    } catch (error) {
      console.error(error);
      setErrorMessage("Ошибка при сохранении");
    } finally {
      setSaving(false);
    }
  };

  const handleGenerateDocx = async () => {
    try {
      const response = await api.generateProtocolDocx(id);

      const blob = new Blob([response.data], {
        type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      });

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `protocol_${id}.docx`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Ошибка генерации DOCX:", error);
      setErrorMessage("Не удалось сформировать DOCX");
    }
  };

  const commonProps = {
    form,
    handleChange,
    textFieldSx,
    selectFieldSx,
    sectionPaperSx,
    sectionTitleSx,
    subsectionTitleSx,
    smallLabelSx,
  };

  return (
    <Box sx={pageSx}>
      <Box sx={pageInnerSx}>
        <Typography variant="h4" sx={{ color: "black", fontWeight: 700 }}>
          Осмотр автомобиля — Приложение 1-2 — протокол #{id}
        </Typography>

        {loading && <Alert severity="info">Загрузка данных...</Alert>}
        {successMessage && <Alert severity="success">{successMessage}</Alert>}
        {errorMessage && <Alert severity="error">{errorMessage}</Alert>}

        <ProtocolInspectionHeader {...commonProps} />
        <ProtocolInspectionConditions {...commonProps} />
        <ProtocolInspectionPhotos {...commonProps} />
        <ProtocolInspectionVehicle {...commonProps} />
        <ProtocolInspectionPowertrain {...commonProps} />
        <ProtocolInspectionBrakes {...commonProps} />
        <ProtocolInspectionLights {...commonProps} />
        <ProtocolInspectionMisc {...commonProps} />

        <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 2, pb: 2 }}>
          <Button
            variant="outlined"
            onClick={handleGenerateDocx}
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