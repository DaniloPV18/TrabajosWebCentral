import { LABELS, ARIA_LABELS } from "@/constants/labels";
import { useVacantes } from "@/context/VacantesContext";
import { COLORS } from "@/constants/colors";

export const SearchBar = () => {
  const { busqueda, setBusqueda } = useVacantes();

  return (
      <div className="mb-8 group">
      <div className="relative">
          {/* Top accent line */}
          <div className="absolute -top-1 left-0 right-0 h-1 bg-gradient-to-r from-cyan-500 to-violet-500 rounded-t-xl opacity-0 group-focus-within:opacity-100 transition-opacity"></div>
        
        <div className="absolute left-4 top-1/2 transform -translate-y-1/2 text-xl text-cyan-400">
          🔍
        </div>
        <input
          type="search"
          placeholder={LABELS.BUSCAR_PLACEHOLDER}
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
          aria-label={ARIA_LABELS.SEARCH_INPUT}
            className={`w-full pl-12 pr-12 py-4 text-lg font-medium ${COLORS.bg.secondary} ${COLORS.text.primary} border-2 ${COLORS.border.light} rounded-xl focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/30 shadow-lg placeholder-slate-500 transition-all hover:border-slate-400`}
        />
        {busqueda && (
          <button
            onClick={() => setBusqueda("")}
            aria-label={ARIA_LABELS.CLEAR_SEARCH}
              className={`absolute right-4 top-1/2 transform -translate-y-1/2 ${COLORS.text.tertiary} hover:text-cyan-400 text-2xl transition-colors p-2 rounded-lg hover:bg-slate-700/30`}
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
};
