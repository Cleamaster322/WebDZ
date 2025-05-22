import {useEffect, useState} from 'react'
import {useNavigate} from 'react-router-dom'

import api from "../../shared/api.jsx"
import Box from '@mui/material/Box'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'

function Login() {
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate()


    // Проверяем токены при загрузке страницы
    useEffect(() => {
        async function checkTokens() {
            setLoading(true)
            setError(null)
            const accessToken = localStorage.getItem('accessToken')
            const refreshToken = localStorage.getItem('refreshToken')

            if (!accessToken && !refreshToken) {
                setLoading(false)
                return // токенов нет, остаёмся на странице логина
            }

            try {
                // Пробуем вызвать защищённый эндпоинт, чтобы проверить accessToken
                // Например, GET /cars/protected/ - замените на ваш защищённый эндпоинт
                await api.get('/cars/brands/')

                // Если прошли - access валидный, редиректим
                navigate('/home')

            } catch (err) {
                // Если 401, пробуем обновить access с помощью refresh
                if (err.response?.status === 401 && refreshToken) {
                    try {
                        const response = await api.client.post(`${api.client.defaults.baseURL}cars/token/refresh/`, {refresh: refreshToken})
                        const newAccessToken = response.data.access
                        localStorage.setItem('accessToken', newAccessToken)
                        api.client.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`
                        navigate('/home')
                    } catch (refreshError) {
                        // Обновить токен не удалось, очищаем и остаёмся на странице логина
                        localStorage.removeItem('accessToken')
                        localStorage.removeItem('refreshToken')
                        setLoading(false)
                    }
                } else {
                    // Другие ошибки
                    setLoading(false)
                }
            }
        }

        checkTokens()
    }, [navigate])

    async function submitData() {
        setLoading(true)
        setError(null)
        try {
            const response = await api.post('/cars/token/', {username, password})
            if (response.status === 200) {
                localStorage.setItem("accessToken", response.data.access)
                localStorage.setItem("refreshToken", response.data.refresh)
                await api.setTokenAuth()
                navigate('/home')
            } else {
                setError('Ошибка авторизации')
            }
        } catch (e) {
            if (e.response?.status === 401) {
                setError('Неверный логин или пароль')
            } else {
                setError('Ошибка сети или сервер недоступен')
            }
        } finally {
            setLoading(false)
        }
    }


    return (
        <>
            <Box
                component='form'
                sx={{'& > :not(style)': {m: 1, width: '25ch'}}}
                noValidate
                autoComplete='off'
                onSubmit={e => {
                    e.preventDefault()
                    if (!loading) submitData()
                }}
            >
                <TextField
                    label='Логин'
                    variant='outlined'
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                    disabled={loading}
                />
                <TextField
                    label='Пароль'
                    variant='outlined'
                    type='password'
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    disabled={loading}
                />
                <Button
                    type='submit'
                    variant='contained'
                    disabled={loading || !username || !password}
                >
                    {loading ? 'Загрузка...' : 'Войти'}
                </Button>
                {error && <div style={{color: 'red'}}>{error}</div>}
            </Box>
        </>
    )
}

export default Login
