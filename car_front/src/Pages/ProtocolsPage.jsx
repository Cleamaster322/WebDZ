import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../shared/api.jsx";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";
import Chip from "@mui/material/Chip";

const ACTIVE_STATUSES = ["draft", "in_progress"];

function getStatusLabel(status) {
  switch (status) {
    case "draft":
      return "Черновик";
    case "in_progress":
      return "В работе";
    case "completed":
      return "Завершён";
    case "approved":
      return "Утверждён";
    case "cancelled":
      return "Отменён";
    default:
      return status || "Неизвестно";
  }
}

function formatDate(dateString) {
  if (!dateString) return "—";
  try {
    return new Date(dateString).toLocaleDateString("ru-RU");
  } catch {
    return dateString;
  }
}

function ProtocolCard({ protocol, onOpen }) {
  return (
    <Paper
      elevation={0}
      sx={{
        border: "3px solid black",
        borderRadius: 0,
        p: 2.5,
        minHeight: 230,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
      }}
    >
      <Box>
        <Typography variant="h6" fontWeight={700} mb={2}>
          {protocol.protocol_number || `Протокол ${protocol.id}`}
        </Typography>

        <Box mb={1.5}>
          <Chip
            label={getStatusLabel(protocol.status)}
            size="small"
            sx={{ fontWeight: 600 }}
          />
        </Box>

        <Typography variant="body1" fontWeight={600}>
          {protocol.brand_name || "Марка не указана"}{" "}
          {protocol.commercial_name || ""}
        </Typography>

        <Typography variant="body2" sx={{ mt: 1 }}>
          VIN: {protocol.vin || "—"}
        </Typography>

        <Typography variant="body2">
          Дата: {formatDate(protocol.protocol_date)}
        </Typography>

        <Typography variant="body2">
          Владелец: {protocol.owner_name || "—"}
        </Typography>
      </Box>

      <Box mt={2}>
        <Button
          variant="text"
          onClick={() => onOpen(protocol)}
          sx={{
            p: 0,
            minWidth: "auto",
            textTransform: "none",
            fontWeight: 700,
            color: "black",
          }}
        >
          открыть
        </Button>
      </Box>
    </Paper>
  );
}

export default function ProtocolsPage() {
  const navigate = useNavigate();

  const [protocols, setProtocols] = useState([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");

  const loadProtocols = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/protocols/");
      const rawData = response?.data;

      let items = [];

      if (Array.isArray(rawData)) {
        items = rawData;
      } else if (Array.isArray(rawData?.results)) {
        items = rawData.results;
      }

      const activeProtocols = items.filter((item) =>
        ACTIVE_STATUSES.includes(item.status)
      );

      setProtocols(activeProtocols);
    } catch (err) {
      console.error(err);
      setError("Не удалось загрузить список протоколов.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProtocols();
  }, []);

  const handleCreateProtocol = async () => {
    try {
      setCreating(true);
      setError("");

      await api.post("/protocols/create/", {
        owner_name: "Не указано",
      });

      navigate("/home");
    } catch (err) {
      console.error(err);
      setError("Не удалось создать протокол.");
    } finally {
      setCreating(false);
    }
  };

  const handleOpenProtocol = (protocol) => {
    console.log("open protocol", protocol);
    navigate("/home");
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "#e9e9e9",
        p: 4,
      }}
    >
      <Paper
        elevation={0}
        sx={{
          minHeight: "calc(100vh - 64px)",
          border: "4px solid black",
          borderRadius: 0,
          p: 4,
          bgcolor: "#e9e9e9",
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            mb: 4,
            gap: 2,
            flexWrap: "wrap",
          }}
        >
          <Typography variant="h4" fontWeight={700}>
            Протоколы в работе
          </Typography>

          <Button
            variant="contained"
            onClick={handleCreateProtocol}
            disabled={creating}
            sx={{
              textTransform: "none",
              fontWeight: 700,
              bgcolor: "black",
              borderRadius: 0,
              px: 3,
              py: 1.2,
              "&:hover": {
                bgcolor: "#222",
              },
            }}
          >
            {creating ? "Создание..." : "Создать"}
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Box sx={{ display: "flex", justifyContent: "center", mt: 6 }}>
            <CircularProgress />
          </Box>
        ) : protocols.length === 0 ? (
          <Typography variant="h6">
            Активных протоколов пока нет.
          </Typography>
        ) : (
          <Grid container spacing={4}>
            {protocols.map((protocol) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={protocol.id}>
                <ProtocolCard
                  protocol={protocol}
                  onOpen={handleOpenProtocol}
                />
              </Grid>
            ))}
          </Grid>
        )}
      </Paper>
    </Box>
  );
}