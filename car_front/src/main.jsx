import {createRoot} from 'react-dom/client'
import ReactDOM from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import CarSelection from './Pages/CarSelection.jsx'
import CarInfo from './Pages/CarInfo.jsx'
import Protocols from "./Pages/Protocols.jsx";
import ReportNotificationListener from './Features/ProtocolMessage/ProtocolMessage.jsx'

import {BrowserRouter, Route, Routes} from "react-router-dom";

ReactDOM.createRoot(document.getElementById('root')).render(
    <BrowserRouter>
        <ReportNotificationListener />
        <Routes>
            <Route path="/" element={<App/>}/>
            <Route path="/home" element={<CarSelection/>}/>
            <Route path="/CarInfo" element={<CarInfo/>}/>
            <Route path="/Protocols" element={<Protocols/>}/>
        </Routes>
    </BrowserRouter>
)