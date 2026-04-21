
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import { renderField, renderTripleRow } from "./protocolInspectionHelpers.jsx";

function ProtocolInspectionConditions({
  form,
  handleChange,
  textFieldSx,
  sectionPaperSx,
  sectionTitleSx,
  subsectionTitleSx,
  smallLabelSx,
}) {
  return (
    <Paper sx={sectionPaperSx}>
      <Typography variant="h5" sx={sectionTitleSx}>
        2. Условия проведения испытаний
      </Typography>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Общие условия
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Температура окружающей среды, °C",
          name: "ambient_temp_c",
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Относительная влажность, %",
          name: "ambient_humidity_pct",
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Атмосферное давление, кПа",
          name: "atmospheric_pressure_kpa",
        })}
      </Grid>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Дорожные условия
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Температура окружающей среды, °C",
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

        {renderTripleRow({
          form,
          handleChange,
          textFieldSx,
          smallLabelSx,
          items: [
            { label: "Фаза a-ноль", name: "voltage_phase_a_zero", placeholder: "В" },
            { label: "Фаза b-ноль", name: "voltage_phase_b_zero", placeholder: "В" },
            { label: "Фаза c-ноль", name: "voltage_phase_c_zero", placeholder: "В" },
          ],
        })}

        {renderTripleRow({
          form,
          handleChange,
          textFieldSx,
          smallLabelSx,
          items: [
            { label: "Фаза a-фаза b", name: "voltage_phase_ab", placeholder: "В" },
            { label: "Фаза b-фаза c", name: "voltage_phase_bc", placeholder: "В" },
            { label: "Фаза a-фаза c", name: "voltage_phase_ac", placeholder: "В" },
          ],
          marginBottom: 0,
        })}
      </Box>
    </Paper>
  );
}

export default ProtocolInspectionConditions;