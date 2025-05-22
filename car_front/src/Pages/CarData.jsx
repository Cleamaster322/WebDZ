import { Autocomplete, TextField } from "@mui/material";
import { useState, useEffect } from "react";
import api from "../shared/api.jsx";
import {useNavigate} from "react-router-dom";
import Button from "@mui/material/Button";

function BrandsAndModels() {
   const navigate = useNavigate();

  const [brands, setBrands] = useState([]);
  const [selectedBrand, setSelectedBrand] = useState(null);

  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);

  const [generations, setGenerations] = useState([]);
  const [selectedGeneration, setSelectedGeneration] = useState(null);

  const [brandInputValue, setBrandInputValue] = useState("");
  const [brandLoading, setBrandLoading] = useState(false);
  const [modelLoading, setModelLoading] = useState(false);
  const [generationLoading, setGenerationLoading] = useState(false);

  // get brands
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      async function fetchBrands() {
        try {
          setBrandLoading(true);

          const params = brandInputValue
            ? { name: brandInputValue, page_size: 50 }
            : { page_size: 50 };

          const response = await api.get("/cars/brands", { params });

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

  // get model by brand_id
  useEffect(() => {
    async function fetchModels() {
      if (!selectedBrand) {
        setModels([]);
        return;
      }

      try {
        setModelLoading(true);

        const response = await api.get("/cars/models", {
          params: {
            brand_id: selectedBrand.id, //
            page_size: 100,
          },
        });

        setModels(response.data.results);
      } catch (error) {
        console.error(error);
        setModels([]);
      } finally {
        setModelLoading(false);
      }
    }

    fetchModels();
  }, [selectedBrand]);

  // --- Fetch generations by model_id ---
  useEffect(() => {
    async function fetchGenerations() {
      if (!selectedModel) {
        setGenerations([]);
        return;
      }

      try {
        setGenerationLoading(true);
        const response = await api.get("/cars/generations", {
          params: { model_id: selectedModel.id, page_size: 100 },
        });
        setGenerations(response.data.results);
      } catch (error) {
        console.error(error);
        setGenerations([]);
      } finally {
        setGenerationLoading(false);
      }
    }

    fetchGenerations();
  }, [selectedModel]);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    // Если в api есть установка токена — можно её тоже очистить
    api.client.defaults.headers.common['Authorization'] = null;
    // Перейти на логин
    navigate('/');
  };

  return (
    <div>
      <Button
        variant="outlined"
        color="error"
        onClick={handleLogout}
        sx={{ marginBottom: 2 }}
      >
        Выйти
      </Button>

      {/* Brand selection */}
      <Autocomplete
        disablePortal
        options={brands}
        getOptionLabel={(option) => option.name || ""}
        loading={brandLoading}
        onInputChange={(event, newInputValue) => {
          setBrandInputValue(newInputValue);
        }}
        onChange={(event, newValue) => {
          setSelectedBrand(newValue);
          setSelectedModel(null);
          setSelectedGeneration(null);
        }}
        sx={{ width: 400, marginBottom: 2 }}
        renderInput={(params) => (
          <TextField {...params} label="Выберите бренд" />
        )}
      />

      {/* Model selection */}
      {selectedBrand && (
        <Autocomplete
          disablePortal
          options={models}
          getOptionLabel={(option) => option.name || ""}
          loading={modelLoading}
          onChange={(event, newValue) => {
            setSelectedModel(newValue);
            setSelectedGeneration(null);
          }}
          sx={{ width: 400, marginBottom: 2 }}
          renderInput={(params) => (
            <TextField {...params} label="Выберите модель" />
          )}
        />
      )}

      {/* Generation selection */}
      {selectedModel && (
        generations.length > 0 ? (
          <Autocomplete
          disablePortal
          options={generations}
          getOptionLabel={(option) => `${option.name} (${option.date_start} - ${option.date_end})` || ""}
          loading={generationLoading}
          onChange={(event, newValue) => {
            setSelectedGeneration(newValue);
          }}
          sx={{ width: 400, marginTop: 2 }}
          renderInput={(params) => (
            <TextField {...params} label="Выберите поколение" />
          )}
        />
      ) : (
    <TextField
      disabled
      label="Поколение"
      value="Нет данных"
      variant="outlined"
      sx={{ width: 400, marginTop: 2 }}
    />
  )
)}

    </div>
  );
}

export default BrandsAndModels;
