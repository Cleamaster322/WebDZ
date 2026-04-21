export const pageSx = {
    width: "100%",
    minHeight: "100vh",
    backgroundColor: "#f6f6f6",
    py: 4,
    px: 3,
};

export const pageInnerSx = {
    width: "100%",
    maxWidth: 1450,
    mx: "auto",
    display: "flex",
    flexDirection: "column",
    gap: 3,
};

export const sectionPaperSx = {
    p: 3,
    borderRadius: 2,
    backgroundColor: "white",
    boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
};

export const sectionTitleSx = {
    mb: 3,
    color: "black",
    fontWeight: 700,
};

export const subsectionTitleSx = {
    mb: 2,
    color: "black",
    fontWeight: 600,
};

export const textFieldSx = {
    "& .MuiInputBase-input": {
        color: "black",
        py: 1.8,
    },
    "& .MuiInputLabel-root": {
        color: "black",
    },
    "& .MuiInputLabel-root.Mui-focused": {
        color: "black",
    },
    "& .MuiOutlinedInput-root": {
        minHeight: 56,
        backgroundColor: "white",
    },
    "& .MuiOutlinedInput-notchedOutline": {
        borderColor: "#bdbdbd",
    },
    "& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline": {
        borderColor: "black",
    },
};

export const selectFieldSx = {
  "& .MuiInputLabel-root": {
    color: "black",
  },
  "& .MuiInputLabel-root.Mui-focused": {
    color: "black",
  },
  "& .MuiOutlinedInput-root": {
    minHeight: 56,
    backgroundColor: "white",
  },
  "& .MuiOutlinedInput-notchedOutline": {
    borderColor: "#bdbdbd",
  },
  "& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline": {
    borderColor: "black",
  },
  "& .MuiSelect-select": {
    display: "flex",
    alignItems: "center",
    minHeight: "unset",
    boxSizing: "border-box",
  },
};

export const smallLabelSx = {
    mb: 1,
    fontWeight: 500,
    color: "black",
};