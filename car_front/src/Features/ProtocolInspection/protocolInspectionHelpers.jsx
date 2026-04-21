import React from "react";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";

export function renderField({
  form,
  handleChange,
  textFieldSx,
  label,
  name,
  md = 4,
  placeholder = "",
  multiline = false,
  minRows = 1,
}) {
  return (
    <Grid size={{ xs: 12, md }}>
      <TextField
        label={label}
        name={name}
        value={form[name] ?? ""}
        onChange={handleChange}
        fullWidth
        placeholder={placeholder}
        multiline={multiline}
        minRows={minRows}
        sx={textFieldSx}
      />
    </Grid>
  );
}

export function renderSelect({
  form,
  handleChange,
  selectFieldSx,
  label,
  name,
  md = 4,
  options = [],
}) {
  return (
    <Grid size={{ xs: 12, md }}>
      <FormControl fullWidth size="small" variant="outlined" sx={selectFieldSx}>
        <InputLabel>{label}</InputLabel>
        <Select
          native
          name={name}
          value={form[name] ?? ""}
          onChange={handleChange}
          label={label}
          variant="outlined"
        >
          <option value=""></option>
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </Select>
      </FormControl>
    </Grid>
  );
}

export function renderTripleRow({
  form,
  handleChange,
  textFieldSx,
  smallLabelSx,
  items,
  marginBottom = 2,
}) {
  return (
    <Grid container spacing={2} sx={{ mb: marginBottom }}>
      {items.map((item) => (
        <Grid size={{ xs: 12, md: 4 }} key={item.name}>
          <Typography sx={smallLabelSx}>{item.label}</Typography>
          <TextField
            name={item.name}
            value={form[item.name] ?? ""}
            onChange={handleChange}
            fullWidth
            placeholder={item.placeholder ?? ""}
            sx={textFieldSx}
          />
        </Grid>
      ))}
    </Grid>
  );
}

export function renderLightPair({
  form,
  handleChange,
  textFieldSx,
  title,
  countName,
  colorName,
}) {
  return (
    <Grid container spacing={2} sx={{ mb: 2 }} key={countName}>
      <Grid size={{ xs: 12, md: 6 }}>
        <TextField
          label={`${title} — количество`}
          name={countName}
          value={form[countName] ?? ""}
          onChange={handleChange}
          fullWidth
          sx={textFieldSx}
        />
      </Grid>

      <Grid size={{ xs: 12, md: 6 }}>
        <TextField
          label={`${title} — цвет`}
          name={colorName}
          value={form[colorName] ?? ""}
          onChange={handleChange}
          fullWidth
          sx={textFieldSx}
        />
      </Grid>
    </Grid>
  );
}