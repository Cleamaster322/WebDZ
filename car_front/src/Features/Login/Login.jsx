import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../../shared/api.jsx";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";

function Login() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const accessToken = localStorage.getItem("accessToken");
        const refreshToken = localStorage.getItem("refreshToken");

        if (accessToken || refreshToken) {
            api.get("/cars/brands/")
                .then(() => {
                    navigate("/home");
                })
                .catch(() => {
                    localStorage.removeItem("accessToken");
                    localStorage.removeItem("refreshToken");
                });
        }
    }, [navigate]);

    async function submitData() {
        setLoading(true);
        setError(null);

        try {
            const response = await api.post("/cars/token/", { username, password });

            if (response.status === 200) {
                localStorage.setItem("accessToken", response.data.access);
                localStorage.setItem("refreshToken", response.data.refresh);
                await api.setTokenAuth();
                navigate("/home");
            } else {
                setError("Ошибка авторизации");
            }
        } catch (e) {
            if (e.response?.status === 401) {
                setError("Неверный логин или пароль");
            } else {
                setError("Ошибка сети или сервер недоступен");
            }
        } finally {
            setLoading(false);
        }
    }

    return (
        <Box
            component="form"
            sx={{ "& > :not(style)": { m: 1, width: "25ch" } }}
            noValidate
            autoComplete="off"
            onSubmit={(e) => {
                e.preventDefault();
                if (!loading) submitData();
            }}
        >
            <TextField
                label="Логин"
                variant="outlined"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading}
            />
            <TextField
                label="Пароль"
                variant="outlined"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
            />
            <Button type="submit" variant="contained" disabled={loading || !username || !password}>
                {loading ? "Загрузка..." : "Войти"}
            </Button>
            {error && <div style={{ color: "red" }}>{error}</div>}
        </Box>
    );
}

export default Login;