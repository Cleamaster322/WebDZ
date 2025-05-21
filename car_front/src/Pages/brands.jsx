import { Autocomplete, TextField } from "@mui/material";
import { useState, useEffect } from "react";
import api from "../shared/api.jsx";

function Brands() {
  const [brands, setBrands] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      async function fetchBrands() {
        try {
          setLoading(true);

          // Параметры запроса — если есть inputValue, добавляем фильтр
          const params = inputValue
            ? { name: inputValue, page_size: 50 }
            : { page_size: 50 };

          const response = await api.get("/cars/brand", { params });

          const brandNames = response.data.results.map((brand) => brand.name);
          setBrands(brandNames);
        } catch (error) {
          console.error(error);
          setBrands([]);
        } finally {
          setLoading(false);
        }
      }

      fetchBrands();
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [inputValue]);

  return (
    <Autocomplete
      disablePortal
      options={brands}
      loading={loading}
      onInputChange={(event, newInputValue) => {
        setInputValue(newInputValue);
      }}
      sx={{ width: 300 }}
      renderInput={(params) => (
        <TextField {...params} label="Выберите бренд" />
      )}
    />
  );
}

export default Brands;
