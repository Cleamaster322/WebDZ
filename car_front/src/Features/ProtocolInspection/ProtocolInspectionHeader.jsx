import { useState } from "react";

import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";

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

    const formattedValue = formatProtocolNumber(form.protocol_number);

    handleChange({
      target: {
        name: "protocol_number",
        value: formattedValue,
      },
    });
  };

  return (
    <Paper sx={sectionPaperSx}>
      <Typography variant="h5" sx={sectionTitleSx}>
        1. Шапка документа
      </Typography>

      <Box
        sx={{
          display: "grid",
          gap: 2,
        }}
      >
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr",
              md: "repeat(3, minmax(0, 1fr))",
            },
            gap: 2,
          }}
        >
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

          <TextField
            fullWidth
            label="Приложение к технической записи №"
            name="appendix_number"
            value={form.appendix_number || ""}
            onChange={handleChange}
            sx={textFieldSx}
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
          />

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
        </Box>

        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr",
              md: "repeat(3, minmax(0, 1fr))",
            },
            gap: 2,
          }}
        >
          <TextField
            fullWidth
            label="Фамилия заказчика"
            name="owner_last_name"
            value={form.owner_last_name || ""}
            onChange={handleChange}
            sx={textFieldSx}
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
          />

          <TextField
            fullWidth
            label="Имя заказчика"
            name="owner_first_name"
            value={form.owner_first_name || ""}
            onChange={handleChange}
            sx={textFieldSx}
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
          />

          <TextField
            fullWidth
            label="Отчество заказчика"
            name="owner_middle_name"
            value={form.owner_middle_name || ""}
            onChange={handleChange}
            sx={textFieldSx}
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
          />
        </Box>

        <TextField
          fullWidth
          multiline
          minRows={2}
          label="Наименование и адрес изготовителя"
          name="manufacturer_info"
          value={form.manufacturer_info || ""}
          onChange={handleChange}
          sx={textFieldSx}
          slotProps={{
            inputLabel: {
              shrink: true,
            },
          }}
        />
      </Box>
    </Paper>
  );
}

export default ProtocolInspectionHeader;