
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";
import Grid from "@mui/material/Grid";
import { renderField } from "./protocolInspectionHelpers.jsx";

function ProtocolInspectionPhotos({
  form,
  handleChange,
  textFieldSx,
  sectionPaperSx,
  sectionTitleSx,
}) {
  return (
    <Paper sx={sectionPaperSx}>
      <Typography variant="h5" sx={sectionTitleSx}>
        3. Фото автомобиля
      </Typography>

      <Alert severity="info" sx={{ mb: 2 }}>
        Позже сюда лучше добавить отдельный upload-блок на 11 фотографий.
      </Alert>

      <Grid container spacing={2}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Комментарий / список фото",
          name: "photos_comment",
          md: 12,
          multiline: true,
          minRows: 3,
        })}
      </Grid>
    </Paper>
  );
}

export default ProtocolInspectionPhotos;