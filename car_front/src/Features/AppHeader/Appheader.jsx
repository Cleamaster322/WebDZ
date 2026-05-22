import { useLocation, useNavigate } from "react-router-dom";

import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import api from "../../shared/api.jsx";

function AppHeader() {
    const navigate = useNavigate();
    const location = useLocation();

    const isActive = (path) => location.pathname === path;

    const handleLogout = () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");

        if (api.client?.defaults?.headers?.common) {
            delete api.client.defaults.headers.common["Authorization"];
        }

        navigate("/");
    };

    const navButtonSx = (active) => ({
        color: active ? "white" : "black",
        backgroundColor: active ? "black" : "white",
        border: "1px solid black",
        borderRadius: 0,
        px: 2,
        py: 0.8,
        fontWeight: 700,
        textTransform: "none",
        boxShadow: "none",
        "&:hover": {
            backgroundColor: active ? "#222" : "#f2f2f2",
            boxShadow: "none",
        },
    });

    return (
        <AppBar
            position="sticky"
            elevation={0}
            sx={{
                top: 0,
                zIndex: 1200,
                backgroundColor: "white",
                color: "black",
                borderBottom: "2px solid black",
                boxShadow: "none",
            }}
        >
            <Toolbar
                sx={{
                    minHeight: "56px",
                    display: "flex",
                    justifyContent: "space-between",
                    gap: 2,
                    px: 2,
                }}
            >
                <Typography
                    variant="h6"
                    sx={{
                        fontWeight: 800,
                        whiteSpace: "nowrap",
                        color: "black",
                    }}
                >
                    Система протоколов
                </Typography>

                <Box
                    sx={{
                        display: "flex",
                        alignItems: "center",
                        gap: 1,
                    }}
                >
                    <Button
                        onClick={() => navigate("/protocols")}
                        sx={navButtonSx(isActive("/protocols"))}
                    >
                        Протоколы в работе
                    </Button>

                    <Button
                        onClick={() => navigate("/protocols/completed")}
                        sx={navButtonSx(isActive("/protocols/completed"))}
                    >
                        Завершенные протоколы
                    </Button>

                    <Button
                        onClick={handleLogout}
                        sx={{
                            color: "white",
                            backgroundColor: "black",
                            border: "1px solid black",
                            borderRadius: 0,
                            px: 2,
                            py: 0.8,
                            fontWeight: 700,
                            textTransform: "none",
                            boxShadow: "none",
                            "&:hover": {
                                backgroundColor: "#222",
                                boxShadow: "none",
                            },
                        }}
                    >
                        Выйти
                    </Button>
                </Box>
            </Toolbar>
        </AppBar>
    );
}

export default AppHeader;