import { Bell, Search, Send } from "lucide-react";

interface NavbarProps {
    searchTerm: string;
    setSearchTerm: (value: string) => void;
    handleScrape: () => void;
    handleSend: () => void;
    handleMonitor: () => void;
    loading: boolean; 
}

function Navbar({ 
    searchTerm, 
    setSearchTerm, 
    handleScrape, 
    handleSend, 
    handleMonitor,
    loading 
}: NavbarProps) {
    return (
        <section className="controls">
            <input 
                type="text" 
                placeholder="Ex: Pizzaria em SP" 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            
            <button className="btn btn-scrape" onClick={handleScrape} disabled={loading}>
                {loading ? "Processando..." : <><Search size={18}/> Garimpar</>}
            </button>
            
            <button className="btn btn-send" onClick={handleSend} disabled={loading}>
                <Send size={18}/> Disparar WhatsApp
            </button>

            <button className="btn btn-monitor" onClick={handleMonitor} disabled={loading}>
                <Bell size={18}/> Monitorar
            </button>
        </section>
    );
}

export default Navbar;