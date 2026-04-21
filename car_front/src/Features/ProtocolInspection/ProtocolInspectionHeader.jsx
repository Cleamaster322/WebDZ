import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import { renderField } from "./protocolInspectionHelpers.jsx";

function ProtocolInspectionHeader({
  form,
  handleChange,
  textFieldSx,
  sectionPaperSx,
  sectionTitleSx,
}) {
  return (
    <Paper sx={sectionPaperSx}>
      <Typography variant="h5" sx={sectionTitleSx}>
        1. Шапка документа
      </Typography>

      <Grid container spacing={2}>
        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Приложение к технической записи №",
          name: "appendix_number",
          md: 6,
        })}

        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "День",
          name: "appendix_date_day",
          md: 2,
        })}

        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Месяц",
          name: "appendix_date_month",
          md: 2,
        })}

        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Год",
          name: "appendix_date_year",
          md: 2,
        })}
      </Grid>
    </Paper>
  );
}

export default ProtocolInspectionHeader;