import React, {useEffect, useState} from 'react';
import api from "../../shared/api.jsx";

export default function EmployeeProtocols({employee}) {
    const [protocols, setProtocols] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!employee) return;

        setLoading(true);
        api.get('/cars/protocols/', {params: {user_id: employee.id}})  // эндпоинт получения протоколов по user_id
            .then(res => {
                setProtocols(res.data.results);
                setLoading(false);
            })
            .catch(err => {
                console.error('Ошибка загрузки протоколов:', err);
                setLoading(false);
            });
    }, [employee]);

    if (!employee) return null;

    if (loading) return <p>Загрузка протоколов для {employee.username || employee.email}...</p>;
    if (protocols.length === 0) return <p>Протоколы не найдены для {employee.username || employee.email}</p>;

    return (
        <div>
            <h3>Протоколы сотрудника {employee.username || employee.email}</h3>
            <ul>
                {protocols.map(p => (
                    <li key={p.id}>
                        {/* Здесь можно отобразить важные данные протокола, например: */}
                        Протокол #{p.id} от {new Date(p.created_at).toLocaleDateString()}
                    </li>
                ))}
            </ul>
        </div>
    );
}
