import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import {renderField, renderSelect} from "./protocolInspectionHelpers.jsx";

function ProtocolInspectionBrakes({
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
                7. Тормозная система
            </Typography>

            <Typography variant="h6" sx={subsectionTitleSx}>
                Типы систем
            </Typography>
            <Grid container spacing={2} sx={{mb: 3}}>
                {renderSelect({
                    form,
                    handleChange,
                    selectFieldSx,
                    label: "Рабочая тормозная система",
                    name: "service_brake_type",
                    md: 6,
                    options: [
                        {value: "disc_disc", label: "Дисковая/дисковая"},
                        {value: "disc_drum", label: "Дисковая/барабанная"},
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
                        {value: "mechanical_hand", label: "Механический ручной"},
                        {value: "mechanical_pedal", label: "Механический педаль"},
                        {value: "electric", label: "Электрический"},
                    ],
                })}
            </Grid>

            <Typography variant="h6" sx={subsectionTitleSx}>
                Усилие на органе управления
            </Typography>
            <Grid container spacing={2} sx={{mb: 3}}>
                {renderField({
                    form,
                    handleChange,
                    textFieldSx,
                    label: "Рабочая тормозная система — ось 1, Н",
                    name: "service_brake_control_force_axle1_n",
                    md: 4,
                })}
                {renderField({
                    form,
                    handleChange,
                    textFieldSx,
                    label: "Рабочая тормозная система — ось 2, Н",
                    name: "service_brake_control_force_axle2_n",
                    md: 4,
                })}
                {renderField({
                    form,
                    handleChange,
                    textFieldSx,
                    label: "Стояночная тормозная система, Н",
                    name: "parking_brake_control_force_n",
                    md: 4,
                })}
            </Grid>

            <Typography variant="h6" sx={subsectionTitleSx}>
                Относительная разность тормозных сил
            </Typography>
            <Grid container spacing={2} sx={{mb: 3}}>
                {renderField({
                    form,
                    handleChange,
                    textFieldSx,
                    label: "Ось 1, %",
                    name: "axle_1_brake_difference_pct",
                    md: 6,
                })}
                {renderField({
                    form,
                    handleChange,
                    textFieldSx,
                    label: "Ось 2, %",
                    name: "axle_2_brake_difference_pct",
                    md: 6,
                })}
            </Grid>

            <Typography variant="h6" sx={subsectionTitleSx}>
                Удельная тормозная сила рабочей тормозной системы
            </Typography>
            <Grid container spacing={2} sx={{mb: 3}}>
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

            <Typography variant="h6" sx={subsectionTitleSx}>
                Удельная тормозная сила стояночной тормозной системы
            </Typography>
            <Grid container spacing={2} sx={{mb: 3}}>
                {renderField({
                    form,
                    handleChange,
                    textFieldSx,
                    label: "Заднее левое, кН",
                    name: "parking_brake_left_kn",
                    md: 6,
                })}
                {renderField({
                    form,
                    handleChange,
                    textFieldSx,
                    label: "Заднее правое, кН",
                    name: "parking_brake_right_kn",
                    md: 6,
                })}
            </Grid>

            <Typography variant="h6" sx={subsectionTitleSx}>
                Нагрузка на ось (стенд)
            </Typography>
            <Grid container spacing={2}>
                {renderField({
                    form,
                    handleChange,
                    textFieldSx,
                    label: "Ось 1, кг",
                    name: "stand_axle1_load_kg",
                    md: 6,
                })}
                {renderField({
                    form,
                    handleChange,
                    textFieldSx,
                    label: "Ось 2, кг",
                    name: "stand_axle2_load_kg",
                    md: 6,
                })}
            </Grid>
        </Paper>
    );
}

export default ProtocolInspectionBrakes;