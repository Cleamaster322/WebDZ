import api from "../shared/api.jsx";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import MenuItem from "@mui/material/MenuItem";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Alert from "@mui/material/Alert";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";

function ProtocolInspection() {
    const { id } = useParams();

    const [protocol, setProtocol] = useState({
        appendix_number: "",
        commercial_name: "",
        vin: "",
        tire_marking: "",
        engine_number: "",
        registration_number: "",
        manufacture_year: "",
        color: "",
    });

    const [measurement, setMeasurement] = useState({
        wheel_formula: "",
        mufflers_count: "",
        seats_count: "",
        suspension_present: false,

        engine_layout: "",
        cylinder_layout: "",
        cylinders_count: "",
        fuel_type: "",
        turbo_present: false,
        transmission_type: "",

        tire_depth_fl_mm: "",
        tire_depth_fr_mm: "",
        tire_depth_rl_mm: "",
        tire_depth_rr_mm: "",

        bumper_to_body_distance_mm: "",
        protruding_elements_doors_mm: "",
        protruding_elements_other_mm: "",

        glass_transparency_left_pct: "",
        glass_transparency_right_pct: "",
        glass_transparency_windshield_pct: "",

        sun_strip_width_mm: "",
        steering_backlash_deg: "",
        speed_by_speedometer_kmh: "",
        actual_speed_kmh: "",
        exhaust_noise_db: "",
        co_min_pct: "",
        co_max_pct: "",

        light_absorption_1: "",
        light_absorption_2: "",
        light_absorption_3: "",
        light_absorption_4: "",
        light_absorption_5: "",
        light_absorption_6: "",

        vehicle_length_mm: "",
        vehicle_width_mm: "",
        vehicle_height_mm: "",
        vehicle_weight_kg: "",

        axle1_load_kg: "",
        axle2_load_kg: "",
        stand_axle1_load_kg: "",
        stand_axle2_load_kg: "",
    });

    const [brake, setBrake] = useState({
        service_brake_type: "",
        parking_brake_type: "",

        service_brake_control_force_axle1_n: "",
        service_brake_control_force_axle2_n: "",
        parking_brake_control_force_n: "",

        axle_1_brake_difference_pct: "",
        axle_2_brake_difference_pct: "",

        service_brake_front_left_kn: "",
        service_brake_front_right_kn: "",
        service_brake_rear_left_kn: "",
        service_brake_rear_right_kn: "",

        parking_brake_left_kn: "",
        parking_brake_right_kn: "",
    });

    const [light, setLight] = useState({
        low_beam_count: "",
        high_beam_count: "",
        front_fog_count: "",
        reverse_light_count: "",
        turn_signal_count: "",
        front_position_light_count: "",
        rear_position_light_count: "",
        main_brake_signal_count: "",
        additional_brake_signal_count: "",
        rear_fog_count: "",
        plate_light_count: "",
        daytime_running_light_count: "",
        parking_light_count: "",

        headlight_type: "halogen",

        low_beam_upper_point_mm: "",
        low_beam_lower_point_mm: "",

        fog_light_upper_point_mm: "",
        fog_light_lower_point_mm: "",
        fog_light_left_distance_mm: "",
        fog_light_right_distance_mm: "",

        brake_signal_upper_point_mm: "",
        brake_signal_lower_point_mm: "",
        brake_signal_left_distance_mm: "",
        brake_signal_right_distance_mm: "",

        additional_brake_signal_from_glass_edge_mm: "",
        additional_brake_signal_from_support_surface_mm: "",
        additional_brake_signal_optical_center_shift_mm: "",

        rear_fog_upper_point_mm: "",
        rear_fog_lower_point_mm: "",

        headlight_washer_present: false,

        left_34v_cd: "",
        left_52h_cd: "",
        left_high_beam_cd: "",
        right_34v_cd: "",
        right_52h_cd: "",
        right_high_beam_cd: "",

        turn_signal_frequency_per_min: "",
        turn_signal_frequency_hz: "",
    });

    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [successMessage, setSuccessMessage] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    useEffect(() => {
        loadProtocolData();
    }, [id]);

    const loadProtocolData = () => {
        setLoading(true);
        setErrorMessage("");

        api.get(`cars/protocols/${id}/full/`)
            .then((response) => {
                const data = response.data;

                if (data.protocol) {
                    setProtocol((prev) => ({
                        ...prev,
                        ...data.protocol,
                    }));
                }

                if (data.measurement) {
                    setMeasurement((prev) => ({
                        ...prev,
                        ...data.measurement,
                    }));
                }

                if (data.brake) {
                    setBrake((prev) => ({
                        ...prev,
                        ...data.brake,
                    }));
                }

                if (data.light) {
                    setLight((prev) => ({
                        ...prev,
                        ...data.light,
                    }));
                }
            })
            .catch((error) => {
                console.error("Ошибка загрузки протокола:", error);
                setErrorMessage("Не удалось загрузить данные протокола");
            })
            .finally(() => {
                setLoading(false);
            });
    };

    const handleProtocolChange = (e) => {
        const { name, value } = e.target;
        setProtocol((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleMeasurementChange = (e) => {
        const { name, value } = e.target;
        setMeasurement((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleBrakeChange = (e) => {
        const { name, value } = e.target;
        setBrake((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleLightChange = (e) => {
        const { name, value } = e.target;
        setLight((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleMeasurementCheckboxChange = (e) => {
        const { name, checked } = e.target;
        setMeasurement((prev) => ({
            ...prev,
            [name]: checked,
        }));
    };

    const handleLightCheckboxChange = (e) => {
        const { name, checked } = e.target;
        setLight((prev) => ({
            ...prev,
            [name]: checked,
        }));
    };

    const normalizePayload = (obj) => {
        const normalized = { ...obj };

        Object.keys(normalized).forEach((key) => {
            if (normalized[key] === "") {
                normalized[key] = null;
            }
        });

        return normalized;
    };

    const handleSave = () => {
        setSaving(true);
        setSuccessMessage("");
        setErrorMessage("");

        api.client.patch(`cars/protocols/${id}/update/`, normalizePayload(protocol))
            .then(() => api.client.patch(`cars/protocols/${id}/measurement/update/`, normalizePayload(measurement)))
            .then(() => api.client.patch(`cars/protocols/${id}/brake/update/`, normalizePayload(brake)))
            .then(() => api.client.patch(`cars/protocols/${id}/light/update/`, normalizePayload(light)))
            .then(() => {
                setSuccessMessage("Данные осмотра успешно сохранены");
            })
            .catch((error) => {
                console.error("Ошибка сохранения:", error);
                setErrorMessage("Ошибка при сохранении данных");
            })
            .finally(() => {
                setSaving(false);
            });
    };

    const handleGenerateDocx = async () => {
  try {
    const response = await api.generateProtocolDocx(id)

    const blob = new Blob(
      [response.data],
      {
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      }
    )

    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `protocol_${id}.docx`
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Ошибка генерации DOCX:', error)
  }
}

    const textFieldSx = {
        "& .MuiInputBase-input": {
            color: "black",
        },
        "& .MuiInputLabel-root": {
            color: "black",
            whiteSpace: "normal",
            lineHeight: 1.2,
            maxWidth: "90%",
            top: "50%",
            transform: "translate(14px, -50%)",
        },
        "& .MuiInputLabel-shrink": {
            top: 0,
            transform: "translate(14px, -9px) scale(0.75)",
        },
        "& .MuiOutlinedInput-notchedOutline": {
            borderColor: "#bdbdbd",
        },
        "& .MuiInputLabel-root.Mui-focused": {
            color: "black",
        },
        "& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: "black",
        },
        "& .MuiOutlinedInput-root": {
            minHeight: 70,
            alignItems: "center",
            backgroundColor: "white",
        },
    };

    const selectFieldSx = {
        "& .MuiInputBase-input": {
            color: "black",
            paddingTop: "16px",
            paddingBottom: "16px",
        },
        "& .MuiOutlinedInput-notchedOutline": {
            borderColor: "#bdbdbd",
        },
        "& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: "black",
        },
        "& .MuiOutlinedInput-root": {
            minHeight: 56,
            backgroundColor: "white",
        },
    };

    const sectionPaperSx = {
        p: 3,
        borderRadius: 2,
        backgroundColor: "white",
        boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
    };

    const fieldLabelSx = {
        mb: 1,
        fontSize: 14,
        fontWeight: 500,
        color: "black",
        lineHeight: 1.3,
    };

    return (
        <Box
            sx={{
                width: "100%",
                minHeight: "100vh",
                backgroundColor: "white",
                color: "black",
                py: 4,
                px: 3,
            }}
        >
            <Box
                sx={{
                    width: "100%",
                    maxWidth: 1400,
                    mx: "auto",
                    display: "flex",
                    flexDirection: "column",
                    gap: 3,
                }}
            >
                <Typography variant="h4" sx={{ color: "black", fontWeight: 700 }}>
                    Осмотр автомобиля — протокол #{id}
                </Typography>

                {loading && <Alert severity="info">Загрузка данных...</Alert>}
                {successMessage && <Alert severity="success">{successMessage}</Alert>}
                {errorMessage && <Alert severity="error">{errorMessage}</Alert>}

                <Paper sx={sectionPaperSx}>
                    <Typography variant="h5" sx={{ mb: 3, color: "black", fontWeight: 600 }}>
                        1. Шапка и основные сведения
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6}>
                            <TextField
                                label="Приложение к технической записи №"
                                name="appendix_number"
                                value={protocol.appendix_number ?? ""}
                                onChange={handleProtocolChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={6}>
                            <TextField
                                label="Марка, коммерческое название"
                                name="commercial_name"
                                value={protocol.commercial_name ?? ""}
                                onChange={handleProtocolChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12}>
                            <TextField
                                label="VIN (№ кузова/шасси)"
                                name="vin"
                                value={protocol.vin ?? ""}
                                onChange={handleProtocolChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={6}>
                            <TextField
                                label="Маркировка колес"
                                name="tire_marking"
                                value={protocol.tire_marking ?? ""}
                                onChange={handleProtocolChange}
                                fullWidth
                                sx={textFieldSx}
                                placeholder="Например: 185/65R15"
                            />
                        </Grid>

                        <Grid item xs={12} md={3}>
                            <TextField
                                label="Год выпуска"
                                name="manufacture_year"
                                value={protocol.manufacture_year ?? ""}
                                onChange={handleProtocolChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={3}>
                            <TextField
                                label="Цвет"
                                name="color"
                                value={protocol.color ?? ""}
                                onChange={handleProtocolChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Конструктивные параметры
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={4}>
                            <Typography sx={fieldLabelSx}>Колесная формула</Typography>
                            <TextField
                                select
                                name="wheel_formula"
                                value={measurement.wheel_formula ?? ""}
                                onChange={handleMeasurementChange}
                                fullWidth
                                size="small"
                                sx={selectFieldSx}
                            >
                                <MenuItem value="4x2_front">4x2 передний</MenuItem>
                                <MenuItem value="4x2_rear">4x2 задний</MenuItem>
                                <MenuItem value="4x4">4x4 полный</MenuItem>
                            </TextField>
                        </Grid>

                        <Grid item xs={12} md={4}>
                            <TextField
                                label="Количество глушителей"
                                name="mufflers_count"
                                value={measurement.mufflers_count ?? ""}
                                onChange={handleMeasurementChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={4}>
                            <TextField
                                label="Количество посадочных мест"
                                name="seats_count"
                                value={measurement.seats_count ?? ""}
                                onChange={handleMeasurementChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={Boolean(measurement.suspension_present)}
                                        onChange={handleMeasurementCheckboxChange}
                                        name="suspension_present"
                                        sx={{ color: "black" }}
                                    />
                                }
                                label="Подвеска: наличие"
                                sx={{ color: "black" }}
                            />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Двигатель
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6}>
                            <Typography sx={fieldLabelSx}>Расположение двигателя</Typography>
                            <TextField
                                select
                                name="engine_layout"
                                value={measurement.engine_layout ?? ""}
                                onChange={handleMeasurementChange}
                                fullWidth
                                size="small"
                                sx={selectFieldSx}
                            >
                                <MenuItem value="transverse">Поперечное</MenuItem>
                                <MenuItem value="longitudinal">Продольное</MenuItem>
                            </TextField>
                        </Grid>

                        <Grid item xs={12} md={6}>
                            <Typography sx={fieldLabelSx}>Расположение цилиндров</Typography>
                            <TextField
                                select
                                name="cylinder_layout"
                                value={measurement.cylinder_layout ?? ""}
                                onChange={handleMeasurementChange}
                                fullWidth
                                size="small"
                                sx={selectFieldSx}
                            >
                                <MenuItem value="inline">Рядное</MenuItem>
                                <MenuItem value="opposed">Оппозитное</MenuItem>
                                <MenuItem value="v_shape">V-образное</MenuItem>
                            </TextField>
                        </Grid>

                        <Grid item xs={12} md={4}>
                            <TextField
                                label="Количество цилиндров"
                                name="cylinders_count"
                                value={measurement.cylinders_count ?? ""}
                                onChange={handleMeasurementChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={4}>
                            <Typography sx={fieldLabelSx}>Вид топлива</Typography>
                            <TextField
                                select
                                name="fuel_type"
                                value={measurement.fuel_type ?? ""}
                                onChange={handleMeasurementChange}
                                fullWidth
                                size="small"
                                sx={selectFieldSx}
                            >
                                <MenuItem value="petrol">Бензин</MenuItem>
                                <MenuItem value="diesel">Дизель</MenuItem>
                                <MenuItem value="hybrid">Гибрид</MenuItem>
                                <MenuItem value="electric">Электро</MenuItem>
                                <MenuItem value="other">Другое</MenuItem>
                            </TextField>
                        </Grid>

                        <Grid item xs={12} md={4}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={Boolean(measurement.turbo_present)}
                                        onChange={handleMeasurementCheckboxChange}
                                        name="turbo_present"
                                        sx={{ color: "black" }}
                                    />
                                }
                                label="Турбонаддув: наличие"
                                sx={{ color: "black" }}
                            />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Трансмиссия
                    </Typography>

                    <Grid container spacing={2}>
                        <Grid item xs={12} md={6}>
                            <Typography sx={fieldLabelSx}>Тип трансмиссии</Typography>
                            <TextField
                                select
                                name="transmission_type"
                                value={measurement.transmission_type ?? ""}
                                onChange={handleMeasurementChange}
                                fullWidth
                                size="small"
                                sx={selectFieldSx}
                            >
                                <MenuItem value="automatic">Автомат</MenuItem>
                                <MenuItem value="cvt">Вариатор</MenuItem>
                                <MenuItem value="manual">Механика</MenuItem>
                                <MenuItem value="robot">Робот</MenuItem>
                                <MenuItem value="reducer">Редуктор</MenuItem>
                                <MenuItem value="other">Другое</MenuItem>
                            </TextField>
                        </Grid>
                    </Grid>
                </Paper>

                <Paper sx={sectionPaperSx}>
                    <Typography variant="h5" sx={{ mb: 3, color: "black", fontWeight: 600 }}>
                        2. Тормозная система
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6}>
                            <Typography sx={fieldLabelSx}>Рабочая тормозная система</Typography>
                            <TextField
                                select
                                name="service_brake_type"
                                value={brake.service_brake_type ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                size="small"
                                sx={selectFieldSx}
                            >
                                <MenuItem value="disc_disc">Дисковая/дисковая</MenuItem>
                                <MenuItem value="disc_drum">Дисковая/барабанная</MenuItem>
                                <MenuItem value="other">Другое</MenuItem>
                            </TextField>
                        </Grid>

                        <Grid item xs={12} md={6}>
                            <Typography sx={fieldLabelSx}>Стояночная тормозная система</Typography>
                            <TextField
                                select
                                name="parking_brake_type"
                                value={brake.parking_brake_type ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                size="small"
                                sx={selectFieldSx}
                            >
                                <MenuItem value="mechanical_hand">Механический ручной</MenuItem>
                                <MenuItem value="mechanical_pedal">Механический педаль</MenuItem>
                                <MenuItem value="electric">Электрический</MenuItem>
                                <MenuItem value="other">Другое</MenuItem>
                            </TextField>
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Усилие на органе управления
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={4}>
                            <TextField
                                label="Рабочая тормозная система: ось 1, Н"
                                name="service_brake_control_force_axle1_n"
                                value={brake.service_brake_control_force_axle1_n ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={4}>
                            <TextField
                                label="Рабочая тормозная система: ось 2, Н"
                                name="service_brake_control_force_axle2_n"
                                value={brake.service_brake_control_force_axle2_n ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={4}>
                            <TextField
                                label="Стояночная тормозная система, Н"
                                name="parking_brake_control_force_n"
                                value={brake.parking_brake_control_force_n ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Относительная разность тормозных сил
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6}>
                            <TextField
                                label="Ось 1, %"
                                name="axle_1_brake_difference_pct"
                                value={brake.axle_1_brake_difference_pct ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={6}>
                            <TextField
                                label="Ось 2, %"
                                name="axle_2_brake_difference_pct"
                                value={brake.axle_2_brake_difference_pct ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Удельная тормозная сила рабочей тормозной системы
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6} lg={3}>
                            <TextField
                                label="Переднее левое, кН"
                                name="service_brake_front_left_kn"
                                value={brake.service_brake_front_left_kn ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={6} lg={3}>
                            <TextField
                                label="Переднее правое, кН"
                                name="service_brake_front_right_kn"
                                value={brake.service_brake_front_right_kn ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={6} lg={3}>
                            <TextField
                                label="Заднее левое, кН"
                                name="service_brake_rear_left_kn"
                                value={brake.service_brake_rear_left_kn ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={6} lg={3}>
                            <TextField
                                label="Заднее правое, кН"
                                name="service_brake_rear_right_kn"
                                value={brake.service_brake_rear_right_kn ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Удельная тормозная сила стояночной тормозной системы
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6}>
                            <TextField
                                label="Заднее левое, кН"
                                name="parking_brake_left_kn"
                                value={brake.parking_brake_left_kn ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={6}>
                            <TextField
                                label="Заднее правое, кН"
                                name="parking_brake_right_kn"
                                value={brake.parking_brake_right_kn ?? ""}
                                onChange={handleBrakeChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Нагрузка на ось (стенд)
                    </Typography>

                    <Grid container spacing={2}>
                        <Grid item xs={12} md={6}>
                            <TextField
                                label="Ось 1, кг"
                                name="stand_axle1_load_kg"
                                value={measurement.stand_axle1_load_kg ?? ""}
                                onChange={handleMeasurementChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>

                        <Grid item xs={12} md={6}>
                            <TextField
                                label="Ось 2, кг"
                                name="stand_axle2_load_kg"
                                value={measurement.stand_axle2_load_kg ?? ""}
                                onChange={handleMeasurementChange}
                                fullWidth
                                sx={textFieldSx}
                            />
                        </Grid>
                    </Grid>
                </Paper>

                <Paper sx={sectionPaperSx}>
                    <Typography variant="h5" sx={{ mb: 3, color: "black", fontWeight: 600 }}>
                        3. Осветительные приборы
                    </Typography>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Внешние световые приборы (количество)
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="Фара ближнего света" name="low_beam_count" value={light.low_beam_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="Фара дальнего света" name="high_beam_count" value={light.high_beam_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="Передняя ПТФ" name="front_fog_count" value={light.front_fog_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="Фонарь заднего хода" name="reverse_light_count" value={light.reverse_light_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="Указатели поворота" name="turn_signal_count" value={light.turn_signal_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="Передний габаритный огонь" name="front_position_light_count" value={light.front_position_light_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="Задний габаритный огонь" name="rear_position_light_count" value={light.rear_position_light_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="Сигнал торможения основной" name="main_brake_signal_count" value={light.main_brake_signal_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="Сигнал торможения дополнительный" name="additional_brake_signal_count" value={light.additional_brake_signal_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="Задний ПТФ" name="rear_fog_count" value={light.rear_fog_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="Подсветка госномера" name="plate_light_count" value={light.plate_light_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="ДХО" name="daytime_running_light_count" value={light.daytime_running_light_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={3}>
                            <TextField label="Стояночные огни" name="parking_light_count" value={light.parking_light_count ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Тип фар
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6}>
                            <Typography sx={fieldLabelSx}>Тип фар</Typography>
                            <TextField
                                select
                                name="headlight_type"
                                value={light.headlight_type ?? ""}
                                onChange={handleLightChange}
                                fullWidth
                                size="small"
                                sx={selectFieldSx}
                            >
                                <MenuItem value="halogen">Галоген</MenuItem>
                                <MenuItem value="xenon">Ксенон</MenuItem>
                                <MenuItem value="led">LED</MenuItem>
                                <MenuItem value="other">Другое</MenuItem>
                            </TextField>
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Установка фар ближнего света
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6}>
                            <TextField label="Верхняя точка, мм" name="low_beam_upper_point_mm" value={light.low_beam_upper_point_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Нижняя точка, мм" name="low_beam_lower_point_mm" value={light.low_beam_lower_point_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Установка ПТФ
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6}>
                            <TextField label="Верхняя точка, мм" name="fog_light_upper_point_mm" value={light.fog_light_upper_point_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Нижняя точка, мм" name="fog_light_lower_point_mm" value={light.fog_light_lower_point_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Левая, мм" name="fog_light_left_distance_mm" value={light.fog_light_left_distance_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Правая, мм" name="fog_light_right_distance_mm" value={light.fog_light_right_distance_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Установка основных сигналов торможения
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6}>
                            <TextField label="Верхняя точка, мм" name="brake_signal_upper_point_mm" value={light.brake_signal_upper_point_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Нижняя точка, мм" name="brake_signal_lower_point_mm" value={light.brake_signal_lower_point_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Левая, мм" name="brake_signal_left_distance_mm" value={light.brake_signal_left_distance_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Правая, мм" name="brake_signal_right_distance_mm" value={light.brake_signal_right_distance_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Установка дополнительного сигнала торможения
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={4}>
                            <TextField label="От нижнего края покрытия заднего стекла, мм" name="additional_brake_signal_from_glass_edge_mm" value={light.additional_brake_signal_from_glass_edge_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <TextField label="От уровня опорной поверхности, мм" name="additional_brake_signal_from_support_surface_mm" value={light.additional_brake_signal_from_support_surface_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <TextField label="Смещение оптического центра, мм" name="additional_brake_signal_optical_center_shift_mm" value={light.additional_brake_signal_optical_center_shift_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Установка задних ПТФ
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6}>
                            <TextField label="Верхняя точка, мм" name="rear_fog_upper_point_mm" value={light.rear_fog_upper_point_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Нижняя точка, мм" name="rear_fog_lower_point_mm" value={light.rear_fog_lower_point_mm ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Омыватели фар
                    </Typography>

                    <Box sx={{ mb: 4 }}>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={Boolean(light.headlight_washer_present)}
                                    onChange={handleLightCheckboxChange}
                                    name="headlight_washer_present"
                                    sx={{ color: "black" }}
                                />
                            }
                            label="Омыватели фар: наличие"
                            sx={{ color: "black" }}
                        />
                    </Box>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Сила света фар
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={4} lg={2}>
                            <TextField label="Левая 34V, кд" name="left_34v_cd" value={light.left_34v_cd ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={2}>
                            <TextField label="Левая 52H, кд" name="left_52h_cd" value={light.left_52h_cd ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={2}>
                            <TextField label="Левая дальний, кд" name="left_high_beam_cd" value={light.left_high_beam_cd ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={2}>
                            <TextField label="Правая 34V, кд" name="right_34v_cd" value={light.right_34v_cd ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={2}>
                            <TextField label="Правая 52H, кд" name="right_52h_cd" value={light.right_52h_cd ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4} lg={2}>
                            <TextField label="Правая дальний, кд" name="right_high_beam_cd" value={light.right_high_beam_cd ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Частота мерцания указателей поворота
                    </Typography>

                    <Grid container spacing={2}>
                        <Grid item xs={12} md={6}>
                            <TextField label="Пр/мин" name="turn_signal_frequency_per_min" value={light.turn_signal_frequency_per_min ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Гц" name="turn_signal_frequency_hz" value={light.turn_signal_frequency_hz ?? ""} onChange={handleLightChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>
                </Paper>

                <Paper sx={sectionPaperSx}>
                    <Typography variant="h5" sx={{ mb: 3, color: "black", fontWeight: 600 }}>
                        4. Прочее
                    </Typography>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Остаточная глубина рисунка протектора
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6} lg={3}>
                            <TextField label="Левое переднее" name="tire_depth_fl_mm" value={measurement.tire_depth_fl_mm ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6} lg={3}>
                            <TextField label="Правое переднее" name="tire_depth_fr_mm" value={measurement.tire_depth_fr_mm ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6} lg={3}>
                            <TextField label="Левое заднее" name="tire_depth_rl_mm" value={measurement.tire_depth_rl_mm ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6} lg={3}>
                            <TextField label="Правое заднее" name="tire_depth_rr_mm" value={measurement.tire_depth_rr_mm ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Кузов и выступающие элементы
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12}>
                            <TextField label="Расстояние между краем бампера и кузовом, мм" name="bumper_to_body_distance_mm" value={measurement.bumper_to_body_distance_mm ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Ручки дверей, багажника, мм" name="protruding_elements_doors_mm" value={measurement.protruding_elements_doors_mm ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Остальные элементы, мм" name="protruding_elements_other_mm" value={measurement.protruding_elements_other_mm ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Светопропускание стекол
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={4}>
                            <TextField label="Правое, %" name="glass_transparency_right_pct" value={measurement.glass_transparency_right_pct ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <TextField label="Левое, %" name="glass_transparency_left_pct" value={measurement.glass_transparency_left_pct ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <TextField label="Ветровое, %" name="glass_transparency_windshield_pct" value={measurement.glass_transparency_windshield_pct ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Прочие параметры
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={6}>
                            <TextField label="Ширина светозащитной полосы, мм" name="sun_strip_width_mm" value={measurement.sun_strip_width_mm ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Суммарный люфт рулевого управления, °" name="steering_backlash_deg" value={measurement.steering_backlash_deg ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Скорость по спидометру, км/ч" name="speed_by_speedometer_kmh" value={measurement.speed_by_speedometer_kmh ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Фактическая скорость, км/ч" name="actual_speed_kmh" value={measurement.actual_speed_kmh ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <TextField label="Уровень шума отработавших газов, дБА" name="exhaust_noise_db" value={measurement.exhaust_noise_db ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <TextField label="Min обор: CO, %" name="co_min_pct" value={measurement.co_min_pct ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={4}>
                            <TextField label="Max обор: CO, %" name="co_max_pct" value={measurement.co_max_pct ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Коэффициент поглощения света
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={4} lg={2}><TextField label="1" name="light_absorption_1" value={measurement.light_absorption_1 ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} /></Grid>
                        <Grid item xs={12} md={4} lg={2}><TextField label="2" name="light_absorption_2" value={measurement.light_absorption_2 ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} /></Grid>
                        <Grid item xs={12} md={4} lg={2}><TextField label="3" name="light_absorption_3" value={measurement.light_absorption_3 ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} /></Grid>
                        <Grid item xs={12} md={4} lg={2}><TextField label="4" name="light_absorption_4" value={measurement.light_absorption_4 ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} /></Grid>
                        <Grid item xs={12} md={4} lg={2}><TextField label="5" name="light_absorption_5" value={measurement.light_absorption_5 ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} /></Grid>
                        <Grid item xs={12} md={4} lg={2}><TextField label="6" name="light_absorption_6" value={measurement.light_absorption_6 ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} /></Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Габаритные размеры ТС
                    </Typography>

                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        <Grid item xs={12} md={3}>
                            <TextField label="Длина, мм" name="vehicle_length_mm" value={measurement.vehicle_length_mm ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={3}>
                            <TextField label="Ширина, мм" name="vehicle_width_mm" value={measurement.vehicle_width_mm ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={3}>
                            <TextField label="Высота, мм" name="vehicle_height_mm" value={measurement.vehicle_height_mm ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={3}>
                            <TextField label="Масса ТС, кг" name="vehicle_weight_kg" value={measurement.vehicle_weight_kg ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>

                    <Typography variant="h6" sx={{ mb: 2, color: "black" }}>
                        Нагрузка на ось
                    </Typography>

                    <Grid container spacing={2}>
                        <Grid item xs={12} md={6}>
                            <TextField label="Ось 1, кг" name="axle1_load_kg" value={measurement.axle1_load_kg ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <TextField label="Ось 2, кг" name="axle2_load_kg" value={measurement.axle2_load_kg ?? ""} onChange={handleMeasurementChange} fullWidth sx={textFieldSx} />
                        </Grid>
                    </Grid>
                </Paper>

                <Box sx={{ display: "flex", justifyContent: "flex-end", pb: 2 }}>
                    <Button
                        variant="contained"
                        onClick={handleGenerateDocx}
                        disabled={saving || loading}
                        sx={{
                            px: 4,
                            py: 1.2,
                            backgroundColor: "black",
                            color: "white",
                            "&:hover": {
                                backgroundColor: "#222",
                            },
                        }}
                    >
                        {saving ? "Сохранение..." : "Сохранить"}
                    </Button>
                </Box>
            </Box>
        </Box>
    );
}

export default ProtocolInspection;