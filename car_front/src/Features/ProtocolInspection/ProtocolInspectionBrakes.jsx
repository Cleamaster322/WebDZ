import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import { renderField, renderSelect } from "./protocolInspectionHelpers.jsx";

function ProtocolInspectionBrakes({
  form,
  handleChange,
  textFieldSx,
  selectFieldSx,
  sectionPaperSx,
  sectionTitleSx,
}) {
  return (
    <Paper sx={sectionPaperSx}>
      <Typography variant="h5" sx={sectionTitleSx}>
        6. Тормозная система
      </Typography>

      <Grid container spacing={2} sx={{ mb: 2 }}>
        {renderSelect({
          form,
          handleChange,
          selectFieldSx,
          label: "Рабочая тормозная система",
          name: "service_brake_type",
          md: 6,
          options: [
            { value: "disc_disc", label: "Дисковая/дисковая" },
            { value: "disc_drum", label: "Дисковая/барабанная" },
          ],
        })}
        {renderSelect({
          form,
          handleChange,
          selectFieldSx,
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
          form,
          handleChange,
          textFieldSx,
          label: "Усилие рабочей тормозной системы, ось 1, Н",
          name: "service_brake_control_force_axle1_n",
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Усилие рабочей тормозной системы, ось 2, Н",
          name: "service_brake_control_force_axle2_n",
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Усилие стояночной тормозной системы, Н",
          name: "parking_brake_control_force_n",
        })}
      </Grid>

      <Grid container spacing={2} sx={{ mb: 2 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Относительная разность тормозных сил, ось 1, %",
          name: "axle_1_brake_difference_pct",
          md: 6,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Относительная разность тормозных сил, ось 2, %",
          name: "axle_2_brake_difference_pct",
          md: 6,
        })}
      </Grid>

      <Grid container spacing={2} sx={{ mb: 2 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Переднее левое, кН",
          name: "service_brake_front_left_kn",
          md: 3,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Переднее правое, кН",
          name: "service_brake_front_right_kn",
          md: 3,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Заднее левое, кН",
          name: "service_brake_rear_left_kn",
          md: 3,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Заднее правое, кН",
          name: "service_brake_rear_right_kn",
          md: 3,
        })}
      </Grid>

      <Grid container spacing={2} sx={{ mb: 2 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Стояночная тормозная сила, заднее левое, кН",
          name: "parking_brake_left_kn",
          md: 6,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Стояночная тормозная сила, заднее правое, кН",
          name: "parking_brake_right_kn",
          md: 6,
        })}
      </Grid>

      <Grid container spacing={2}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Нагрузка на ось (стенд), ось 1, кг",
          name: "stand_axle1_load_kg",
          md: 6,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Нагрузка на ось (стенд), ось 2, кг",
          name: "stand_axle2_load_kg",
          md: 6,
        })}
      </Grid>
    </Paper>
  );
}

export default ProtocolInspectionBrakes;