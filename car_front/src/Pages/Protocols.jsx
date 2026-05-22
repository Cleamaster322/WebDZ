import ProtocolList from "../Features/Protocols/ProtocolList.jsx";

export default function Protocols() {
    return (
        <ProtocolList
            title="Протоколы в работе"
            description="Черновики и протоколы, которые ещё находятся в заполнении."
            statuses={["draft", "in_progress"]}
            emptyTitle="Нет протоколов в работе"
            emptyDescription="Создайте новый протокол через выбор автомобиля."
            showCreateButton={true}
        />
    );
}