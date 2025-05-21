import { Autocomplete, TextField } from "@mui/material";
import { useState, useEffect } from "react";
import api from "../shared/api.jsx";

function BrandsAndModels() {
  const [brands, setBrands] = useState([]);
  const [selectedBrand, setSelectedBrand] = useState(null);

  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);

  const [brandInputValue, setBrandInputValue] = useState("");
  const [brandLoading, setBrandLoading] = useState(false);
  const [modelLoading, setModelLoading] = useState(false);

  // get brands
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      async function fetchBrands() {
        try {
          setBrandLoading(true);

          const params = brandInputValue
            ? { name: brandInputValue, page_size: 50 }
            : { page_size: 50 };

          const response = await api.get("/cars/brand", { params });

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

        const response = await api.get("/cars/model", {
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

  return (
    <div>
      <Autocomplete
        disablePortal
        options={brands}
        getOptionLabel={(option) => option.name || ""} // объекты с name и id
        loading={brandLoading}
        onInputChange={(event, newInputValue) => {
          setBrandInputValue(newInputValue);
        }}
        onChange={(event, newValue) => {
          setSelectedBrand(newValue);
          setSelectedModel(null);
        }}
        sx={{ width: 300, marginBottom: 2 }}
        renderInput={(params) => (
          <TextField {...params} label="Выберите бренд" />
        )}
      />

      {selectedBrand && (
        <Autocomplete
          disablePortal
          options={models}
          getOptionLabel={(option) => option.name || ""}
          loading={modelLoading}
          onChange={(event, newValue) => {
            setSelectedModel(newValue); //
          }}
          sx={{ width: 300 }}
          renderInput={(params) => (
            <TextField {...params} label="Выберите модель" />
          )}
        />
      )}
    </div>
  );
}

export default BrandsAndModels;
