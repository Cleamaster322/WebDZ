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

const ACTIVE_STATUSES = ["draft", "in_progress"];

function getStatusText(status) {
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

function ProtocolCard({ protocol, onOpen }) {
    return (
        <Paper
            sx={{
                border: "3px solid black",
                borderRadius: 0,
                p: 3,
                minHeight: 220,
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                boxShadow: "none",
            }}
        >
            <Box>
                <Typography variant="h6" fontWeight={700} mb={2}>
                    {protocol.protocol_number || `protocol ${protocol.id}`}
                </Typography>

                <Typography variant="body1" fontWeight={700}>
                    {protocol.brand_name || "Без марки"} {protocol.commercial_name || ""}
                </Typography>

                <Typography variant="body2" sx={{ mt: 1 }}>
                    Статус: {getStatusText(protocol.status)}
                </Typography>

                <Typography variant="body2">
                    VIN: {protocol.vin || "—"}
                </Typography>

                <Typography variant="body2">
                    Год: {protocol.manufacture_year || "—"}
                </Typography>
            </Box>

            <Button
                onClick={() => onOpen(protocol)}
                sx={{
                    mt: 3,
                    alignSelf: "flex-start",
                    p: 0,
                    minWidth: "auto",
                    color: "black",
                    textTransform: "none",
                    fontWeight: 700,
                }}
            >
                открыть
            </Button>
        </Paper>
    );
}

export default function Protocols() {
    const navigate = useNavigate();

    const [protocols, setProtocols] = useState([]);
    const [loading, setLoading] = useState(true);
    const [creating, setCreating] = useState(false);
    const [error, setError] = useState("");

    const loadProtocols = async () => {
        try {
            setLoading(true);
            setError("");

            const response = await api.get("/cars/protocols/");
            const data = response.data;

            let items = [];
            if (Array.isArray(data)) {
                items = data;
            } else if (Array.isArray(data?.results)) {
                items = data.results;
            }

            const activeItems = items.filter((item) =>
                ACTIVE_STATUSES.includes(item.status)
            );

            setProtocols(activeItems);
        } catch (err) {
            console.error(err);
            setError("Не удалось загрузить протоколы");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadProtocols();
    }, []);

    const handleCreate = async () => {
        try {
            setCreating(true);
            setError("");

            const response = await api.post("/cars/protocols/create/", {
                owner_name: "Не указано",
            });

            const createdProtocol = response.data;

            navigate(`/protocols/${createdProtocol.id}/inspection`);
        } catch (err) {
            console.error(err);
            setError("Не удалось создать протокол");
        } finally {
            setCreating(false);
        }
    };

    const handleOpen = (protocol) => {
        navigate(`/protocols/${protocol.id}/inspection`);
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
                sx={{
                    minHeight: "calc(100vh - 64px)",
                    border: "4px solid black",
                    borderRadius: 0,
                    p: 4,
                    bgcolor: "#e9e9e9",
                    boxShadow: "none",
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
                        onClick={handleCreate}
                        disabled={creating}
                        sx={{
                            bgcolor: "black",
                            color: "white",
                            textTransform: "none",
                            borderRadius: 0,
                            px: 3,
                            py: 1.2,
                            fontWeight: 700,
                            boxShadow: "none",
                            "&:hover": {
                                bgcolor: "#222",
                                boxShadow: "none",
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
                    <Typography variant="h6">Нет незавершённых протоколов</Typography>
                ) : (
                    <Grid container spacing={4}>
                        {protocols.map((protocol) => (
                            <Grid item xs={12} sm={6} md={4} lg={3} key={protocol.id}>
                                <ProtocolCard protocol={protocol} onOpen={handleOpen} />
                            </Grid>
                        ))}
                    </Grid>
                )}
            </Paper>
        </Box>
    );
}