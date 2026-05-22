import { useState } from "react";

import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import { renderField } from "./protocolInspectionHelpers.jsx";

function stripProtocolNumber(value) {
  if (value === null || value === undefined) {
    return "";
  }

  const digits = String(value).replace(/\D/g, "");

  if (!digits) {
    return "";
  }

  return String(Number(digits));
}

function formatProtocolNumber(value) {
  if (value === null || value === undefined) {
    return "";
  }

  const digits = String(value).replace(/\D/g, "");

  if (!digits) {
    return "";
  }

  return digits.padStart(5, "0");
}

function ProtocolInspectionHeader({
  form,
  handleChange,
  textFieldSx,
  sectionPaperSx,
  sectionTitleSx,
}) {
  const [protocolNumberFocused, setProtocolNumberFocused] = useState(false);

  const protocolNumberValue = protocolNumberFocused
    ? stripProtocolNumber(form.protocol_number)
    : formatProtocolNumber(form.protocol_number);

  const handleProtocolNumberChange = (event) => {
    const digits = event.target.value.replace(/\D/g, "").slice(0, 5);

    handleChange({
      target: {
        name: "protocol_number",
        value: digits,
      },
    });
  };

  const handleProtocolNumberBlur = () => {
    setProtocolNumberFocused(false);

    handleChange({
      target: {
        name: "protocol_number",
        value: formatProtocolNumber(form.protocol_number),
      },
    });
  };

  return (
    <Paper sx={sectionPaperSx}>
      <Typography variant="h5" sx={sectionTitleSx}>
        1. Шапка документа
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Номер протокола"
            name="protocol_number"
            value={protocolNumberValue}
            onFocus={() => setProtocolNumberFocused(true)}
            onBlur={handleProtocolNumberBlur}
            onChange={handleProtocolNumberChange}
            sx={textFieldSx}
            inputProps={{
              inputMode: "numeric",
              pattern: "[0-9]*",
              maxLength: 5,
            }}
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
          />
        </Grid>

        {renderField({
          form,
          handleChange,
          textFieldSx,
          label: "Приложение к технической записи №",
          name: "appendix_number",
          md: 4,
        })}

        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            type="date"
            label="Дата протокола"
            name="protocol_date"
            value={form.protocol_date || ""}
            onChange={handleChange}
            sx={textFieldSx}
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
          />
        </Grid>
      </Grid>
    </Paper>
  );
}

export default ProtocolInspectionHeader;