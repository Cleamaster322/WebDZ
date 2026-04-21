import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import { renderField } from "./protocolInspectionHelpers.jsx";

function ProtocolInspectionConditions({
  form,
  handleChange,
  textFieldSx,
  sectionPaperSx,
  sectionTitleSx,
  subsectionTitleSx,
}) {
  return (
    <Paper sx={sectionPaperSx}>
      <Typography variant="h5" sx={sectionTitleSx}>
        2. Условия проведения испытаний
      </Typography>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Условия проведения испытаний
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Температура окружающей среды, °С",
          name: "ambient_temp_c",
          md: 4,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Относительная влажность, %",
          name: "ambient_humidity_pct",
          md: 4,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Атмосферное давление, кПа",
          name: "atmospheric_pressure_kpa",
          md: 4,
        })}
      </Grid>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Условия проведения испытаний в дорожных условиях
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Температура окружающей среды, °С",
          name: "road_ambient_temp_c",
          md: 6,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Относительная влажность, %",
          name: "road_ambient_humidity_pct",
          md: 6,
        })}
      </Grid>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Параметры электрической сети
      </Typography>

      <Grid container spacing={2} sx={{ mb: 2 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Частота электрической сети, Гц",
          name: "electric_frequency_hz",
          md: 4,
        })}
      </Grid>

      <Grid container spacing={2} sx={{ mb: 2 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Фаза а-ноль, В",
          name: "voltage_phase_a_zero",
          md: 4,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Фаза b-ноль, В",
          name: "voltage_phase_b_zero",
          md: 4,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Фаза c-ноль, В",
          name: "voltage_phase_c_zero",
          md: 4,
        })}
      </Grid>

      <Grid container spacing={2}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Фаза a-фаза b, В",
          name: "voltage_phase_ab",
          md: 4,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Фаза b-фаза c, В",
          name: "voltage_phase_bc",
          md: 4,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Фаза a-фаза c, В",
          name: "voltage_phase_ac",
          md: 4,
        })}
      </Grid>
    </Paper>
  );
}

export default ProtocolInspectionConditions;