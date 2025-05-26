import React, {useEffect, useState} from 'react';
import api from "../../shared/api.jsx"

export default function EmployeesList({onSelect}) {
    const [employees, setEmployees] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('cars/get-all-users/')
            .then(res => {
                setEmployees(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error('Ошибка загрузки сотрудников:', err);
                setLoading(false);
            });
    }, []);

    if (loading) return <p>Загрузка сотрудников...</p>;
    if (employees.length === 0) return <p>Сотрудники не найдены</p>;

    return (
        <div>
            <h2>Сотрудники</h2>
            <ul>
                {employees.map(emp => (
                    <li key={emp.id}>
                        <button onClick={() => onSelect(emp)}>{emp.username || emp.email}</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}
