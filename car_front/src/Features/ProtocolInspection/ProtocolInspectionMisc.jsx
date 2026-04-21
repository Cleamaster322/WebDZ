import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import { renderField, renderSelect } from "./protocolInspectionHelpers.jsx";

function ProtocolInspectionMisc({
  form,
  handleChange,
  textFieldSx,
  selectFieldSx,
  sectionPaperSx,
  sectionTitleSx,
  subsectionTitleSx,
}) {
  return (
    <Paper sx={sectionPaperSx}>
      <Typography variant="h5" sx={sectionTitleSx}>
        10. Прочее
      </Typography>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Остаточная глубина рисунка протектора
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Левое переднее, мм",
          name: "tire_depth_fl_mm",
          md: 3,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Левое заднее, мм",
          name: "tire_depth_rl_mm",
          md: 3,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Правое переднее, мм",
          name: "tire_depth_fr_mm",
          md: 3,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Правое заднее, мм",
          name: "tire_depth_rr_mm",
          md: 3,
        })}
      </Grid>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Кузов и топливная система
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderSelect({
          form,
          handleChange,
          selectFieldSx,
          label: "Концы бампера загибаются к кузову",
          name: "bumper_ends_bent_to_body",
          md: 6,
          options: [
            { value: "yes", label: "Да" },
            { value: "no", label: "Нет" },
          ],
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Расстояние между краем бампера и кузовом, мм",
          name: "bumper_to_body_distance_mm",
          md: 6,
        })}
        {renderSelect({
          form,
          handleChange,
          selectFieldSx,
          label: "Открывающаяся крыша",
          name: "opening_roof_present",
          md: 6,
          options: [
            { value: "yes", label: "Да" },
            { value: "no", label: "Нет" },
          ],
        })}
        {renderSelect({
          form,
          handleChange,
          selectFieldSx,
          label: "Меры по обеспечению утечки паров и топлива из топливного бака",
          name: "fuel_leak_prevention_measure",
          md: 6,
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
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Ручки дверей, багажника, мм",
          name: "protruding_elements_doors_mm",
          md: 6,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Остальные элементы, мм",
          name: "protruding_elements_other_mm",
          md: 6,
        })}
      </Grid>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Светопропускание стекол
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Правое, %",
          name: "glass_transparency_right_pct",
          md: 4,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Левое, %",
          name: "glass_transparency_left_pct",
          md: 4,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Ветровое, %",
          name: "glass_transparency_windshield_pct",
          md: 4,
        })}
      </Grid>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Дополнительные параметры
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Ширина светозащитной полосы, мм",
          name: "sun_strip_width_mm",
          md: 6,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Суммарный люфт в рулевом управлении, °",
          name: "steering_backlash_deg",
          md: 6,
        })}
      </Grid>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Скорость транспортного средства
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "По спидометру, км/ч",
          name: "speed_by_speedometer_kmh",
          md: 6,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Фактическая, км/ч",
          name: "actual_speed_kmh",
          md: 6,
        })}
      </Grid>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Экология и шум
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Уровень шума отработавших газов, дБа",
          name: "exhaust_noise_db",
          md: 4,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Минимальные обороты: CO, %",
          name: "co_min_pct",
          md: 4,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Максимальные обороты: CO, %",
          name: "co_max_pct",
          md: 4,
        })}
      </Grid>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Коэффициент поглощения света
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Значение 1, м-1",
          name: "light_absorption_1",
          md: 2,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Значение 2, м-1",
          name: "light_absorption_2",
          md: 2,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Значение 3, м-1",
          name: "light_absorption_3",
          md: 2,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Значение 4, м-1",
          name: "light_absorption_4",
          md: 2,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Значение 5, м-1",
          name: "light_absorption_5",
          md: 2,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Значение 6, м-1",
          name: "light_absorption_6",
          md: 2,
        })}
      </Grid>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Габаритные размеры и масса
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Длина, мм",
          name: "vehicle_length_mm",
          md: 3,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Ширина, мм",
          name: "vehicle_width_mm",
          md: 3,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Высота, мм",
          name: "vehicle_height_mm",
          md: 3,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Масса транспортного средства, кг",
          name: "vehicle_weight_kg",
          md: 3,
        })}
      </Grid>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Нагрузка на ось
      </Typography>
      <Grid container spacing={2}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Ось 1, кг",
          name: "axle1_load_kg",
          md: 6,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Ось 2, кг",
          name: "axle2_load_kg",
          md: 6,
        })}
      </Grid>
    </Paper>
  );
}

export default ProtocolInspectionMisc;