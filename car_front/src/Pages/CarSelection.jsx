import {
    Autocomplete,
    TextField,
    Box,
    Card,
    CardContent,
    CardMedia,
    Typography,
    CircularProgress,
    Chip,
    MenuItem,
    Button,
} from "@mui/material";
import {useState, useEffect} from "react";
import api from "../shared/api.jsx";
import {useNavigate} from "react-router-dom";

function getGenerationImageUrl(imagePath) {
    if (!imagePath) return "";

    if (imagePath.startsWith("http")) {
        return imagePath;
    }

    return `http://127.0.0.1:8000/${imagePath}`;
}

function getRegionLabel(region) {
    const labels = {
        japan: "Япония",
        china: "Китай",
        "south-korea": "Южная Корея",
        korea: "Корея",
        europe: "Европа",
        usa: "США",
        russia: "Россия",
    };

    return labels[region] || region || "Регион не указан";
}

function getGenerationTitle(generation) {
    const generationText = generation.generation_num
        ? `${generation.generation_num} поколение`
        : "Поколение";

    const restylingText = generation.restyling_num
        ? `, рестайлинг ${generation.restyling_num}`
        : "";

    return `${generationText}${restylingText}`;
}

function groupGenerationsByRegion(generations) {
    return generations.reduce((groups, generation) => {
        const region = generation.region || "unknown";

        if (!groups[region]) {
            groups[region] = [];
        }

        groups[region].push(generation);
        return groups;
    }, {});
}

function getBodyCodeOptions(generation) {
    if (!generation?.body_code) return [];

    return generation.body_code
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean)
        .sort((a, b) => a.localeCompare(b, "ru", {numeric: true}));
}

function buildCreateProtocolPayload({
    selectedBrand,
    selectedModel,
    selectedGeneration,
    selectedConfiguration,
}) {
    const payload = {
        owner_name: "Не указано",
        brand_name: selectedBrand?.name || "",
        commercial_name: selectedModel?.name || "",
        body_type: selectedGeneration?.body_type || "",
    };

    if (selectedConfiguration?.id) {
        payload.configuration_id = selectedConfiguration.id;
    }

    return payload;
}

function buildConfigurationLabel(option) {
    if (!option) return "";

    const parts = [];

    if (option.name) {
        parts.push(option.name);
    }

    if (option.engine_name) {
        parts.push(`двигатель: ${option.engine_name}`);
    }

    if (option.engine_model) {
        parts.push(`модель ДВС: ${option.engine_model}`);
    }

    if (option.engine_power_kw) {
        parts.push(`${option.engine_power_kw} кВт`);
    } else if (option.engine_power_hp) {
        parts.push(`${option.engine_power_hp} л.с.`);
    }

    if (option.fuel_type) {
        parts.push(option.fuel_type);
    }

    if (option.transmission) {
        parts.push(option.transmission);
    }

    if (option.drive_type) {
        parts.push(option.drive_type);
    }

    if (option.seats_count) {
        parts.push(`${option.seats_count} мест`);
    }

    const period = option.date_start || option.date_end
        ? ` (${option.date_start || "?"} - ${option.date_end || "?"})`
        : "";

    return `${parts.join(" · ")}${period}`;
}

function CarSelection() {
    const navigate = useNavigate();

    const emptyConfigurationFilterOptions = {
        drive_types: [],
        fuel_types: [],
        engine_models: [],
        transmissions: [],
        seats_counts: [],
        engine_powers_kw: [],
        engine_powers_hp: [],
    };

    const emptyConfigurationFilters = {
        drive_type: "",
        fuel_type: "",
        engine_model: "",
        transmission: "",
        seats_count: "",
        manufacture_year: "",
        body_code: "",
        engine_power: "",
        turbo_present: "",
    };

    const [brands, setBrands] = useState([]);
    const [selectedBrand, setSelectedBrand] = useState(null);

    const [models, setModels] = useState([]);
    const [selectedModel, setSelectedModel] = useState(null);

    const [generations, setGenerations] = useState([]);
    const [selectedGeneration, setSelectedGeneration] = useState(null);

    const [configurations, setConfigurations] = useState([]);
    const [selectedConfiguration, setSelectedConfiguration] = useState(null);

    const [creatingProtocol, setCreatingProtocol] = useState(false);
    const [createProtocolError, setCreateProtocolError] = useState("");

    const [configurationFilterOptions, setConfigurationFilterOptions] = useState(emptyConfigurationFilterOptions);
    const [configurationFilters, setConfigurationFilters] = useState(emptyConfigurationFilters);

    const [brandInputValue, setBrandInputValue] = useState("");
    const [modelInputValue, setModelInputValue] = useState("");
    const [configurationInputValue, setConfigurationInputValue] = useState("");

    const [brandLoading, setBrandLoading] = useState(false);
    const [modelLoading, setModelLoading] = useState(false);
    const [generationLoading, setGenerationLoading] = useState(false);
    const [configurationLoading, setConfigurationLoading] = useState(false);
    const [configurationFilterLoading, setConfigurationFilterLoading] = useState(false);

    useEffect(() => {
        const delayDebounceFn = setTimeout(() => {
            async function fetchBrands() {
                try {
                    setBrandLoading(true);

                    const params = brandInputValue
                        ? {name: brandInputValue, page_size: 50}
                        : {page_size: 50};

                    const response = await api.get("/cars/brands/", {params});
                    setBrands(response.data.results || []);
                } catch (error) {
                    console.error(error);
                    setBrands([]);
                } finally {
                    setBrandLoading(false);
                }
            }

            fetchBrands();
        }, 300);

        return () => clearTimeout(delayDebounceFn);
    }, [brandInputValue]);

    useEffect(() => {
        if (!selectedBrand) {
            setModels([]);
            return;
        }

        const delayDebounceFn = setTimeout(() => {
            async function fetchModels() {
                try {
                    setModelLoading(true);

                    const params = modelInputValue
                        ? {brand_id: selectedBrand.id, name: modelInputValue, page_size: 50}
                        : {brand_id: selectedBrand.id, page_size: 50};

                    const response = await api.get("/cars/models/", {params});
                    setModels(response.data.results || []);
                } catch (error) {
                    console.error(error);
                    setModels([]);
                } finally {
                    setModelLoading(false);
                }
            }

            fetchModels();
        }, 300);

        return () => clearTimeout(delayDebounceFn);
    }, [selectedBrand, modelInputValue]);

    useEffect(() => {
        if (!selectedModel) {
            setGenerations([]);
            return;
        }

        async function fetchGenerations() {
            try {
                setGenerationLoading(true);

                const response = await api.get("/cars/generations/", {
                    params: {
                        model_id: selectedModel.id,
                        page_size: 100,
                    },
                });

                setGenerations(response.data.results || []);
            } catch (error) {
                console.error(error);
                setGenerations([]);
            } finally {
                setGenerationLoading(false);
            }
        }

        fetchGenerations();
    }, [selectedModel]);

    useEffect(() => {
        if (!selectedGeneration) {
            setConfigurationFilterOptions(emptyConfigurationFilterOptions);
            return;
        }

        async function fetchConfigurationFilterOptions() {
            try {
                setConfigurationFilterLoading(true);

                const response = await api.get("/cars/configuration-filter-options/", {
                    params: {
                        generation_id: selectedGeneration.id,
                    },
                });

                setConfigurationFilterOptions({
                    ...emptyConfigurationFilterOptions,
                    ...(response.data || {}),
                });
            } catch (error) {
                console.error(error);
                setConfigurationFilterOptions(emptyConfigurationFilterOptions);
            } finally {
                setConfigurationFilterLoading(false);
            }
        }

        fetchConfigurationFilterOptions();
    }, [selectedGeneration]);

    useEffect(() => {
        if (!selectedGeneration) {
            setConfigurations([]);
            return;
        }

        const delayDebounceFn = setTimeout(() => {
            async function fetchConfigurations() {
                try {
                    setConfigurationLoading(true);

                    const params = {
                        generation_id: selectedGeneration.id,
                        page_size: 100,
                    };

                    if (configurationInputValue) {
                        params.name = configurationInputValue;
                    }

                    Object.entries(configurationFilters).forEach(([key, value]) => {
                        if (value !== "" && value !== null && value !== undefined) {
                            params[key] = value;
                        }
                    });

                    const response = await api.get("/cars/configurations-filtered/", {params});
                    setConfigurations(response.data.results || []);
                } catch (error) {
                    console.error(error);
                    setConfigurations([]);
                } finally {
                    setConfigurationLoading(false);
                }
            }

            fetchConfigurations();
        }, 300);

        return () => clearTimeout(delayDebounceFn);
    }, [selectedGeneration, configurationInputValue, configurationFilters]);

    const handleLogout = () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        delete api.client.defaults.headers.common["Authorization"];
        navigate("/");
    };

    const resetConfigurationFilters = () => {
        setConfigurationFilters(emptyConfigurationFilters);
        setSelectedConfiguration(null);
        setConfigurationInputValue("");
    };

    const handleConfigurationFilterChange = (field, value) => {
        setConfigurationFilters((prev) => ({
            ...prev,
            [field]: value,
        }));

        setSelectedConfiguration(null);
    };

    const handleSelectGeneration = (generation) => {
        setSelectedGeneration(generation);
        setSelectedConfiguration(null);
        setConfigurationInputValue("");
        setConfigurationFilters(emptyConfigurationFilters);
        setConfigurations([]);
    };

    const handleNextPage = async () => {
        if (!selectedBrand || !selectedModel) return;

        try {
            setCreatingProtocol(true);
            setCreateProtocolError("");

            const payload = buildCreateProtocolPayload({
                selectedBrand,
                selectedModel,
                selectedGeneration,
                selectedConfiguration,
            });

            const response = await api.post("/cars/protocols/create/", payload);
            const createdProtocol = response.data;

            navigate(`/protocols/${createdProtocol.id}/inspection`);
        } catch (error) {
            console.error(error);

            const backendError =
                error.response?.data?.configuration_id?.[0] ||
                error.response?.data?.configuration_id ||
                error.response?.data?.commercial_name?.[0] ||
                error.response?.data?.brand_name?.[0] ||
                error.response?.data?.error ||
                error.response?.data?.detail;

            setCreateProtocolError(
                backendError || "Не удалось создать протокол"
            );
        } finally {
            setCreatingProtocol(false);
        }
    };

    const groupedGenerations = groupGenerationsByRegion(generations);
    const bodyCodeOptions = getBodyCodeOptions(selectedGeneration);

    return (
        <Box sx={{padding: 3}}>
            <Button
                variant="outlined"
                color="error"
                onClick={handleLogout}
                sx={{marginBottom: 2}}
            >
                Выйти
            </Button>

            <Typography variant="h5" sx={{marginBottom: 3}}>
                Выбор автомобиля
            </Typography>

            <Autocomplete
                value={selectedBrand}
                inputValue={brandInputValue}
                disablePortal
                options={brands}
                getOptionLabel={(option) => option?.name || ""}
                isOptionEqualToValue={(option, value) => option.id === value.id}
                filterOptions={(options) => options}
                loading={brandLoading}
                onInputChange={(event, newInputValue) => setBrandInputValue(newInputValue)}
                onChange={(event, newValue) => {
                    setSelectedBrand(newValue);
                    setSelectedModel(null);
                    setSelectedGeneration(null);
                    setSelectedConfiguration(null);
                    setModels([]);
                    setGenerations([]);
                    setConfigurations([]);
                    setModelInputValue("");
                    setConfigurationInputValue("");
                    setConfigurationFilters(emptyConfigurationFilters);
                }}
                sx={{width: 400, marginBottom: 2}}
                renderInput={(params) => (
                    <TextField {...params} label="Выберите бренд"/>
                )}
            />

            {selectedBrand && (
                <Autocomplete
                    value={selectedModel}
                    inputValue={modelInputValue}
                    disablePortal
                    options={models}
                    getOptionLabel={(option) => option?.name || ""}
                    isOptionEqualToValue={(option, value) => option.id === value.id}
                    filterOptions={(options) => options}
                    loading={modelLoading}
                    onInputChange={(event, newInputValue) => setModelInputValue(newInputValue)}
                    onChange={(event, newValue) => {
                        setSelectedModel(newValue);
                        setSelectedGeneration(null);
                        setSelectedConfiguration(null);
                        setGenerations([]);
                        setConfigurations([]);
                        setConfigurationInputValue("");
                        setConfigurationFilters(emptyConfigurationFilters);
                    }}
                    sx={{width: 400, marginBottom: 3}}
                    renderInput={(params) => (
                        <TextField {...params} label="Выберите модель"/>
                    )}
                />
            )}

            {selectedModel && (
                <Box sx={{marginTop: 2}}>
                    <Typography variant="h6" sx={{marginBottom: 2}}>
                        Выберите поколение
                    </Typography>

                    {generationLoading && (
                        <Box sx={{display: "flex", alignItems: "center", gap: 1}}>
                            <CircularProgress size={22}/>
                            <Typography>Загрузка поколений...</Typography>
                        </Box>
                    )}

                    {!generationLoading && generations.length === 0 && (
                        <Typography color="text.secondary">
                            Нет данных по поколениям. Можно создать протокол по выбранной марке и модели и заполнить
                            данные вручную.
                        </Typography>
                    )}

                    {!generationLoading && Object.entries(groupedGenerations).map(([region, regionGenerations]) => (
                        <Box key={region} sx={{marginBottom: 4}}>
                            <Typography
                                variant="h6"
                                sx={{
                                    marginBottom: 2,
                                    fontWeight: 700,
                                }}
                            >
                                Модельный ряд {selectedBrand?.name} {selectedModel?.name} для {getRegionLabel(region)}
                            </Typography>

                            <Box
                                sx={{
                                    display: "grid",
                                    gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
                                    gap: 2,
                                    maxWidth: 1100,
                                }}
                            >
                                {regionGenerations.map((generation) => {
                                    const isSelected = selectedGeneration?.id === generation.id;

                                    return (
                                        <Card
                                            key={generation.id}
                                            onClick={() => handleSelectGeneration(generation)}
                                            sx={{
                                                cursor: "pointer",
                                                border: isSelected ? "2px solid #1976d2" : "1px solid #ddd",
                                                boxShadow: isSelected ? 4 : 1,
                                                transition: "0.2s",
                                                "&:hover": {
                                                    boxShadow: 4,
                                                    transform: "translateY(-2px)",
                                                },
                                            }}
                                        >
                                            {generation.image_path ? (
                                                <CardMedia
                                                    component="img"
                                                    height="150"
                                                    image={getGenerationImageUrl(generation.image_path)}
                                                    alt={generation.name}
                                                    sx={{
                                                        objectFit: "contain",
                                                        backgroundColor: "#f5f5f5",
                                                    }}
                                                />
                                            ) : (
                                                <Box
                                                    sx={{
                                                        height: 150,
                                                        display: "flex",
                                                        alignItems: "center",
                                                        justifyContent: "center",
                                                        backgroundColor: "#f5f5f5",
                                                        color: "text.secondary",
                                                    }}
                                                >
                                                    Нет изображения
                                                </Box>
                                            )}

                                            <CardContent>
                                                <Typography variant="subtitle1" fontWeight={600}>
                                                    {generation.name}
                                                </Typography>

                                                <Typography variant="body2" color="text.secondary">
                                                    {generation.date_start || "?"} - {generation.date_end || "?"}
                                                </Typography>

                                                <Box sx={{display: "flex", gap: 1, flexWrap: "wrap", marginTop: 1}}>
                                                    <Chip
                                                        size="small"
                                                        label={getRegionLabel(generation.region)}
                                                    />

                                                    {generation.body_type && (
                                                        <Chip
                                                            size="small"
                                                            label={generation.body_type}
                                                            variant="outlined"
                                                        />
                                                    )}
                                                </Box>

                                                <Typography variant="body2" sx={{marginTop: 1}}>
                                                    {getGenerationTitle(generation)}
                                                </Typography>

                                                {generation.body_code && (
                                                    <Typography variant="body2" color="text.secondary">
                                                        Код кузова: {generation.body_code}
                                                    </Typography>
                                                )}
                                            </CardContent>
                                        </Card>
                                    );
                                })}
                            </Box>
                        </Box>
                    ))}
                </Box>
            )}

            {selectedGeneration && (
                <Box sx={{marginTop: 4, maxWidth: 1200}}>
                    <Typography variant="h6" sx={{marginBottom: 2}}>
                        Фильтры комплектаций
                    </Typography>

                    {configurationFilterLoading && (
                        <Box sx={{display: "flex", alignItems: "center", gap: 1, marginBottom: 2}}>
                            <CircularProgress size={20}/>
                            <Typography>Загрузка фильтров...</Typography>
                        </Box>
                    )}

                    <Box
                        sx={{
                            display: "grid",
                            gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
                            gap: 2,
                            marginBottom: 2,
                        }}
                    >
                        <TextField
                            label="Год выпуска"
                            value={configurationFilters.manufacture_year}
                            onChange={(e) => handleConfigurationFilterChange("manufacture_year", e.target.value)}
                            size="small"
                            placeholder="Например 2021"
                        />

                        <TextField
                            select
                            label="Код кузова"
                            value={configurationFilters.body_code}
                            onChange={(e) => handleConfigurationFilterChange("body_code", e.target.value)}
                            size="small"
                            disabled={bodyCodeOptions.length === 0}
                        >
                            <MenuItem value="">Все</MenuItem>
                            {bodyCodeOptions.map((value) => (
                                <MenuItem key={value} value={value}>
                                    {value}
                                </MenuItem>
                            ))}
                        </TextField>

                        <TextField
                            select
                            label="Привод"
                            value={configurationFilters.drive_type}
                            onChange={(e) => handleConfigurationFilterChange("drive_type", e.target.value)}
                            size="small"
                        >
                            <MenuItem value="">Все</MenuItem>
                            {(configurationFilterOptions.drive_types || []).map((value) => (
                                <MenuItem key={value} value={value}>
                                    {value}
                                </MenuItem>
                            ))}
                        </TextField>

                        <TextField
                            select
                            label="Тип топлива"
                            value={configurationFilters.fuel_type}
                            onChange={(e) => handleConfigurationFilterChange("fuel_type", e.target.value)}
                            size="small"
                        >
                            <MenuItem value="">Все</MenuItem>
                            {(configurationFilterOptions.fuel_types || []).map((value) => (
                                <MenuItem key={value} value={value}>
                                    {value}
                                </MenuItem>
                            ))}
                        </TextField>

                        <TextField
                            select
                            label="Двигатель"
                            value={configurationFilters.engine_model}
                            onChange={(e) => handleConfigurationFilterChange("engine_model", e.target.value)}
                            size="small"
                        >
                            <MenuItem value="">Все</MenuItem>
                            {(configurationFilterOptions.engine_models || []).map((value) => (
                                <MenuItem key={value} value={value}>
                                    {value}
                                </MenuItem>
                            ))}
                        </TextField>

                        <TextField
                            select
                            label="Мощность"
                            value={configurationFilters.engine_power}
                            onChange={(e) => handleConfigurationFilterChange("engine_power", e.target.value)}
                            size="small"
                        >
                            <MenuItem value="">Все</MenuItem>

                            {(configurationFilterOptions.engine_powers_kw || []).map((value) => (
                                <MenuItem key={`kw-${value}`} value={value}>
                                    {value} кВт
                                </MenuItem>
                            ))}

                            {(configurationFilterOptions.engine_powers_hp || []).map((value) => (
                                <MenuItem key={`hp-${value}`} value={value}>
                                    {value} л.с.
                                </MenuItem>
                            ))}
                        </TextField>

                        <TextField
                            select
                            label="Тип коробки"
                            value={configurationFilters.transmission}
                            onChange={(e) => handleConfigurationFilterChange("transmission", e.target.value)}
                            size="small"
                        >
                            <MenuItem value="">Все</MenuItem>
                            {(configurationFilterOptions.transmissions || []).map((value) => (
                                <MenuItem key={value} value={value}>
                                    {value}
                                </MenuItem>
                            ))}
                        </TextField>

                        <TextField
                            select
                            label="Кол-во мест"
                            value={configurationFilters.seats_count}
                            onChange={(e) => handleConfigurationFilterChange("seats_count", e.target.value)}
                            size="small"
                        >
                            <MenuItem value="">Все</MenuItem>
                            {(configurationFilterOptions.seats_counts || []).map((value) => (
                                <MenuItem key={value} value={value}>
                                    {value}
                                </MenuItem>
                            ))}
                        </TextField>

                        <TextField
                            select
                            label="Турбонаддув"
                            value={configurationFilters.turbo_present}
                            onChange={(e) => handleConfigurationFilterChange("turbo_present", e.target.value)}
                            size="small"
                        >
                            <MenuItem value="">Все</MenuItem>
                            <MenuItem value="true">Есть</MenuItem>
                            <MenuItem value="false">Нет</MenuItem>
                        </TextField>
                    </Box>

                    <Button
                        variant="outlined"
                        onClick={resetConfigurationFilters}
                        sx={{marginBottom: 2}}
                    >
                        Сбросить фильтры комплектаций
                    </Button>

                    <Typography variant="body2" color="text.secondary" sx={{marginBottom: 1}}>
                        Найдено комплектаций: {configurations.length}
                    </Typography>

                    <Autocomplete
                        value={selectedConfiguration}
                        inputValue={configurationInputValue}
                        disablePortal
                        options={configurations}
                        getOptionLabel={buildConfigurationLabel}
                        isOptionEqualToValue={(option, value) => option.id === value.id}
                        filterOptions={(options) => options}
                        loading={configurationLoading}
                        onInputChange={(event, newInputValue) => setConfigurationInputValue(newInputValue)}
                        onChange={(event, newValue) => setSelectedConfiguration(newValue)}
                        sx={{width: 850, marginTop: 1}}
                        renderInput={(params) => (
                            <TextField
                                {...params}
                                label="Выберите конфигурацию"
                                placeholder="Можно искать по названию: X, Bolero, Highway Star..."
                            />
                        )}
                    />

                    {!configurationLoading && selectedGeneration && configurations.length === 0 && (
                        <Typography color="text.secondary" sx={{marginTop: 1}}>
                            По выбранным фильтрам комплектации не найдены. Можно создать пустой протокол и заполнить
                            данные вручную.
                        </Typography>
                    )}
                </Box>
            )}

            <Button
                variant="contained"
                color="primary"
                onClick={handleNextPage}
                sx={{marginTop: 4}}
                disabled={!selectedBrand || !selectedModel || creatingProtocol}
            >
                {creatingProtocol
                    ? "Создание протокола..."
                    : selectedConfiguration
                        ? "Создать протокол по выбранной комплектации"
                        : selectedGeneration
                            ? "Создать пустой протокол"
                            : "Создать протокол по марке и модели"}
            </Button>

            {createProtocolError && (
                <Typography color="error" sx={{marginTop: 2}}>
                    {createProtocolError}
                </Typography>
            )}
        </Box>
    );
}

export default CarSelection;