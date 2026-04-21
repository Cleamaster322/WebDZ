import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Alert from "@mui/material/Alert";
import { renderField } from "./protocolInspectionHelpers.jsx";

function ProtocolInspectionPhotos({
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
        3. Фото автомобиля
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        Фото: с 4-х сторон, номер кузова (VIN), шильдик, бирка размера колес,
        общий пробег транспортного средства, фото испытаний.
      </Alert>

      <Typography variant="h6" sx={subsectionTitleSx}>
        Описание и комментарии по фото
      </Typography>

      <Grid container spacing={2}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Комментарий по фотографиям",
          name: "photos_comment",
          md: 12,
          multiline: true,
          minRows: 4,
        })}
      </Grid>
    </Paper>
  );
}

export default ProtocolInspectionPhotos;