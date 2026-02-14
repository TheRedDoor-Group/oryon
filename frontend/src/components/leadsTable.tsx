import type { Lead } from "../types/lead.type";

interface LeadsTableProps {
  leads: Lead[];
}

function LeadsTable({ leads }: LeadsTableProps) {
    if (leads.length === 0) {
        return (
            <div className="empty-state">
                <h3>Nenhum lead encontrado</h3>
                <p>Digite um termo acima e clique em "Garimpar" para começar.</p>
            </div>
        );
    }

    return (
        <div style={{ overflowX: 'auto' }}>
            <table className="leads-table">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Telefone</th>
                        <th>Tipo</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {leads.map((lead) => (
                        <tr key={lead.id}>
                            <td>{lead.business_name}</td> 
                            <td>{lead.phone_clean}</td>
                            <td>{lead.lead_type === 'mobile' ? '📱 Móvel' : '☎️ Fixo'}</td>
                            <td>
                                <span className={`status-badge ${lead.status === 'SENT_HELLO' ? 'sent' : 'new'}`}>
                                    {lead.status === 'SENT_HELLO' ? 'Enviado' : lead.status}
                                </span>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default LeadsTable;