import type { Lead } from "../types/lead.type";

interface LeadsTableProps {
  leads: Lead[];
}

function LeadsTable({ leads }: LeadsTableProps) {
    return (
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
                {leads.length > 0 ? (
                    leads.map((lead) => (
                        <tr key={lead.id}>
                            <td>{lead.business_name}</td> 
                            <td>{lead.phone_clean}</td>
                            <td>{lead.lead_type}</td>
                            <td>
                                <span className={`status-badge ${lead.status === 'SENT_HELLO' ? 'sent' : 'new'}`}>
                                    {lead.status === 'SENT_HELLO' ? '✅ Enviado' : lead.status}
                                </span>
                            </td>
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan={4} style={{ textAlign: 'center', padding: '2rem' }}>
                            Nenhum lead encontrado. Digite um termo e clique em "Garimpar".
                        </td>
                    </tr>
                )}
            </tbody>
        </table>
    );
}

export default LeadsTable;