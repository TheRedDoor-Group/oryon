import { useState, useEffect, useCallback } from 'react'
import { leadService } from './services/api'
import './styles/App.scss'
import Navbar from './components/navbar'
import LeadsTable from './components/leadsTable'
import type { Lead } from './types/lead.type'

function App() {
  const [leads, setLeads] = useState<Lead[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [loading, setLoading] = useState(false)

  const fetchLeads = useCallback(async () => {
    try {
      const data = await leadService.list()
      setLeads(data)
    } catch (error) {
      console.error("Erro ao buscar leads:", error)
    }
  }, [])

  useEffect(() => {
    fetchLeads()
  }, [fetchLeads])

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const executeAction = async (contexto: string, actionFn: () => Promise<any>) => {
    setLoading(true)
    try {
      await actionFn()
      alert(`${contexto} realizado com sucesso!`)
      await fetchLeads()
    } catch (error) {
      alert(`Erro ao ${contexto}: ${error}`)
    } finally {
      setLoading(false)
    }
  }

  const handleScrape = () => {
    if (!searchTerm) return alert("Digite um termo!")
    executeAction("Garimpo", () => leadService.scrape(searchTerm))
  }

  const handleSend = () => {
    if (!confirm("Isso vai abrir o WhatsApp. Confirmar?")) return
    executeAction("Envio", leadService.send)
  }

  const handleMonitor = async () => {
    if (!confirm("O Monitor vai abrir uma nova janela. Confirmar?")) return
    try {
      const res = await leadService.monitor()
      alert(res.message)
    } catch (error) {
      alert(error)
    }
  }

  return (
    <div className="dashboard-container">
      <header>
        <h1>Oryon Dashboard</h1>
      </header>

      <Navbar 
        searchTerm={searchTerm} 
        setSearchTerm={setSearchTerm} 
        handleScrape={handleScrape} 
        handleSend={handleSend} 
        handleMonitor={handleMonitor}
        loading={loading} 
      />

      <LeadsTable leads={leads} /> 
    </div>
  )
}

export default App