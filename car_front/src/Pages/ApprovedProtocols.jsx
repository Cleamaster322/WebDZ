import ProtocolList from "../Features/Protocols/ProtocolList.jsx";

function ApprovedProtocols() {
    return (
        <ProtocolList
            title="Утверждённые протоколы"
            description="Протоколы, которые прошли проверку и были утверждены руководителем или исполнительным директором."
            statuses={["approved"]}
            emptyTitle="Утверждённые протоколы не найдены"
            emptyDescription="После утверждения завершённого протокола он будет отображаться на этой странице."
            showCreateButton={false}
        />
    );
}

export default ApprovedProtocols;