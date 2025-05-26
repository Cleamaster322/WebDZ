import React, {useState} from 'react';
import EmployeesList from '../Features/EmployeesList/EmployeesList.jsx';
import EmployeeProtocols from '../Features/EmployeeProtocols/EmployeeProtocols.jsx';

function Protocols() {
    const [selectedEmployee, setSelectedEmployee] = useState(null);

    return (
        <div>
            <EmployeesList onSelect={setSelectedEmployee}/>
            <EmployeeProtocols employee={selectedEmployee}/>
        </div>
    );
}

export default Protocols