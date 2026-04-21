import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import { renderField, renderSelect } from "./protocolInspectionHelpers.jsx";

function ProtocolInspectionPowertrain({
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
        5. Двигатель, рулевое управление, трансмиссия
      </Typography>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Двигатель
      </Typography>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Модель двигателя",
          name: "engine_model",
          md: 6,
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Мощность двигателя, кВт",
          name: "engine_power_kw",
          md: 6,
        })}
        {renderSelect({
          form,
          handleChange,
          selectFieldSx,
          label: "Расположение двигателя",
          name: "engine_layout",
          md: 4,
          options: [
            { value: "transverse", label: "Поперечное" },
            { value: "longitudinal", label: "Продольное" },
          ],
        })}
        {renderSelect({
          form,
          handleChange,
          selectFieldSx,
          label: "Расположение цилиндров",
          name: "cylinder_layout",
          md: 4,
          options: [
            { value: "inline", label: "Рядное" },
            { value: "opposed", label: "Оппозитное" },
            { value: "v_shape", label: "V-образное" },
          ],
        })}
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Количество цилиндров",
          name: "cylinders_count",
          md: 4,
        })}
        {renderSelect({
          form,
          handleChange,
          selectFieldSx,
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
          form,
          handleChange,
          selectFieldSx,
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
          form,
          handleChange,
          selectFieldSx,
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
          form,
          handleChange,
          selectFieldSx,
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
  );
}

export default ProtocolInspectionPowertrain;