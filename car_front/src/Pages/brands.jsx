import { Autocomplete, TextField } from "@mui/material";
import {useEffect, useState} from "react";
import api from "../shared/api.jsx";


function Brands() {
    const [brands, setBrand] = useState([]);

    useEffect(() => {
        async function fetchBrands() {
            try {
                const response = await api.get("/cars/brand");
                const brandName = response.data.map((brand) => brand.name);
                setBrand(brandName);
            } catch (error) {
                console.log(error);
            }
        }
        fetchBrands();
    },[]);

  return (
    <>
      <Autocomplete
        disablePortal
        options={brands}
        sx={{ width: 300 }}
        renderInput={(params) => (
          <TextField {...params} label="Выберите бренд" />
        )}
      />
    </>
  );
}

export default Brands;