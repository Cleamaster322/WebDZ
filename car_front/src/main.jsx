import ReactDOM from "react-dom/client";
import "./index.css";

import App from "./App.jsx";
import CarSelection from "./Pages/CarSelection.jsx";
import CarInfo from "./Pages/CarInfo.jsx";
import Protocols from "./Pages/Protocols.jsx";
import CompletedProtocols from "./Pages/CompletedProtocols.jsx";
import ProtocolInspection from "./Pages/ProtocolInspection.jsx";
import Employees from "./Pages/Employees.jsx";
import { BrowserRouter, Route, Routes } from "react-router-dom";

ReactDOM.createRoot(document.getElementById("root")).render(
    <BrowserRouter>

        <Routes>
            <Route path="/" element={<App />} />
            <Route path="/home" element={<CarSelection />} />
            <Route path="/CarInfo" element={<CarInfo />} />
            <Route path="/protocols" element={<Protocols />} />
            <Route path="/protocols/completed" element={<CompletedProtocols />} />
            <Route path="/protocols/:id/inspection" element={<ProtocolInspection />} />
            <Route path="/employees" element={<Employees />} />

        </Routes>
    </BrowserRouter>
);