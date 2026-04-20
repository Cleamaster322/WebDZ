import api from "../shared/api.jsx";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import MenuItem from "@mui/material/MenuItem";
import Alert from "@mui/material/Alert";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import Divider from "@mui/material/Divider";

function ProtocolInspection() {
  const { id } = useParams();

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

  const pageSx = {
    width: "100%",
    minHeight: "100vh",
    backgroundColor: "#f6f6f6",
    py: 4,
    px: 3,
  };

  const pageInnerSx = {
    width: "100%",
    maxWidth: 1450,
    mx: "auto",
    display: "flex",
    flexDirection: "column",
    gap: 3,
  };

  const sectionPaperSx = {
    p: 3,
    borderRadius: 2,
    backgroundColor: "white",
    boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
  };

  const sectionTitleSx = {
    mb: 3,
    color: "black",
    fontWeight: 700,
  };

  const subsectionTitleSx = {
    mb: 2,
    color: "black",
    fontWeight: 600,
  };

  const textFieldSx = {
    "& .MuiInputBase-input": {
      color: "black",
      py: 1.8,
    },
    "& .MuiInputLabel-root": {
      color: "black",
    },
    "& .MuiInputLabel-root.Mui-focused": {
      color: "black",
    },
    "& .MuiOutlinedInput-root": {
      minHeight: 56,
      backgroundColor: "white",
    },
    "& .MuiOutlinedInput-notchedOutline": {
      borderColor: "#bdbdbd",
    },
    "& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline": {
      borderColor: "black",
    },
  };

  const selectFieldSx = {
    ...textFieldSx,
    "& .MuiSelect-select": {
      display: "flex",
      alignItems: "center",
      width: "100%",
      minHeight: "unset",
      py: 1.8,
      boxSizing: "border-box",
    },
  };

  const smallLabelSx = {
    mb: 1,
    fontWeight: 500,
    color: "black",
  };

  const renderField = ({
    label,
    name,
    md = 4,
    placeholder = "",
    multiline = false,
    minRows = 1,
  }) => (
    <Grid item xs={12} md={md}>
      <TextField
        label={label}
        name={name}
        value={form[name] ?? ""}
        onChange={handleChange}
        fullWidth
        placeholder={placeholder}
        multiline={multiline}
        minRows={minRows}
        sx={textFieldSx}
      />
    </Grid>
  );

  const renderSelect = ({
    label,
    name,
    md = 4,
    options = [],
  }) => (
    <Grid item xs={12} md={md}>
      <TextField
        select
        label={label}
        name={name}
        value={form[name] ?? ""}
        onChange={handleChange}
        fullWidth
        size="small"
        sx={selectFieldSx}
      >
        {options.map((option) => (
          <MenuItem key={option.value} value={option.value}>
            {option.label}
          </MenuItem>
        ))}
      </TextField>
    </Grid>
  );

  const renderTripleRow = (items, marginBottom = 2) => (
    <Grid container spacing={2} sx={{ mb: marginBottom }}>
      {items.map((item) => (
        <Grid item xs={12} md={4} key={item.name}>
          <Typography sx={smallLabelSx}>{item.label}</Typography>
          <TextField
            name={item.name}
            value={form[item.name] ?? ""}
            onChange={handleChange}
            fullWidth
            placeholder={item.placeholder ?? ""}
            sx={textFieldSx}
          />
        </Grid>
      ))}
    </Grid>
  );

  const renderLightPair = (title, countName, colorName) => (
    <Grid container spacing={2} sx={{ mb: 2 }} key={countName}>
      <Grid item xs={12} md={6}>
        <TextField
          label={`${title} — количество`}
          name={countName}
          value={form[countName] ?? ""}
          onChange={handleChange}
          fullWidth
          sx={textFieldSx}
        />
      </Grid>
      <Grid item xs={12} md={6}>
        <TextField
          label={`${title} — цвет`}
          name={colorName}
          value={form[colorName] ?? ""}
          onChange={handleChange}
          fullWidth
          sx={textFieldSx}
        />
      </Grid>
    </Grid>
  );

  return (
    <Box sx={pageSx}>
      <Box sx={pageInnerSx}>
        <Typography variant="h4" sx={{ color: "black", fontWeight: 700 }}>
          Осмотр автомобиля — Приложение 1-2 — протокол #{id}
        </Typography>

        {loading && <Alert severity="info">Загрузка данных...</Alert>}
        {successMessage && <Alert severity="success">{successMessage}</Alert>}
        {errorMessage && <Alert severity="error">{errorMessage}</Alert>}

        <Paper sx={sectionPaperSx}>
          <Typography variant="h5" sx={sectionTitleSx}>
            1. Шапка документа
          </Typography>

          <Grid container spacing={2}>
            {renderField({
              label: "Приложение к технической записи №",
              name: "appendix_number",
              md: 6,
            })}
            {renderField({ label: "День", name: "appendix_date_day", md: 2 })}
            {renderField({ label: "Месяц", name: "appendix_date_month", md: 2 })}
            {renderField({ label: "Год", name: "appendix_date_year", md: 2 })}
          </Grid>
        </Paper>

        <Paper sx={sectionPaperSx}>
          <Typography variant="h5" sx={sectionTitleSx}>
            2. Условия проведения испытаний
          </Typography>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Общие условия
          </Typography>
          <Grid container spacing={2} sx={{ mb: 3 }}>
            {renderField({ label: "Температура окружающей среды, °C", name: "ambient_temp_c" })}
            {renderField({ label: "Относительная влажность, %", name: "ambient_humidity_pct" })}
            {renderField({ label: "Атмосферное давление, кПа", name: "atmospheric_pressure_kpa" })}
          </Grid>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Дорожные условия
          </Typography>
          <Grid container spacing={2} sx={{ mb: 3 }}>
            {renderField({ label: "Температура окружающей среды, °C", name: "road_ambient_temp_c", md: 6 })}
            {renderField({ label: "Относительная влажность, %", name: "road_ambient_humidity_pct", md: 6 })}
          </Grid>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Параметры электрической сети
          </Typography>

          <Box sx={{ mb: 3 }}>
            <Typography sx={smallLabelSx}>Частота электрической сети</Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={4}>
                <TextField
                  name="electric_frequency_hz"
                  value={form.electric_frequency_hz}
                  onChange={handleChange}
                  fullWidth
                  placeholder="Гц"
                  sx={textFieldSx}
                />
              </Grid>
            </Grid>
          </Box>

          <Box sx={{ mb: 1 }}>
            <Typography sx={smallLabelSx}>Напряжение в сети</Typography>

            {renderTripleRow([
              { label: "Фаза a-ноль", name: "voltage_phase_a_zero", placeholder: "В" },
              { label: "Фаза b-ноль", name: "voltage_phase_b_zero", placeholder: "В" },
              { label: "Фаза c-ноль", name: "voltage_phase_c_zero", placeholder: "В" },
            ])}

            {renderTripleRow(
              [
                { label: "Фаза a-фаза b", name: "voltage_phase_ab", placeholder: "В" },
                { label: "Фаза b-фаза c", name: "voltage_phase_bc", placeholder: "В" },
                { label: "Фаза a-фаза c", name: "voltage_phase_ac", placeholder: "В" },
              ],
              0
            )}
          </Box>
        </Paper>

        <Paper sx={sectionPaperSx}>
          <Typography variant="h5" sx={sectionTitleSx}>
            3. Фото автомобиля
          </Typography>

          <Alert severity="info" sx={{ mb: 2 }}>
            Позже сюда лучше добавить отдельный upload-блок на 11 фотографий.
          </Alert>

          <Grid container spacing={2}>
            {renderField({
              label: "Комментарий / список фото",
              name: "photos_comment",
              md: 12,
              multiline: true,
              minRows: 3,
            })}
          </Grid>
        </Paper>

        <Paper sx={sectionPaperSx}>
          <Typography variant="h5" sx={sectionTitleSx}>
            4. Основные сведения об автомобиле
          </Typography>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Марка", name: "brand_name", md: 3, placeholder: "Kia" })}
            {renderField({ label: "Коммерческое название", name: "commercial_name", md: 3, placeholder: "Rio" })}
            {renderField({ label: "VIN (№ кузова/шасси)", name: "vin", md: 3 })}
            {renderSelect({
              label: "Категория",
              name: "category",
              md: 3,
              options: [
                { value: "M1", label: "M1" },
                { value: "N1", label: "N1" },
              ],
            })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Тип кузова", name: "body_type", md: 4 })}
            {renderField({
              label: "Маркировка колес (перед)",
              name: "tire_marking_front",
              md: 4,
              placeholder: "185/65R15",
            })}
            {renderField({
              label: "Маркировка колес (зад)",
              name: "tire_marking_rear",
              md: 4,
              placeholder: "185/65R15",
            })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderSelect({
              label: "Сезонность шин",
              name: "tire_season",
              md: 4,
              options: [
                { value: "summer", label: "Лето" },
                { value: "winter", label: "Зима" },
              ],
            })}
            {renderSelect({
              label: "Наличие шипов",
              name: "tire_spikes_present",
              md: 4,
              options: [
                { value: "yes", label: "Да" },
                { value: "no", label: "Нет" },
              ],
            })}
            {renderField({ label: "Год выпуска", name: "manufacture_year", md: 4 })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Цвет", name: "color", md: 4 })}
            {renderSelect({
              label: "Колесная формула",
              name: "wheel_formula",
              md: 4,
              options: [
                { value: "4x2_front", label: "4x2 передний" },
                { value: "4x2_rear", label: "4x2 задний" },
                { value: "4x4", label: "4x4 полный" },
              ],
            })}
            {renderField({ label: "Количество глушителей", name: "mufflers_count", md: 4 })}
          </Grid>

          <Grid container spacing={2}>
            {renderField({ label: "Количество посадочных мест", name: "seats_count", md: 6 })}
            {renderSelect({
              label: "Подножки",
              name: "side_steps_present",
              md: 6,
              options: [
                { value: "yes", label: "Наличие" },
                { value: "no", label: "Отсутствие" },
              ],
            })}
          </Grid>
        </Paper>

        <Paper sx={sectionPaperSx}>
          <Typography variant="h5" sx={sectionTitleSx}>
            5. Двигатель, рулевое управление, трансмиссия
          </Typography>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Двигатель
          </Typography>
          <Grid container spacing={2} sx={{ mb: 3 }}>
            {renderField({ label: "Модель двигателя", name: "engine_model", md: 6 })}
            {renderField({ label: "Мощность двигателя, кВт", name: "engine_power_kw", md: 6 })}
            {renderSelect({
              label: "Расположение двигателя",
              name: "engine_layout",
              md: 4,
              options: [
                { value: "transverse", label: "Поперечное" },
                { value: "longitudinal", label: "Продольное" },
              ],
            })}
            {renderSelect({
              label: "Расположение цилиндров",
              name: "cylinder_layout",
              md: 4,
              options: [
                { value: "inline", label: "Рядное" },
                { value: "opposed", label: "Оппозитное" },
                { value: "v_shape", label: "V-образное" },
              ],
            })}
            {renderField({ label: "Количество цилиндров", name: "cylinders_count", md: 4 })}
            {renderSelect({
              label: "Вид топлива",
              name: "fuel_type",
              md: 6,
              options: [
                { value: "petrol", label: "Бензин" },
                { value: "diesel", label: "Дизель" },
                { value: "hybrid", label: "Гибрид" },
                { value: "electric", label: "Электро" },
              ],
            })}
            {renderSelect({
              label: "Турбонаддув",
              name: "turbo_present",
              md: 6,
              options: [
                { value: "yes", label: "Наличие" },
                { value: "no", label: "Отсутствие" },
              ],
            })}
          </Grid>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Рулевое управление
          </Typography>
          <Grid container spacing={2} sx={{ mb: 3 }}>
            {renderSelect({
              label: "Тип усилителя",
              name: "steering_booster_type",
              md: 6,
              options: [
                { value: "hydromechanical", label: "гидромеханический" },
                { value: "electromechanical", label: "электромеханический" },
              ],
            })}
          </Grid>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Трансмиссия
          </Typography>
          <Grid container spacing={2}>
            {renderSelect({
              label: "Тип трансмиссии",
              name: "transmission_type",
              md: 6,
              options: [
                { value: "automatic", label: "Автомат" },
                { value: "cvt", label: "Вариатор" },
                { value: "manual", label: "Механика" },
                { value: "robot", label: "Робот" },
                { value: "reducer", label: "Редуктор" },
              ],
            })}
          </Grid>
        </Paper>

        <Paper sx={sectionPaperSx}>
          <Typography variant="h5" sx={sectionTitleSx}>
            6. Тормозная система
          </Typography>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderSelect({
              label: "Рабочая тормозная система",
              name: "service_brake_type",
              md: 6,
              options: [
                { value: "disc_disc", label: "Дисковая/дисковая" },
                { value: "disc_drum", label: "Дисковая/барабанная" },
              ],
            })}
            {renderSelect({
              label: "Стояночная тормозная система",
              name: "parking_brake_type",
              md: 6,
              options: [
                { value: "mechanical_hand", label: "Механический ручной" },
                { value: "mechanical_pedal", label: "Механический педаль" },
                { value: "electric", label: "Электрический" },
              ],
            })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({
              label: "Усилие рабочей тормозной системы, ось 1, Н",
              name: "service_brake_control_force_axle1_n",
            })}
            {renderField({
              label: "Усилие рабочей тормозной системы, ось 2, Н",
              name: "service_brake_control_force_axle2_n",
            })}
            {renderField({
              label: "Усилие стояночной тормозной системы, Н",
              name: "parking_brake_control_force_n",
            })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({
              label: "Относительная разность тормозных сил, ось 1, %",
              name: "axle_1_brake_difference_pct",
              md: 6,
            })}
            {renderField({
              label: "Относительная разность тормозных сил, ось 2, %",
              name: "axle_2_brake_difference_pct",
              md: 6,
            })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Переднее левое, кН", name: "service_brake_front_left_kn", md: 3 })}
            {renderField({ label: "Переднее правое, кН", name: "service_brake_front_right_kn", md: 3 })}
            {renderField({ label: "Заднее левое, кН", name: "service_brake_rear_left_kn", md: 3 })}
            {renderField({ label: "Заднее правое, кН", name: "service_brake_rear_right_kn", md: 3 })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Стояночная тормозная сила, заднее левое, кН", name: "parking_brake_left_kn", md: 6 })}
            {renderField({ label: "Стояночная тормозная сила, заднее правое, кН", name: "parking_brake_right_kn", md: 6 })}
          </Grid>

          <Grid container spacing={2}>
            {renderField({ label: "Нагрузка на ось (стенд), ось 1, кг", name: "stand_axle1_load_kg", md: 6 })}
            {renderField({ label: "Нагрузка на ось (стенд), ось 2, кг", name: "stand_axle2_load_kg", md: 6 })}
          </Grid>
        </Paper>

        <Paper sx={sectionPaperSx}>
          <Typography variant="h5" sx={sectionTitleSx}>
            7. Осветительные приборы
          </Typography>

          {[
            ["Фара ближнего света", "low_beam_count", "low_beam_color"],
            ["Фара дальнего света", "high_beam_count", "high_beam_color"],
            ["Передняя ПТФ", "front_fog_count", "front_fog_color"],
            ["Фонарь заднего хода", "reverse_light_count", "reverse_light_color"],
            ["Указатели поворота", "turn_signal_count", "turn_signal_color"],
            ["Передний габаритный огонь", "front_position_light_count", "front_position_light_color"],
            ["Задний габаритный огонь", "rear_position_light_count", "rear_position_light_color"],
            ["Сигнал торможения основной", "main_brake_signal_count", "main_brake_signal_color"],
            ["Сигнал торможения дополнительный", "additional_brake_signal_count", "additional_brake_signal_color"],
            ["Задний ПТФ", "rear_fog_count", "rear_fog_color"],
            ["Подсветка госномера", "plate_light_count", "plate_light_color"],
            ["ДХО", "daytime_running_light_count", "daytime_running_light_color"],
            ["Стояночные огни", "parking_light_count", "parking_light_color"],
          ].map(([title, countName, colorName]) =>
            renderLightPair(title, countName, colorName)
          )}

          <Divider sx={{ my: 3 }} />

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderSelect({
              label: "Тип фар",
              name: "headlight_type",
              md: 4,
              options: [
                { value: "halogen", label: "Галоген" },
                { value: "xenon", label: "Ксенон" },
                { value: "led", label: "LED" },
              ],
            })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Фары ближнего света: верхняя точка, мм", name: "low_beam_upper_point_mm", md: 6 })}
            {renderField({ label: "Фары ближнего света: нижняя точка, мм", name: "low_beam_lower_point_mm", md: 6 })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "ПТФ: верхняя точка, мм", name: "fog_light_upper_point_mm", md: 6 })}
            {renderField({ label: "ПТФ: нижняя точка, мм", name: "fog_light_lower_point_mm", md: 6 })}
            {renderField({ label: "ПТФ: левая по ширине, мм", name: "fog_light_left_distance_mm", md: 6 })}
            {renderField({ label: "ПТФ: правая по ширине, мм", name: "fog_light_right_distance_mm", md: 6 })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Основной сигнал торможения: верхняя точка, мм", name: "brake_signal_upper_point_mm", md: 6 })}
            {renderField({ label: "Основной сигнал торможения: нижняя точка, мм", name: "brake_signal_lower_point_mm", md: 6 })}
            {renderField({ label: "Основной сигнал торможения: левая по ширине, мм", name: "brake_signal_left_distance_mm", md: 6 })}
            {renderField({ label: "Основной сигнал торможения: правая по ширине, мм", name: "brake_signal_right_distance_mm", md: 6 })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Доп. сигнал: от нижнего края стекла, мм", name: "additional_brake_signal_from_glass_edge_mm" })}
            {renderField({ label: "Доп. сигнал: от опорной поверхности, мм", name: "additional_brake_signal_from_support_surface_mm" })}
            {renderField({ label: "Доп. сигнал: смещение оптического центра, мм", name: "additional_brake_signal_optical_center_shift_mm" })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Задние ПТФ: верхняя точка, мм", name: "rear_fog_upper_point_mm", md: 6 })}
            {renderField({ label: "Задние ПТФ: нижняя точка, мм", name: "rear_fog_lower_point_mm", md: 6 })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderSelect({
              label: "Омыватели фар",
              name: "headlight_washer_present",
              md: 6,
              options: [
                { value: "yes", label: "Наличие" },
                { value: "no", label: "Отсутствие" },
              ],
            })}
          </Grid>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Левая 34В, кд", name: "left_34v_cd", md: 2 })}
            {renderField({ label: "Левая 52Н, кд", name: "left_52h_cd", md: 2 })}
            {renderField({ label: "Левая дальний, кд", name: "left_high_beam_cd", md: 2 })}
            {renderField({ label: "Правая 34В, кд", name: "right_34v_cd", md: 2 })}
            {renderField({ label: "Правая 52Н, кд", name: "right_52h_cd", md: 2 })}
            {renderField({ label: "Правая дальний, кд", name: "right_high_beam_cd", md: 2 })}
          </Grid>

          <Grid container spacing={2}>
            {renderField({ label: "Частота мерцания, пр./мин.", name: "turn_signal_frequency_per_min", md: 6 })}
            {renderField({ label: "Частота мерцания, Гц", name: "turn_signal_frequency_hz", md: 6 })}
          </Grid>
        </Paper>

        <Paper sx={sectionPaperSx}>
          <Typography variant="h5" sx={sectionTitleSx}>
            8. Прочее
          </Typography>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Остаточная глубина рисунка протектора
          </Typography>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Левое переднее, мм", name: "tire_depth_fl_mm", md: 3 })}
            {renderField({ label: "Левое заднее, мм", name: "tire_depth_rl_mm", md: 3 })}
            {renderField({ label: "Правое переднее, мм", name: "tire_depth_fr_mm", md: 3 })}
            {renderField({ label: "Правое заднее, мм", name: "tire_depth_rr_mm", md: 3 })}
          </Grid>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Кузов и топливная система
          </Typography>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderSelect({
              label: "Концы бампера загибаются к кузову",
              name: "bumper_ends_bent_to_body",
              md: 6,
              options: [
                { value: "yes", label: "Да" },
                { value: "no", label: "Нет" },
              ],
            })}
            {renderSelect({
              label: "Открывающаяся крыша",
              name: "opening_roof_present",
              md: 6,
              options: [
                { value: "yes", label: "Да" },
                { value: "no", label: "Нет" },
              ],
            })}
            {renderField({
              label: "Расстояние между краем бампера и кузовом, мм",
              name: "bumper_to_body_distance_mm",
              md: 12,
            })}
            {renderSelect({
              label: "Меры по обеспечению утечки паров и топлива из топливного бака",
              name: "fuel_leak_prevention_measure",
              md: 12,
              options: [
                { value: "fixed_cap", label: "Несъемная крышка" },
                { value: "structural_elements", label: "Элементы конструкции" },
                { value: "other_measure", label: "Любая другая мера" },
              ],
            })}
          </Grid>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Выступающие элементы
          </Typography>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Ручки дверей, багажника, мм", name: "protruding_elements_doors_mm", md: 6 })}
            {renderField({ label: "Остальные элементы, мм", name: "protruding_elements_other_mm", md: 6 })}
          </Grid>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Светопропускание стекол
          </Typography>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Правое, %", name: "glass_transparency_right_pct" })}
            {renderField({ label: "Левое, %", name: "glass_transparency_left_pct" })}
            {renderField({ label: "Ветровое, %", name: "glass_transparency_windshield_pct" })}
          </Grid>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Дополнительные параметры
          </Typography>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Ширина светозащитной полосы, мм", name: "sun_strip_width_mm", md: 6 })}
            {renderField({ label: "Суммарный люфт в Р/У, °", name: "steering_backlash_deg", md: 6 })}
            {renderField({ label: "Скорость по спидометру, км/ч", name: "speed_by_speedometer_kmh", md: 6 })}
            {renderField({ label: "Фактическая скорость, км/ч", name: "actual_speed_kmh", md: 6 })}
            {renderField({ label: "Уровень шума отработавших газов, дБа", name: "exhaust_noise_db", md: 4 })}
            {renderField({ label: "Min обор: CO, %", name: "co_min_pct", md: 4 })}
            {renderField({ label: "Max обор: CO, %", name: "co_max_pct", md: 4 })}
          </Grid>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Коэффициент поглощения света
          </Typography>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "1, м-1", name: "light_absorption_1", md: 2 })}
            {renderField({ label: "2, м-1", name: "light_absorption_2", md: 2 })}
            {renderField({ label: "3, м-1", name: "light_absorption_3", md: 2 })}
            {renderField({ label: "4, м-1", name: "light_absorption_4", md: 2 })}
            {renderField({ label: "5, м-1", name: "light_absorption_5", md: 2 })}
            {renderField({ label: "6, м-1", name: "light_absorption_6", md: 2 })}
          </Grid>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Габаритные размеры и масса
          </Typography>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            {renderField({ label: "Длина, мм", name: "vehicle_length_mm", md: 3 })}
            {renderField({ label: "Ширина, мм", name: "vehicle_width_mm", md: 3 })}
            {renderField({ label: "Высота, мм", name: "vehicle_height_mm", md: 3 })}
            {renderField({ label: "Масса ТС, кг", name: "vehicle_weight_kg", md: 3 })}
          </Grid>

          <Typography variant="h6" sx={subsectionTitleSx}>
            Нагрузка на ось
          </Typography>
          <Grid container spacing={2}>
            {renderField({ label: "Ось 1, кг", name: "axle1_load_kg", md: 6 })}
            {renderField({ label: "Ось 2, кг", name: "axle2_load_kg", md: 6 })}
          </Grid>
        </Paper>

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