import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import {renderSelect} from "./protocolInspectionHelpers.jsx";

function ProtocolInspectionSteeringTransmission({
    form,
    handleChange,
    selectFieldSx,
    sectionPaperSx,
    sectionTitleSx,
    subsectionTitleSx,
}) {
    return (
        <Paper sx={sectionPaperSx}>
            <Typography variant="h5" sx={sectionTitleSx}>
                6. Рулевое управление и трансмиссия
            </Typography>

            <Typography variant="h6" sx={subsectionTitleSx}>
                Рулевое управление
            </Typography>

            <Grid container spacing={2} sx={{mb: 3}}>
                {renderSelect({
                    form,
                    handleChange,
                    selectFieldSx,
                    label: "Тип усилителя",
                    name: "steering_booster_type",
                    md: 6,
                    options: [
                        {value: "hydraulic", label: "гидромеханический"},
                        {value: "electric", label: "электромеханический"},
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
                        {value: "automatic", label: "Автомат"},
                        {value: "variator", label: "Вариатор"},
                        {value: "manual", label: "Механика"},
                        {value: "robot", label: "Робот"},
                        {value: "reductor", label: "Редуктор"},
                    ],
                })}
            </Grid>
        </Paper>
    );
}

export default ProtocolInspectionSteeringTransmission;