import {Autocomplete, TextField} from "@mui/material";
import {useState, useEffect} from "react";
import api from "../shared/api.jsx";
import {useNavigate} from "react-router-dom";
import Button from "@mui/material/Button";

function CarSelection() {
    const navigate = useNavigate();

    const [brands, setBrands] = useState([]);
    const [selectedBrand, setSelectedBrand] = useState(null);

    const [models, setModels] = useState([]);
    const [selectedModel, setSelectedModel] = useState(null);

    const [generations, setGenerations] = useState([]);
    const [selectedGeneration, setSelectedGeneration] = useState(null);

    const [configurations, setConfigurations] = useState([]);
    const [selectedConfiguration, setSelectedConfiguration] = useState(null);

    const [brandInputValue, setBrandInputValue] = useState("");
    const [modelInputValue, setModelInputValue] = useState("");
    const [generationInputValue, setGenerationInputValue] = useState("");
    const [configurationInputValue, setConfigurationInputValue] = useState("");

    const [brandLoading, setBrandLoading] = useState(false);
    const [modelLoading, setModelLoading] = useState(false);
    const [generationLoading, setGenerationLoading] = useState(false);
    const [configurationLoading, setConfigurationLoading] = useState(false);

    // Fetch brands
    useEffect(() => {
        const delayDebounceFn = setTimeout(() => {
            async function fetchBrands() {
                try {
                    setBrandLoading(true);
                    const params = brandInputValue ? {name: brandInputValue, page_size: 50} : {page_size: 50};
                    const response = await api.get("/cars/brands", {params});
                    setBrands(response.data.results);
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

    // Fetch models
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
                    const response = await api.get("/cars/models", {params});
                    setModels(response.data.results);
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

    // Fetch generations
    useEffect(() => {
        if (!selectedModel) {
            setGenerations([]);
            return;
        }

        const delayDebounceFn = setTimeout(() => {
            async function fetchGenerations() {
                try {
                    setGenerationLoading(true);
                    const params = generationInputValue
                        ? {model_id: selectedModel.id, name: generationInputValue, page_size: 50}
                        : {model_id: selectedModel.id, page_size: 50};
                    const response = await api.get("/cars/generations", {params});
                    setGenerations(response.data.results);
                } catch (error) {
                    console.error(error);
                    setGenerations([]);
                } finally {
                    setGenerationLoading(false);
                }
            }

            fetchGenerations();
        }, 300);

        return () => clearTimeout(delayDebounceFn);
    }, [selectedModel, generationInputValue]);

    // Fetch configurations
    useEffect(() => {
        if (!selectedGeneration) {
            setConfigurations([]);
            return;
        }

        const delayDebounceFn = setTimeout(() => {
            async function fetchConfigurations() {
                try {
                    setConfigurationLoading(true);
                    const params = configurationInputValue
                        ? {generation_id: selectedGeneration.id, name: configurationInputValue, page_size: 50}
                        : {generation_id: selectedGeneration.id, page_size: 50};
                    const response = await api.get("/cars/configurations", {params});
                    setConfigurations(response.data.results);
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
    }, [selectedGeneration, configurationInputValue]);

    const handleLogout = () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        api.client.defaults.headers.common["Authorization"] = null;
        navigate("/");
    };
    // Новая функция для перехода на другую страницу
    const handleNextPage = () => {
        navigate("/CarInfo", {state: {selectedBrand, selectedModel, selectedGeneration, selectedConfiguration}}); // замените на нужный путь
    };

    return (
        <div>
            <Button variant="outlined" color="error" onClick={handleLogout} sx={{marginBottom: 2}}>
                Выйти
            </Button>

            {/* Brand selection */}
            <Autocomplete
                value={selectedBrand}
                inputValue={brandInputValue}
                disablePortal
                options={brands}
                getOptionLabel={(option) => option.name || ""}
                loading={brandLoading}
                onInputChange={(event, newInputValue) => setBrandInputValue(newInputValue)}
                onChange={(event, newValue) => {
                    setSelectedBrand(newValue);
                    setSelectedModel(null);
                    setSelectedGeneration(null);
                    setSelectedConfiguration(null);
                    setModelInputValue("");
                    setGenerationInputValue("");
                    setConfigurationInputValue("");
                }}
                sx={{width: 400, marginBottom: 2}}
                renderInput={(params) => <TextField {...params} label="Выберите бренд"/>}
            />

            {/* Model selection */}
            {selectedBrand && (
                <Autocomplete
                    value={selectedModel}
                    inputValue={modelInputValue}
                    disablePortal
                    options={models}
                    getOptionLabel={(option) => option.name || ""}
                    loading={modelLoading}
                    onInputChange={(event, newInputValue) => setModelInputValue(newInputValue)}
                    onChange={(event, newValue) => {
                        setSelectedModel(newValue);
                        setSelectedGeneration(null);
                        setSelectedConfiguration(null);
                        setGenerationInputValue("");
                        setConfigurationInputValue("");
                    }}
                    sx={{width: 400, marginBottom: 2}}
                    renderInput={(params) => <TextField {...params} label="Выберите модель"/>}
                />
            )}

            {/* Generation selection */}
            {selectedModel && (
                generations.length > 0 ? (
                    <Autocomplete
                        value={selectedGeneration}
                        inputValue={generationInputValue}
                        disablePortal
                        options={generations}
                        getOptionLabel={(option) =>
                            `${option.name} (${option.date_start} - ${option.date_end})` || ""
                        }
                        loading={generationLoading}
                        onInputChange={(event, newInputValue) => setGenerationInputValue(newInputValue)}
                        onChange={(event, newValue) => {
                            setSelectedGeneration(newValue);
                            setSelectedConfiguration(null);
                            setConfigurationInputValue("");
                        }}
                        sx={{width: 400, marginTop: 2}}
                        renderInput={(params) => <TextField {...params} label="Выберите поколение"/>}
                    />
                ) : (
                    <TextField
                        disabled
                        label="Поколение"
                        value="Нет данных"
                        variant="outlined"
                        sx={{width: 400, marginTop: 2}}
                    />
                )
            )}

            {/* Configuration selection */}
            {selectedGeneration && (
                <Autocomplete
                    value={selectedConfiguration}
                    inputValue={configurationInputValue}
                    disablePortal
                    options={configurations}
                    getOptionLabel={(option) => option.name || ""}
                    loading={configurationLoading}
                    onInputChange={(event, newInputValue) => setConfigurationInputValue(newInputValue)}
                    onChange={(event, newValue) => setSelectedConfiguration(newValue)}
                    sx={{width: 400, marginTop: 2}}
                    renderInput={(params) => <TextField {...params} label="Выберите конфигурацию"/>}
                />
            )}
            {/* Новая кнопка для перехода */}
            <Button
                variant="contained"
                color="primary"
                onClick={handleNextPage}
                sx={{marginTop: 4}}
                disabled={!selectedConfiguration} // Можно заблокировать кнопку, если не выбрана конфигурация
            >
                Перейти на следующую страницу
            </Button>
        </div>
    );
}

export default CarSelection;
